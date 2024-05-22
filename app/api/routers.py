from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.responses import JSONResponse
from typing import Annotated
from redis.asyncio import Redis

from app.schemas.data import DataModel, ResponseCheckData, RequestData
from app.core.db import init_redis_pool

router = APIRouter()


@router.post("/write_data")
async def write_data(data: DataModel,
                     redis: Annotated[Redis, Depends(init_redis_pool)]):
    """
    Ендпоинт для записи данных в хранилище Redis
    :param data: Данные для записи - номер телефона(валидация происходит на стороне pydantic
    по регулярному выражению ^8\d{10}$ и адрес
    :param redis: Экземпляр клиента Redis
    :return: Если запись прошла успешно, возвращается 201 статус,
    если не удалось записать данные, то возвращается статус 500
    """
    try:
        await redis.set(name=data.phone, value=data.address)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                'phone': data.phone,
                'address': data.address
            })
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong")


@router.get("/check_data", response_model=ResponseCheckData)
async def check_data(phone: Annotated[str, Query(..., pattern=r"^8\d{10}$")],
                     redis: Annotated[Redis, Depends(init_redis_pool)]):
    """
    Эндпоинт для получения адреса по номеру телефона.
    :param phone: Номер телефона - валидация происходит на стороне pydantic
    по регулярному выражению ^8\d{10}$
    :param redis: Экземпляр клиента Redis
    :return: Если номера телефона не найден, возвращается ошибка 404,
    если запрос прошел успешно, то возвращается адрес
    """
    address = await redis.get(phone)
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Phone number not found")
    return ResponseCheckData(address=address)
