"""
Custom MCP server exposing pytest test-running tools to an AI agent.

Pairs with the official Playwright MCP server (browser/selector discovery).
This server gives the agent a feedback loop: run the suite, read structured
failures, then edit the Page Objects / tests to fix them.

Tools:
  - run_tests(test_path, markers): run pytest, return a pass/fail summary
  - get_failures(): structured failures (file, test, traceback) from the last run
  - list_tests(): collect-only listing of available tests
"""
import json
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Repo root is one level up from this file.
REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = REPO_ROOT / ".mcp_last_run.json"

mcp = FastMCP("automation-test-runner")


def _run_pytest(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", "-m", "pytest", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


@mcp.tool()
def run_tests(test_path: str = "tests", markers: str = "") -> str:
    """Run the pytest suite (or a subset) and return a summary.

    Args:
        test_path: Path or node id to run (default: the whole `tests` dir).
        markers: Optional `-m` marker expression (e.g. "not slow").
    """
    args = [test_path, "-v", "--tb=short", f"--json-report",
            f"--json-report-file={REPORT_PATH}"]
    if markers:
        args += ["-m", markers]

    proc = _run_pytest(args)
    summary = {"returncode": proc.returncode}

    if REPORT_PATH.exists():
        data = json.loads(REPORT_PATH.read_text())
        summary["summary"] = data.get("summary", {})
    summary["stdout_tail"] = proc.stdout[-3000:]
    return json.dumps(summary, indent=2)


@mcp.tool()
def get_failures() -> str:
    """Return structured failures (test id, file, line, traceback) from the last run."""
    if not REPORT_PATH.exists():
        return "No run found. Call run_tests first."

    data = json.loads(REPORT_PATH.read_text())
    failures = []
    for test in data.get("tests", []):
        if test.get("outcome") not in ("passed", "skipped"):
            call = test.get("call", {})
            failures.append({
                "test_id": test.get("nodeid"),
                "outcome": test.get("outcome"),
                "traceback": (call.get("longrepr") or "")[-2000:],
            })
    if not failures:
        return "No failures in the last run."
    return json.dumps(failures, indent=2)


@mcp.tool()
def list_tests() -> str:
    """List all collectible tests without running them."""
    proc = _run_pytest(["--collect-only", "-q"])
    return proc.stdout[-3000:]


if __name__ == "__main__":
    mcp.run()
