from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SuggestionRequest(_message.Message):
    __slots__ = ("book_1", "book_2")
    BOOK_1_FIELD_NUMBER: _ClassVar[int]
    BOOK_2_FIELD_NUMBER: _ClassVar[int]
    book_1: str
    book_2: str
    def __init__(self, book_1: _Optional[str] = ..., book_2: _Optional[str] = ...) -> None: ...

class SuggestionResponse(_message.Message):
    __slots__ = ("sug_book_1", "sug_book_2")
    SUG_BOOK_1_FIELD_NUMBER: _ClassVar[int]
    SUG_BOOK_2_FIELD_NUMBER: _ClassVar[int]
    sug_book_1: str
    sug_book_2: str
    def __init__(self, sug_book_1: _Optional[str] = ..., sug_book_2: _Optional[str] = ...) -> None: ...
