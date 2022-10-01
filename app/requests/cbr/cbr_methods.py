import datetime as dt
from typing import Optional

import requests
from lxml import etree

from app.settings import settings


def get_cbr_quotes() -> Optional[float]:
    response = requests.get(
        url=settings.CBR_URL, params={"date_req": dt.date.today().strftime("%d/%m/%Y")}
    )
    val_curs = etree.fromstring(response.content)
    value = None
    for item in val_curs.xpath('//ValCurs/Valute[@ID="R01235"]/Value/text()'):
        value = float(item.replace(",", "."))

    return value
