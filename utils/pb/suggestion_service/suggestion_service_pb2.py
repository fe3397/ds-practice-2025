# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: suggestion_service.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18suggestion_service.proto\x12\x12suggestion_service\"3\n\x11SuggestionRequest\x12\x0e\n\x06\x62ook_1\x18\x01 \x01(\t\x12\x0e\n\x06\x62ook_2\x18\x02 \x01(\t\"<\n\x12SuggestionResponse\x12\x12\n\nsug_book_1\x18\x01 \x01(\t\x12\x12\n\nsug_book_2\x18\x02 \x01(\t2m\n\nSuggestion\x12_\n\x0eMakeSuggestion\x12%.suggestion_service.SuggestionRequest\x1a&.suggestion_service.SuggestionResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'suggestion_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SUGGESTIONREQUEST']._serialized_start=48
  _globals['_SUGGESTIONREQUEST']._serialized_end=99
  _globals['_SUGGESTIONRESPONSE']._serialized_start=101
  _globals['_SUGGESTIONRESPONSE']._serialized_end=161
  _globals['_SUGGESTION']._serialized_start=163
  _globals['_SUGGESTION']._serialized_end=272
# @@protoc_insertion_point(module_scope)
