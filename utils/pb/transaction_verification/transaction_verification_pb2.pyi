from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VerificationRequest(_message.Message):
    __slots__ = ("order_data",)
    ORDER_DATA_FIELD_NUMBER: _ClassVar[int]
    order_data: str
    def __init__(self, order_data: _Optional[str] = ...) -> None: ...

class VerificationResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...
