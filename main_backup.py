from typing import Annotated
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field


app = FastAPI()


# # request body
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax:
#         price_with_tax = item.price * (1 + item.tax)
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.model_dump()}


# @app.get("/items/")
# async def read_times(
#     q: Annotated[str | None, Query(min_length=3, max_length=50)] = None
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# multiple query parameters
# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         list[str] | None,
#         Query(
#             alias="item-query",
#             title="Query string",
#             description="Query string for the items to searh in the database",
#             min_length=3,
#             max_length=50,
#             # pattern="^fixedquery$",
#         ),
#     ] = None
# ):
#     query_items = {"q": q}
#     return query_items


# @app.get("/items/{item_id}")
# async def read_item(
#     item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
#     q: Annotated[str | None, Query(alias="item-query")] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results


# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         list[str] | None,
#         Query(
#             alias="item-query",
#             title="Query string",
#             description="Query string for the items to searh in the database",
#             min_length=3,
#             max_length=50,
#             # pattern="^fixedquery$",
#         ),
#     ] = None
# ):
#     query_items = {"q": q}
#     return query_items
