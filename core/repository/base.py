from typing import Any, Generic, Type, TypeVar, Optional, Union
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from core.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base class for data repositories."""

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model_class: Type[ModelType] = model

    async def create(self, attributes: dict[str, Any] = None) -> ModelType:
        if attributes is None:
            attributes = {}
        model = self.model_class(**attributes)
        self.session.add(model)
        return model

    async def get_all(
            self
    ) -> list[ModelType]:
        query = self.query()
        return await self.all(query)

    async def get_by(
            self,
            field: str,
            value: Any,
            unique: bool = False,
    ) -> Union[ModelType, list[ModelType]]:
        query = self.query()
        query = await self._get_by(query, field, value)
        if unique:
            return await self.one(query)
        else:
            return await self.all(query)

    async def delete(self, model: ModelType) -> None:
        await self.session.delete(model)

    def query(
            self,
            order_: Optional[dict] = None,
    ) -> Select:
        query = select(self.model_class)
        query = self._maybe_ordered(query, order_)
        return query

    async def all(self, query: Select) -> list[ModelType]:
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def one(self, query: Select) -> ModelType:
        result = await self.session.execute(query)
        return result.scalars().first()

    async def _get_by(self, query: Select, field: str, value: Any) -> Select:
        return query.where(getattr(self.model_class, field) == value)

    def _maybe_ordered(self, query: Select, order_: Optional[dict] = None) -> Select:
        if order_:
            if order_["asc"]:
                for order in order_["asc"]:
                    query = query.order_by(getattr(self.model_class, order).asc())
            else:
                for order in order_["desc"]:
                    query = query.order_by(getattr(self.model_class, order).desc())
        return query

    async def get(self, key_value: Any) -> ModelType:
        # Dynamically access the __keyfield__ attribute from the model class
        key_field = getattr(self.model_class, "keyfield", None)
        if key_field is None:
            raise AttributeError(f"{self.model_class.__name__} does not have a 'keyfield' attribute")

        return await self.get_by(key_field, key_value, unique=True)
