from fastapi import APIRouter
import app.src.endpoints.books as books
import app.src.endpoints.sport as sport

router = APIRouter(
    prefix="/api/v1",
)
router.include_router(books.router)
router.include_router(sport.router)