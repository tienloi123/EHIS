from fastapi import APIRouter

from app.apis.endpoints import (auth_routes, opa_routes, appointment_routes,
                                notification_routes, medical_record_routes, lab_test_routes,
                                medical_record_doctor_routes, payment_routes, qr_routes,user_routes, patient_routes, doctor_routes, receptionist_routes)

main_router = APIRouter()
main_router.include_router(opa_routes, prefix="/opa", tags=["opa"])
main_router.include_router(auth_routes, prefix="/auth", tags=["auth"])
main_router.include_router(appointment_routes, prefix="/appointment", tags=["appointment"])
main_router.include_router(notification_routes, prefix="/notification", tags=["notification"])
main_router.include_router(medical_record_routes, prefix="/medical-record", tags=["medical-record"])
main_router.include_router(medical_record_doctor_routes, prefix="/medical-record-doctor",
                           tags=["medical-record-doctor"])
main_router.include_router(lab_test_routes, prefix="/lab-test", tags=["lab-test"])
main_router.include_router(payment_routes, prefix="/payments", tags=["payments"])
main_router.include_router(qr_routes, prefix="/qrcode", tags=["qrcode"])
main_router.include_router(user_routes, prefix="/user", tags=["user"])
main_router.include_router(patient_routes, prefix="/patient", tags=["patient"])
main_router.include_router(doctor_routes, prefix="/doctor", tags=["doctor"])
main_router.include_router(receptionist_routes, prefix="/receptionist", tags=["receptionist"])
