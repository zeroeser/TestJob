from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.dto.contracts import DeliveriesIn
from app.models import Deliveries


class CRUDDeliveries(CRUDBase[Deliveries, int, DeliveriesIn, DeliveriesIn]):
    def get(self, db: Session, obj_id: int) -> Optional[Deliveries]:
        """
        Get model by id
        """
        return db.query(self.model).filter(self.model.order_number == obj_id).first()

    def get_all(self, db: Session) -> Optional[List[Deliveries]]:
        """
        Get all list of models
        """
        return db.query(self.model).all()


deliveries = CRUDDeliveries(Deliveries)
