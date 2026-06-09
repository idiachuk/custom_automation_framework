# Custom API + E2E Test Automation Framework


## NOTE:
this framework is dockerized, so to run it you need to have Docker server installed 

Setup:

1. Clone the git repo to local folder
2. Navigate to this folder
3. Build docker container by running: docker build -t custom_framework .
4. Run docker image by: docker run -it --rm --ipc=host -p 8888:8080 custom_framework
5. Observe test run results at: http://localhost:8888
6. Video Explanation: https://drive.google.com/file/d/17udbQFSD6z9uHs_szd8hAuqOkGgF_JjB/view?usp=sharing

## MCP servers — AI-driven test fixing

The framework includes an MCP (Model Context Protocol) setup that lets an AI agent
(e.g. Claude Desktop) run the tests, inspect the live app in a real browser, and fix
broken locators by itself. Two servers work together:

- **`@playwright/mcp`** (official, runs via `npx`) — browser driving and selector discovery
- **`automation-test-runner`** ([mcp_server/test_runner_server.py](mcp_server/test_runner_server.py)) — runs pytest and returns structured failures

### Local setup

1. Install Python dependencies and browsers:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
2. Make sure Node.js is installed (needed for `npx @playwright/mcp`).
3. Add both servers to your MCP client config. For Claude Desktop, merge
   [mcp_server/claude_desktop_config.example.json](mcp_server/claude_desktop_config.example.json)
   into:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

   Adjust the absolute path to `test_runner_server.py` to match your machine.
4. Fully restart the MCP client (on macOS: Cmd+Q, then reopen). Both servers should
   appear in the tools list.

See [mcp_server/README.md](mcp_server/README.md) for the architecture and a typical
agent fix loop.
