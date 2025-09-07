from sqlalchemy import insert, select, update, delete

from pydantic import BaseModel

from src.database import Base, engine
from src.repositories.mapper.base import DataMapper


class BaseRepository:
    model = None
    schema = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(
        self, limit:int | None = None, offset:int | None = None, *filter, **filter_by
    ) -> list[BaseModel]:
        
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        filter = [v for v in filter if v is not None ]
        
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
            )
        
        if limit and offset:
            query = query.limit(limit).offset(offset)
        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        result = [self.mapper.map_to_schema(model) for model in result.scalars().all()]
        
        return result

    async def get_all(self, *args, **kwargs) -> list[BaseModel]:
        return await self.get_filtered(*args, **kwargs)

    async def get_one_or_none(self, **filter_by) -> None | BaseModel:
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_schema(model)

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        print(add_stmt.compile(compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(add_stmt)

        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_schema(model)
    
    async def add_bulk(self, data: list[BaseModel])  -> None | BaseModel:
        '''
        Метод для множественного добавления данных в таблицу
        '''
        add_stmt = insert(self.model).values([item.model_dump() for item in data])
        # print(add_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(add_stmt)

      
    async def delete(self, *filters, **filter_by) -> None:
        delete_stmt = delete(self.model)

        if filter_by:
            delete_stmt = delete_stmt.filter_by(**filter_by)
    
    
        if filters:
            delete_stmt = delete_stmt.filter(*filters)
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
