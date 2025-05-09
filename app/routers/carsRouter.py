from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers import carsController
from app.controllers.tokenController import verify_token
from app.database import database
from app.schemas import carsSchema

router = APIRouter(prefix="/crud")

@router.post("/car/", response_model=carsSchema.CarCreate)
async def create_car(car: carsSchema.CarBase, db: AsyncSession = Depends(database.get_db), validation: str = Depends(verify_token)):
    return await carsController.create_car(car=car, db=db)


@router.get("/car/", response_model=list[carsSchema.Car])
async def read_cars(skip: int = 0, limit: int = 10,
                     db: AsyncSession = Depends(database.get_db),
                     validation: str = Depends(verify_token)):
    return await carsController.get_cars(skip=skip, limit=limit, db=db)


@router.get("/car/{car_id}", response_model=carsSchema.Car)
async def read_car(car_id: int, db: AsyncSession = Depends(database.get_db), validation: str = Depends(verify_token)):
    return await carsController.get_car(car_id=car_id, db=db)


@router.put("/car/{car_id}", response_model=carsSchema.CarCreate)
async def update_car(car_id: int, updated_car: carsSchema.CarCreate,
                      db: AsyncSession = Depends(database.get_db), validation: str = Depends(verify_token)):
    return await carsController.update_car(car_id=car_id, updated_car=updated_car, db=db)


@router.delete("/car/{car_id}")
async def delete_car(car_id: int, db: AsyncSession = Depends(database.get_db),
                      validation: str = Depends(verify_token)):
    return await carsController.delete_car(car_id=car_id, db=db)
