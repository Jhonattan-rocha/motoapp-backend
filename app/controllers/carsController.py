from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.carModel import Car
from app.schemas import carsSchema


async def create_car(db: AsyncSession, car: carsSchema.CarBase):
    db_car = Car(**car.model_dump(exclude_none=True))
    db.add(db_car)
    await db.commit()
    await db.refresh(db_car)
    return db_car


async def get_cars(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Car).offset(skip).limit(limit if limit > 0 else None))
    return result.scalars().unique().all()


async def get_car(db: AsyncSession, car_id: int):
    result = await db.execute(select(Car).where(Car.id == car_id))
    car = result.scalars().unique().first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid id, not found",
        )
    return car


async def update_car(db: AsyncSession, car_id: int, updated_car: carsSchema.CarCreate):
    result = await db.execute(select(Car).where(Car.id == car_id))
    car = result.scalars().first()
    if car is None:
        return None

    for key, value in updated_car.model_dump(exclude_none=True).items():
        if str(value):
            setattr(car, key, value)

    await db.commit()
    await db.refresh(car)
    return car


async def delete_car(db: AsyncSession, car_id: int):
    result = await db.execute(select(Car).where(Car.id == car_id))
    car = result.scalars().first()
    if car is None:
        return None
    await db.delete(car)
    await db.commit()
    return car
