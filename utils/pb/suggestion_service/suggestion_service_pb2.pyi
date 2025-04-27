import common_pb2 as _common_pb2
import order_pb2 as _order_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SuggestionRequest(_message.Message):
    __slots__ = ("order_id",)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    def __init__(self, order_id: _Optional[str] = ...) -> None: ...

class SuggestionResponse(_message.Message):
    __slots__ = ("sug_book_1", "sug_book_2", "vector_clock")
    SUG_BOOK_1_FIELD_NUMBER: _ClassVar[int]
    SUG_BOOK_2_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    sug_book_1: str
    sug_book_2: str
    vector_clock: _common_pb2.VectorClock
    def __init__(self, sug_book_1: _Optional[str] = ..., sug_book_2: _Optional[str] = ..., vector_clock: _Optional[_Union[_common_pb2.VectorClock, _Mapping]] = ...) -> None: ...

class InitSuggestionRequest(_message.Message):
    __slots__ = ("order_data",)
    ORDER_DATA_FIELD_NUMBER: _ClassVar[int]
    order_data: _order_pb2.OrderData
    def __init__(self, order_data: _Optional[_Union[_order_pb2.OrderData, _Mapping]] = ...) -> None: ...

class InitSuggestionResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
