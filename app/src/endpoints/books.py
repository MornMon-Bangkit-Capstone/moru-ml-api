from fastapi import APIRouter
import app.src.method.recommendation_content as rec
import app.src.method.recommendation_collaborative as rec_col

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.post("/recommendation_content/{judul}/{jumlah}")
async def recommendation(judul: str, jumlah: int):
    recom = rec.recommendation_by_keyword(judul, jumlah)
    return {"message": 'Data Sucessfully Generated', "status": 200, "error": False, "data": recom}

@router.post("/recommendation_collaborative/{user_id}")
async def recommendation_col(user_id: str):
    print(user_id)
    recom = rec_col.recommendation(user_id)
    return {"message": 'Data Sucessfully Generated', "status": 200, "error": False, "data": recom}
