from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VerificationRequest(_message.Message):
    __slots__ = ("order_data",)
    ORDER_DATA_FIELD_NUMBER: _ClassVar[int]
    order_data: OrderData
    def __init__(self, order_data: _Optional[_Union[OrderData, _Mapping]] = ...) -> None: ...

class VerificationResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...

class OrderData(_message.Message):
    __slots__ = ("id", "userdata", "carddata", "useradress", "books")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    CARDDATA_FIELD_NUMBER: _ClassVar[int]
    USERADRESS_FIELD_NUMBER: _ClassVar[int]
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    id: str
    userdata: UserData
    carddata: CardData
    useradress: UserAdress
    books: _containers.RepeatedCompositeFieldContainer[Book]
    def __init__(self, id: _Optional[str] = ..., userdata: _Optional[_Union[UserData, _Mapping]] = ..., carddata: _Optional[_Union[CardData, _Mapping]] = ..., useradress: _Optional[_Union[UserAdress, _Mapping]] = ..., books: _Optional[_Iterable[_Union[Book, _Mapping]]] = ...) -> None: ...

class UserData(_message.Message):
    __slots__ = ("name", "contact")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    name: str
    contact: str
    def __init__(self, name: _Optional[str] = ..., contact: _Optional[str] = ...) -> None: ...

class CardData(_message.Message):
    __slots__ = ("card_number", "expiration", "cvv")
    CARD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    card_number: str
    expiration: str
    cvv: str
    def __init__(self, card_number: _Optional[str] = ..., expiration: _Optional[str] = ..., cvv: _Optional[str] = ...) -> None: ...

class UserAdress(_message.Message):
    __slots__ = ("street", "city", "state", "zip", "country")
    STREET_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ZIP_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    street: str
    city: str
    state: str
    zip: str
    country: str
    def __init__(self, street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zip: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class Book(_message.Message):
    __slots__ = ("name", "amount")
    NAME_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    amount: int
    def __init__(self, name: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...
