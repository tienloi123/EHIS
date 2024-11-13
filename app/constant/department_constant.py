from enum import Enum

class DepartmentEnum(str, Enum):
    KHOA_NOI = "Khoa Nội"
    KHOA_NGOAI = "Khoa Ngoại"
    KHOA_SAN = "Khoa Sản"
    KHOA_NHI = "Khoa Nhi"
    KHOA_DA_LIEU = "Khoa Da Liễu"
    KHOA_MAT = "Khoa Mắt"
    KHOA_TAI_MUI_HONG = "Khoa Tai Mũi Họng"
    KHOA_RANG_HAM_MAT = "Khoa Răng Hàm Mặt"
    KHOA_CHAN_DOAN_HINH_ANH = "Khoa Chẩn Đoán Hình Ảnh"
    KHOA_CAP_CUU = "Khoa Cấp Cứu"
