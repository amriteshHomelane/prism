"""Data store facade. Picks the backend automatically:

- Google Sheets (shared, multi-user, persistent) when secrets.toml has
  [gcp_service_account] and [sheets].sheet_id.
- Local JSON file (single machine, zero setup) otherwise.

The app only ever calls store.* — the backend swap is invisible to it.
"""

import streamlit as st


def _use_sheets():
    try:
        return ("gcp_service_account" in st.secrets
                and "sheets" in st.secrets
                and bool(st.secrets["sheets"].get("sheet_id")))
    except Exception:
        return False


if _use_sheets():
    from backend_sheets import *  # noqa: F401,F403
    BACKEND = "Google Sheets (shared)"
else:
    from backend_local import *  # noqa: F401,F403
    BACKEND = "Local file (single machine)"
