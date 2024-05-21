from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import Annotated
from redis.asyncio import Redis

from app.schemas.data import DataModel, ResponseCheckData, RequestData
from app.core.db import init_redis_pool

router = APIRouter()


@router.post("/write_data")
async def write_data(data: DataModel,
                     redis: Annotated[Redis, Depends(init_redis_pool)]):
    if not await redis.exists(data.phone):
        await redis.set(name=data.phone, value=data.address)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                'phone': data.phone,
                'address': data.address
            })
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="This is phone was created yet")


@router.put("/write_data")
async def write_data(data: DataModel,
                     redis: Annotated[Redis, Depends(init_redis_pool)]):
    if await redis.exists(data.phone):
        await redis.set(name=data.phone, value=data.address)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'phone': data.phone,
                'address': data.address
            })
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Phone number not found")


@router.get("/check_data", response_model=ResponseCheckData)
async def check_data(phone: RequestData,
                     redis: Annotated[Redis, Depends(init_redis_pool)]):
    address = await redis.get(phone)
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Phone number not found")
    return ResponseCheckData(address=address)
