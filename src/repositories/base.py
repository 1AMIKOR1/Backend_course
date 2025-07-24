from sqlalchemy import insert, select, update, delete

from pydantic import BaseModel

from database import Base


class BaseRepository:
    model: Base = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, limit=None, offset=None, **filter_by ) -> list[BaseModel]:
        query = select(self.model).filter_by(**filter_by)

        if limit  is not None and offset is not None:
            query = query.limit(limit).offset(offset)
            
        result = await self.session.execute(query)
        result = [self.schema.model_validate(model) for model in result.scalars().all()]
        return result

    async def get_all(self, *args, **kwargs) -> list[BaseModel]:
        return await self.get_filtered(**kwargs)

    async def get_one_or_none(self, **filter_by) -> None | BaseModel:
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)

        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:

        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(edit_stmt)
