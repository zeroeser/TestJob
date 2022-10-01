from typing import Any, Optional, Type


class ModelNotFoundException(Exception):
    def __init__(
        self,
        message: Optional[str] = None,
        model: Optional[Type] = None,
        obj_id: Any = None,
    ):
        self.model: Optional[Type] = model
        self.id: Any = obj_id

        if message is None:
            message = f"Model of type '{model.__name__ if model else 'N/A'}' with ID='{obj_id}' not found"

        self.message: Optional[str] = message

        super().__init__(self.message)
