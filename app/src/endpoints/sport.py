from fastapi import APIRouter
import app.src.method.recommendation_sport as rec

router = APIRouter(
    prefix="/sport",
    tags=["sport"],
    responses={404: {"description": "Not found"}},
)

@router.post("/recommendation_content/{judul}")
async def recommendation(judul: str):
    recom = rec.sports_recommendations(judul)
    return {"message": 'Data Sucessfully Generated', "status": 200, "error": False, "data": recom}