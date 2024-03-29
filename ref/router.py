import datetime
import re

from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from fastapi.responses import JSONResponse, Response

from db import get_async_session
from utils.logger import logger
from .dependencies import get_ref_repository
from .repository import RefRepository

from utils.utils import fastapi_users

router = APIRouter(
    prefix="/referrals",
    tags=["referrals"]
)


# @router.get("/my")
# async def my(
#         repository: RefRepository = Depends(get_ref_repository(get_async_session)),
#         user=Depends(fastapi_users.current_user(active=True))
# ):
#     referrals = await repository.get_referrals_by_id(user.id)
#     return JSONResponse(
#         content={
#             "referrer": user.id,
#             "referrals": referrals
#         },
#         status_code=200
#     )


@router.get("/by_id/{id_:int}")
async def get_referrals_by_id(
        id_: int,
        repository: RefRepository = Depends(get_ref_repository(get_async_session))
):
    referrals = await repository.get_referrals_by_id(id_)

    if referrals is None:
        logger.error(f"Referrer ID does not exist: {id_}")
        raise HTTPException(
            status_code=404,
            detail="Referrer ID does not exist",
        )

    logger.info(f"Successfully retrieved referrals for ID: {id_}: {referrals}")
    return JSONResponse(
        content={
            "referrer": id_,
            "referrals": referrals
        },
        status_code=200
    )


@router.get("/code_by_email/{email}")
async def get_referrer_code_by_email(
        email: str = Path(..., example="user@example.com"),
        repository: RefRepository = Depends(get_ref_repository(get_async_session))
):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, email):
        raise HTTPException(status_code=404, detail="Invalid Email")

    code = await repository.get_code_by_email(email)

    if code is None:
        logger.error(f"The user with the email does not have a referral code: {email}")
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not have a referral code",
        )

    logger.info(f"Successfully retrieved referrer code by email: {email}: {code}")
    return JSONResponse(
        content={
            "code": code,
        },
        status_code=200
    )


#
# @router.get("/by_email/{email}")
# async def get_referrals_by_email(
#         email: str = Path(..., min_length=4, max_length=24, example="user@example.com"),
#         repository: RefRepository = Depends(get_ref_repository(get_async_session))
# ):
#     email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#     if not re.match(email_regex, email):
#         raise HTTPException(status_code=404, detail="Invalid Email")
#
#     referrals = await repository.get_referrals_by_email(email)
#
#     if referrals is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Referrer email does not exist",
#         )
#
#     return JSONResponse(
#         content={
#             "referrer": email,
#             "referrals": referrals
#         },
#         status_code=200
#     )
#
#
# @router.get("/by_code/{code}")
# async def get_referrals_by_code(
#         code: str = Path(..., min_length=4, max_length=24, example="GADJIIAVOV", regex="^#?[a-zA-Z0-9]+$"),
#         repository: RefRepository = Depends(get_ref_repository(get_async_session))
# ):
#     referrals = await repository.get_referrals_by_code(code)
#
#     if referrals is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Referrer code does not exist",
#         )
#
#     return JSONResponse(
#         content={
#             "referrer": code,
#             "referrals": referrals,
#         },
#         status_code=200
#     )


@router.post("/create_code")
async def create_code(
        code: str = Body(..., min_length=4, max_length=24, example="GADJIIAVOV", regex="^#?[a-zA-Z0-9]+$"),
        expiration: datetime.datetime = Body(..., example="2024-02-24T12:00:00.000Z"),
        user=Depends(fastapi_users.current_user(active=True)),
        repository: RefRepository = Depends(get_ref_repository(get_async_session)),
):
    expiration = expiration.replace(tzinfo=None)

    if user.referral_code:
        logger.error(f"A code({user.referral_code}) already exist ({user.id})")
        raise HTTPException(
            status_code=418,
            detail=f"A code already exist ({user.referral_code} -"
                   f" expires {user.referral_code_expiration})")

    code_exists = await repository.get_id_by_code(code)
    if code_exists:
        logger.error(f"The code already exist {user.id}")
        raise HTTPException(
            status_code=403,
            detail="The code already exist. Use another one"
        )

    await repository.create_code_for_user_by_id(user.id, code, expiration)

    logger.info(f"Successfully created code for ID: {user.id}; Code: {code}; Expiration: {expiration}")
    return JSONResponse(
        content={
            "code": code,
            "expiration": str(expiration),
        },
        status_code=200
    )


@router.delete("/delete_code")
async def delete_code(
        user=Depends(fastapi_users.current_user(active=True)),
        repository: RefRepository = Depends(get_ref_repository(get_async_session)),
):
    if not user.referral_code:
        logger.error(f"The code does not exist ({user.id})")
        raise HTTPException(status_code=418, detail="The code does not exist")

    await repository.delete_code_for_user_by_id(user.id)

    logger.info(f"Successfully deleted code for ID: {user.id}")
    return Response(status_code=200)
