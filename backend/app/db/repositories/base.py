from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from ...core.logger import log_error

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, db: AsyncIOMotorDatabase, model: Type[ModelType], collection_name: str):
        self.db = db
        self.model = model
        self.collection = db[collection_name]

    async def find_one(self, query: Dict[str, Any]) -> Optional[ModelType]:
        try:
            result = await self.collection.find_one(query)
            return self.model(**result) if result else None
        except Exception as e:
            log_error(e, {"context": f"find_one in {self.collection.name}", "query": query})
            raise

    async def find_many(self, query: Dict[str, Any]) -> List[ModelType]:
        try:
            cursor = self.collection.find(query)
            results = await cursor.to_list(None)
            return [self.model(**doc) for doc in results]
        except Exception as e:
            log_error(e, {"context": f"find_many in {self.collection.name}", "query": query})
            raise

    async def create(self, data: Dict[str, Any]) -> ModelType:
        try:
            result = await self.collection.insert_one(data)
            created_doc = await self.collection.find_one({"_id": result.inserted_id})
            return self.model(**created_doc)
        except Exception as e:
            log_error(e, {"context": f"create in {self.collection.name}", "data": data})
            raise

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
        try:
            result = await self.collection.update_one(
                {"note_id":id},
                {"$set": data}
            )
            if result.modified_count:
                updated_doc = await self.collection.find_one({"note_id": id})
                return self.model(**updated_doc) if updated_doc else None
            return None
        except Exception as e:
            log_error(e, {"context": f"update in {self.collection.name}", "id": id, "data": data})
            raise

    async def delete(self, id: str) -> bool:
        try:
            result = await self.collection.delete_one({"note_id": id})
            return result.deleted_count > 0
        except Exception as e:
            log_error(e, {"context": f"delete in {self.collection.name}", "id": id})
            raise