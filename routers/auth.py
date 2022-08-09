from fastapi import APIRouter, Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import schemas.auth as auth_schema
import cruds.auth as auth_crud
from lib.auth_utils import AuthJwtCsrf
from fastapi_csrf_protect import CsrfProtect


router = APIRouter(tags=["Authentication"])
auth = AuthJwtCsrf()


@router.post("/login", response_model=auth_schema.SuccessMsg)
async def login(
    res: Response,
    req: Request,
    user: auth_schema.UserBody,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncSession = Depends(get_db),
):
    csrf_token = csrf_protect.get_csrf_from_headers(req.headers)
    csrf_protect.validate_csrf(csrf_token)
    token = await auth_crud.login(db, user)

    res.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="none",
        secure=True,
    )

    return {"message": "Successfully logged-in"}


@router.post("/api/logout", response_model=auth_schema.SuccessMsg)
def logout(request: Request, response: Response, csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
    csrf_protect.validate_csrf(csrf_token)
    response.set_cookie(
        key="access_token", value="", httponly=True, samesite="none", secure=True
    )
    return {"message": "Successfully logged-out"}


@router.get("/csrftoken", response_model=auth_schema.Csrf)
async def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.generate_csrf()
    res = {"csrf_token": csrf_token}
    return res
