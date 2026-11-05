# python3-hello-ms-updates

Python 3 template that makes an HTTP call to the Microsoft Update Catalog
and does a very simple check for available Windows 11 updates.

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python check_updates.py
```

## Test
```bash
pip install pytest
pytest
```
