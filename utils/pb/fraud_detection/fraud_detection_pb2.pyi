from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserData(_message.Message):
    __slots__ = ("name", "contact")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    name: str
    contact: str
    def __init__(self, name: _Optional[str] = ..., contact: _Optional[str] = ...) -> None: ...

class CreditCard(_message.Message):
    __slots__ = ("number", "expirationDate", "cvv")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    number: str
    expirationDate: str
    cvv: str
    def __init__(self, number: _Optional[str] = ..., expirationDate: _Optional[str] = ..., cvv: _Optional[str] = ...) -> None: ...

class FraudRequest(_message.Message):
    __slots__ = ("user", "cc")
    USER_FIELD_NUMBER: _ClassVar[int]
    CC_FIELD_NUMBER: _ClassVar[int]
    user: UserData
    cc: CreditCard
    def __init__(self, user: _Optional[_Union[UserData, _Mapping]] = ..., cc: _Optional[_Union[CreditCard, _Mapping]] = ...) -> None: ...

class FraudResponse(_message.Message):
    __slots__ = ("fraud",)
    FRAUD_FIELD_NUMBER: _ClassVar[int]
    fraud: bool
    def __init__(self, fraud: bool = ...) -> None: ...
