from datetime import datetime
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.errors import ModelNotFoundException
from app.db import Base

ModelType = TypeVar("ModelType", bound=Base)
KeyType = TypeVar("KeyType", bound=int)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, KeyType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, obj_id: KeyType) -> Optional[ModelType]:
        """
        Get object by id
        """
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Add new object
        """
        obj_in_data = jsonable_encoder(obj_in, custom_encoder={datetime: lambda dt: dt})

        db_obj = self.model(**obj_in_data)  # type: ignore

        db.add(db_obj)
        db.flush()
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update existed object
        """
        if not db_obj:
            raise AttributeError("Database object is not present!")

        keys = list(vars(db_obj).keys())
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in keys:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.flush()

        return db_obj

    def remove(self, db: Session, *, obj_id: KeyType) -> ModelType:
        """
        Delete object from database
        """
        obj: Optional[ModelType] = db.get(self.model, obj_id)

        if obj is None:
            raise ModelNotFoundException(model=self.model, obj_id=obj_id)
        db.delete(obj)
        db.flush()

        return obj
