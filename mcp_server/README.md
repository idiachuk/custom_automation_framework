# MCP Server — AI-driven test fixing

A hybrid setup that lets an AI agent (Claude Desktop) inspect the live app and
autonomously fix broken Playwright tests.

## Architecture

Two MCP servers work together:

| Server | Role |
| --- | --- |
| **`@playwright/mcp`** (official, Node) | Drives a real browser. The agent navigates SauceDemo, snapshots the DOM/accessibility tree, and discovers the correct selectors when locators break. |
| **`automation-test-runner`** (custom, this repo) | Runs pytest and returns structured failures so the agent has a feedback loop: run → read failure → edit Page Object → re-run. |

### Custom server tools
- `run_tests(test_path, markers)` — run the suite (or a subset), return a pass/fail summary.
- `get_failures()` — structured failures (test id, outcome, traceback) from the last run.
- `list_tests()` — collect-only listing of available tests.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. Make sure Node is available (for the official Playwright MCP, run via `npx`).

3. Copy `mcp_server/claude_desktop_config.example.json` into your Claude Desktop
   config and adjust the absolute path to match your machine:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

4. Restart Claude Desktop. Both servers should appear in the MCP tools list.

## Typical agent loop

> "The purchase test is failing. Investigate and fix it."

1. `run_tests("tests/test_purchase_positive.py")` → sees the failure
2. `get_failures()` → reads the traceback (e.g. a locator no longer matches)
3. Playwright MCP: `browser_navigate` + `browser_snapshot` → finds the real selector
4. Edits `pages/pages.py` / `pages/locators.py`
5. `run_tests(...)` again → confirms green
