"""Entry point kept for `uvicorn community-api:app` (run from this folder). The code lives in the hba package:
hba/main.py assembles it; hba/routers/ has one module per area of the portal."""
from hba.main import app  # noqa: F401
