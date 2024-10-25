from fastapi import APIRouter

from app.apis.endpoints import auth_routes, opa_routes, appointment_routes

main_router = APIRouter()
main_router.include_router(opa_routes, prefix="/opa", tags=["opa"])
main_router.include_router(auth_routes, prefix="/auth", tags=["auth"])
main_router.include_router(appointment_routes, prefix="/appointment", tags=["appointment"])
