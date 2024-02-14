import re

from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from fastapi.responses import JSONResponse, Response

from db import get_async_session
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
        raise HTTPException(
            status_code=404,
            detail="Referrer ID does not exist",
        )

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
        raise HTTPException(
            status_code=404,
            detail="Referrer email does not exist",
        )

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
        expiration: int = Body(..., ge=1, example="7", description="days"),
        user=Depends(fastapi_users.current_user(active=True)),
        repository: RefRepository = Depends(get_ref_repository(get_async_session)),
):
    if user.referral_code:
        raise HTTPException(
            status_code=418,
            detail=f"A code already exist ({user.referral_code} -"
                   f" expires {user.referral_code_expiration})")

    code_exists = await repository.get_id_by_code(code)
    if code_exists:
        raise HTTPException(
            status_code=403,
            detail="The code already exist. Use another one"
        )

    await repository.create_code_for_user_by_id(user.id, code, expiration)

    return JSONResponse(
        content={
            "code": code,
            "expiration": expiration,
        },
        status_code=200
    )


@router.delete("/delete_code")
async def delete_code(
        user=Depends(fastapi_users.current_user(active=True)),
        repository: RefRepository = Depends(get_ref_repository(get_async_session)),
):
    if not user.referral_code:
        raise HTTPException(status_code=418, detail="The code does not exist")

    await repository.delete_code_for_user_by_id(user.id)

    return Response(status_code=200)
