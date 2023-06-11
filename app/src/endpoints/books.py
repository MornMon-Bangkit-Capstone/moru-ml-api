from fastapi import APIRouter, Depends
import app.src.method.recommendation_content as rec
import app.src.method.recommendation_collaborative as rec_col
import app.src.method.retrain_collaborative as retrain
import requests
import pandas as pd

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

# database = Database()
# engine = database.get_db_connection()

@router.post("/recommendation_content/{judul}/{jumlah}")
async def recommendation(judul: str, jumlah: int):
    recom = rec.recommendation_by_keyword(judul, jumlah)
    return {"message": 'Data Sucessfully Generated', "status": 200, "error": False, "data": recom}

@router.post("/recommendation_collaborative/{user_id}") # 
async def recommendation_col(user_id: str):
    print(user_id)
    recom = rec_col.recommendation(user_id)
    return {"message": 'Data Sucessfully Generated', "status": 200, "error": False, "data": recom}

@router.get("/retrain")
async def allBooks():
    urlBooks = "https://database---moru-api-backend-inq7f5uz7q-et.a.run.app/database/title"
    urlRatings = "https://database---moru-api-backend-inq7f5uz7q-et.a.run.app/database/rating"
    responseJsonBook = requests.get(urlBooks)
    responseJsonRatings = requests.get(urlRatings)
    dataBook = responseJsonBook.json()
    dataRatings = responseJsonRatings.json()
    Books = pd.DataFrame(dataBook.get('message'))
    Ratings = pd.DataFrame(dataRatings.get('message'))
    retrain.train(Ratings, Books)
    # print(Ratings)
    # print(Books)
    return {"message": 'New Model Sucessfully Generated', "status": 200, "error": False}
