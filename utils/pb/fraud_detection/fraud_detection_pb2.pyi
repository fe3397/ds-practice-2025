import common_pb2 as _common_pb2
import order_pb2 as _order_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FraudRequest(_message.Message):
    __slots__ = ("order_id",)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    def __init__(self, order_id: _Optional[str] = ...) -> None: ...

class FraudResponse(_message.Message):
    __slots__ = ("fraud", "vector_clock")
    FRAUD_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    fraud: bool
    vector_clock: _common_pb2.VectorClock
    def __init__(self, fraud: bool = ..., vector_clock: _Optional[_Union[_common_pb2.VectorClock, _Mapping]] = ...) -> None: ...

class InitFraudRequest(_message.Message):
    __slots__ = ("order_data",)
    ORDER_DATA_FIELD_NUMBER: _ClassVar[int]
    order_data: _order_pb2.OrderData
    def __init__(self, order_data: _Optional[_Union[_order_pb2.OrderData, _Mapping]] = ...) -> None: ...

class InitFraudResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
