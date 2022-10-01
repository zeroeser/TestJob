from typing import Any, Dict, Tuple

import gspread

from app.settings import settings


def get_sheet_info() -> Tuple[Dict[str, Any]]:
    sa = gspread.service_account_from_dict(settings.credentials)
    sh = sa.open("Test")

    wks = sh.worksheet("Лист1")
    return tuple(wks.get_all_records())
