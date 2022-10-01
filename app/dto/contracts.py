from datetime import datetime as dt

from pydantic import BaseModel, Field


class DeliveriesIn(BaseModel):
    number: int = Field(description="позиция в экселе")
    order_number: int = Field(description="номер заказа")
    price_in_dollar: int = Field(description="Стоимость в долларах")
    delivery_time: dt = Field(description="Срок поставки")
    price_in_rub: float = Field(description="Стоимость в рублях по курсу Центробанка")

    class Config:
        orm_mode = True
        title = "Преобразование данных из экселя"

    @classmethod
    def from_excel(cls, data, usd_exchange_rate):
        return cls(
            number=data["№"],
            order_number=data["заказ №"],
            price_in_dollar=data["стоимость,$"],
            delivery_time=dt.strptime(data["срок поставки"], "%d.%m.%Y"),
            price_in_rub=data["стоимость,$"] * usd_exchange_rate,
        )
