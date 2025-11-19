# CardBrandIdentifier

A small, elegant tool to detect credit card brands from card numbers. Built for clarity and tested end-to-end. Stylish, minimal, and created entirely in Visual Studio Code with GitHub Copilot for the DIO GitHub Copilot Course.

## Features
- Lightweight server (app.py) that accepts a card number and returns the detected brand.
- Simple client (client.py) to query the server from the command line.
- Unit/integration tests (test_app.py) to validate detection logic and endpoints.

## Project layout
- app.py       — server application
- client.py    — command line client that queries the server
- test_app.py  — pytest test suite
- requirements.txt — Python dependencies (if present)
- README.md    — this guide

## Prerequisites
- Python 3.8+
- (Optional) virtualenv
- Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

## Running the server (app.py)
Start the server:
```bash
python app.py
```
By default the server listens on localhost (e.g. http://127.0.0.1:5000). Check the app.py startup message for the exact host/port.

Example curl usage:
```bash
curl -X POST http://127.0.0.1:5000/identify -d '{"card":"4111111111111111"}' -H "Content-Type: application/json"
# -> {"brand":"VISA"}
```

## Using the client (client.py)
Run the client to send a card number to the running server. Two common ways:

Interactive / positional:
```bash
python client.py 4111111111111111
```

Or explicit host/port (if supported by client.py):
```bash
python client.py --host 127.0.0.1 --port 5000 --card 4111111111111111
```

The client prints the server response (detected brand and optional metadata).

## Testing (test_app.py)
Run the test suite with pytest:
```bash
pytest -q test_app.py
```
This validates detection rules and the server endpoint(s).

## Notes & Tips
- Keep the server running while using the client or tests that depend on it.
- Tests are designed to be fast and deterministic; run them often during development.
- Use Git for version control and VS Code + GitHub Copilot to accelerate iteration.

Project created entirely using Visual Studio Code with GitHub Copilot for the DIO GitHub Copilot Course.
