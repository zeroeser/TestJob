import requests as req

from app import crud, requests
from app.db.session import SessionLocal
from app.dto.contracts import DeliveriesIn
from app.requests.cbr.cbr_methods import get_cbr_quotes
from app.requests.sheet import get_sheet_info
from app.settings import settings
from scheduler.app import celery


@celery.task(name="database_update", track_started=True)
def database_update():
    # Вытаскиваю данные из экселя
    list_of_contracts = get_sheet_info()
    excel_ids = set(x.get("заказ №") for x in list_of_contracts)
    # Вытаскиваю сегодняшний курс доллара
    usd_exchange_rate = get_cbr_quotes()
    if not usd_exchange_rate:
        raise Exception("Usd exchange request error")
    with SessionLocal() as db:
        # Собираю все ключи из базы данной
        db_ids = set(e.order_number for e in crud.deliveries.get_all(db))
        inserted = excel_ids - db_ids  # Новые id из экселя
        deleted = db_ids - excel_ids  # Удаленные id из экселя
        for data in list_of_contracts:
            delivery = DeliveriesIn.from_excel(
                data, usd_exchange_rate
            )  # Преобразование Dict в Pydantic модель
            if (
                delivery.order_number in inserted
            ):  # Добавление нового контракта, если оно находится в inserted
                crud.deliveries.create(db, obj_in=delivery)
                message = f"Cрок поставки {delivery.order_number} просрочен"
                telegram_notification.apply_async(
                    args=(message,),
                    eta=delivery.delivery_time,  # Добавление задачи оповещения в Celery
                )
                continue
            db_obj = crud.deliveries.get(db, obj_id=delivery.order_number)
            crud.deliveries.update(db, obj_in=delivery, db_obj=db_obj)
        for id in deleted:
            crud.deliveries.remove(db, obj_id=id)

        db.commit()


@celery.task(name="telegram_notification", track_started=True)
def telegram_notification(message: str) -> None:
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    req.get(
        url,
        params={
            "chat_id": settings.TELEGRAM_NOTIFICATION_USER_CHAT_ID,
            "text": message,
        },
    )


a = database_update()
