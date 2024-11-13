from enum import Enum
from starlette import status


class AppStatus(Enum):
    SUCCESS = status.HTTP_200_OK, 'SUCCESS', 'Thành công!'

    ERROR_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST, 'BAD_REQUEST', 'Yêu cầu không hợp lệ.'
    ERROR_400_USER_ALREADY_EXISTS = status.HTTP_400_BAD_REQUEST, 'BAD_REQUEST', 'Người dùng đã tồn tại.'
    ERROR_400_INVALID_USERNAME_PASSWORD = status.HTTP_400_BAD_REQUEST, 'INVALID_USERNAME_PASSWORD', ('Mật khẩu '
                                                                                                     'không hợp lệ.')
    ERROR_400_INVALID_URL = status.HTTP_400_BAD_REQUEST, 'INVALID_URL', 'Đường dẫn chứa các ký tự không được hỗ trợ.'
    ERROR_400_INVALID_TOKEN = status.HTTP_400_BAD_REQUEST, 'INVALID_TOKEN', 'Mã truy cập không hợp lệ.'
    ERROR_400_INVALID_OBJECT_ID = status.HTTP_400_BAD_REQUEST, 'INVALID_OBJECT_ID', '{description} không phải là một ObjectId hợp lệ.'
    ERROR_400_INVALID_DATA = status.HTTP_400_BAD_REQUEST, 'INVALID_DATA', 'Dữ liệu vào không hợp lệ: {description}'
    ERROR_400_NOTHING_TO_UPDATE = status.HTTP_400_BAD_REQUEST, 'NOTHING_TO_UPDATE', 'Không có gì để cập nhật'

    HTTP_401_USER_NOT_ACTIVE = status.HTTP_401_UNAUTHORIZED, 'UNAUTHORIZED', 'Người dùng chưa được kích hoạt.'
    ERROR_401_EXPIRED_TOKEN = status.HTTP_401_UNAUTHORIZED, 'EXPIRED TOKEN', 'Mã truy cập đã hết hạn.'

    ERROR_403_FORBIDDEN = status.HTTP_403_FORBIDDEN, 'FORBIDDEN', 'Bạn không được phép thực hiện hành động này.'

    ERROR_404_NOT_FOUND = status.HTTP_404_NOT_FOUND, 'NOT_FOUND', ('Không tìm thấy tài nguyên yêu cầu. Vui lòng đảm '
                                                                   'bảo rằng URL hoặc yêu cầu là chính xác và tương '
                                                                   'ứng với một tài nguyên hiện có trong hệ thống của '
                                                                   'chúng tôi. Nếu bạn tin rằng đây là lỗi, '
                                                                   'xin vui lòng liên hệ với đội hỗ trợ của chúng tôi '
                                                                   'để được hỗ trợ thêm. Chúng tôi xin lỗi vì bất kỳ '
                                                                   'sự bất tiện nào.')
    ERROR_404_USER_NOT_FOUND = status.HTTP_404_NOT_FOUND, 'NOT_FOUND', 'Email không hợp lệ.'
    ERROR_404_MEETING_NOT_FOUND = status.HTTP_404_NOT_FOUND, 'NOT_FOUND', 'Không tìm thấy cuộc họp.'
    ERROR_404_ATTENDANCE_NOT_FOUND = status.HTTP_404_NOT_FOUND, 'NOT_FOUND', 'Không tìm thấy danh sách tham dự.'
    ERROR_404_NOTIFICATION_NOT_FOUND = status.HTTP_404_NOT_FOUND, 'NOT_FOUND', 'Không tìm thấy thông báo với ID: {description}'

    ERROR_405_METHOD_NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED, 'METHOD_NOT_ALLOWED', ('Bạn không được phép '
                                                                                              'thực hiện hành động '
                                                                                              'này.')
    ERROR_405_METHOD_NOT_ALLOWED_BY_OPA = status.HTTP_405_METHOD_NOT_ALLOWED, 'METHOD_NOT_ALLOWED', ('Bạn không được '
                                                                                                     'phép thực hiện '
                                                                                                     'hành động này '
                                                                                                     'do:\n{'
                                                                                                     'description}')

    ERROR_500_INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR, 'INTERNAL_SERVER_ERROR', ('Đã xảy ra lỗi '
                                                                                                       'máy chủ nội '
                                                                                                       'bộ. Đây là '
                                                                                                       'vấn đề từ '
                                                                                                       'phía chúng '
                                                                                                       'tôi, '
                                                                                                       'và chúng tôi '
                                                                                                       'đang tích cực '
                                                                                                       'làm việc để '
                                                                                                       'giải quyết '
                                                                                                       'nó. Chúng tôi '
                                                                                                       'xin lỗi vì '
                                                                                                       'bất kỳ sự bất '
                                                                                                       'tiện nào điều '
                                                                                                       'này có thể đã '
                                                                                                       'gây ra. Nếu '
                                                                                                       'bạn cần hỗ '
                                                                                                       'trợ ngay lập '
                                                                                                       'tức hoặc có '
                                                                                                       'bất kỳ câu '
                                                                                                       'hỏi nào, '
                                                                                                       'xin vui lòng '
                                                                                                       'liên hệ với '
                                                                                                       'đội hỗ trợ '
                                                                                                       'của chúng '
                                                                                                       'tôi, '
                                                                                                       'và họ sẽ hỗ '
                                                                                                       'trợ bạn giải '
                                                                                                       'quyết vấn đề. '
                                                                                                       'Cảm ơn bạn đã '
                                                                                                       'kiên nhẫn.')

    @property
    def status_code(self):
        return self.value[0]

    @property
    def name(self):
        return self.value[1]

    @property
    def message(self):
        return self.value[2]
