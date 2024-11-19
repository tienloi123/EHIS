from fastapi import APIRouter

from app.apis.endpoints import (auth_routes, opa_routes, appointment_routes,
                                notification_routes, medical_record_routes, lab_test_routes,medical_record_doctor_routes)

main_router = APIRouter()
main_router.include_router(opa_routes, prefix="/opa", tags=["opa"])
main_router.include_router(auth_routes, prefix="/auth", tags=["auth"])
main_router.include_router(appointment_routes, prefix="/appointment", tags=["appointment"])
main_router.include_router(notification_routes, prefix="/notification", tags=["notification"])
main_router.include_router(medical_record_routes, prefix="/medical-record", tags=["medical-record"])
main_router.include_router(medical_record_doctor_routes, prefix="/medical-record-doctor", tags=["medical-record-doctor"])
main_router.include_router(lab_test_routes, prefix="/lab-test", tags=["lab-test"])

