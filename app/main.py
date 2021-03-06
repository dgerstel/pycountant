from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.templating import Jinja2Templates

from typing import Optional, Any
from pathlib import Path

from app.transfers_data import TRANSFERS
from app.schemas import Transfer, TransferCreate


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "transfers": TRANSFERS},
    )


@api_router.get("/history/{transfer_id}", status_code=200)
def fetch_history(*, transfer_id: int) -> dict:
    result = [t for t in TRANSFERS if t["id"]==transfer_id]
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Transfer with ID {transfer_id} not found"
        )
    return result[0]


# New addition, query parameter
# https://fastapi.tiangolo.com/tutorial/query-params/
@api_router.get("/search/", status_code=200)
def search_recipes(*,
    keyword: Optional[str] = Query(None, min_lenth=3, example="mcdonalds"), max_results: Optional[int] = 10
) -> dict:
    """
    Search for transfers based on client keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": TRANSFERS[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["client"].lower(), TRANSFERS)
    return {"results": list(results)[:max_results]}


@api_router.post("/transfer/", status_code=201, response_model=Transfer)
def create_recipe(*, recipe_in: TransferCreate) -> dict:
    """
    Create a new transfer (in memory only)
    """
    new_entry_id = len(TRANSFERS) + 1
    transfer_entry = Transfer(
        id=new_entry_id,
        amount=recipe_in.amount,
        client=recipe_in.client,
        vat=recipe_in.vat,
        descr=recipe_in.descr
    )
    TRANSFERS.append(transfer_entry.dict())

    return transfer_entry


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
