# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: common.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'common.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x63ommon.proto\x12\x06\x63ommon\"\x1c\n\x0bVectorClock\x12\r\n\x05\x63lock\x18\x01 \x03(\x05\"\x10\n\x0ePrepareRequest\" \n\x0fPrepareResponse\x12\r\n\x05ready\x18\x01 \x01(\x08\"\x0f\n\rCommitRequest\"!\n\x0e\x43ommitResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x0e\n\x0c\x41\x62ortRequest\" \n\rAbortResponse\x12\x0f\n\x07\x61\x62orted\x18\x01 \x01(\x08\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_VECTORCLOCK']._serialized_start=24
  _globals['_VECTORCLOCK']._serialized_end=52
  _globals['_PREPAREREQUEST']._serialized_start=54
  _globals['_PREPAREREQUEST']._serialized_end=70
  _globals['_PREPARERESPONSE']._serialized_start=72
  _globals['_PREPARERESPONSE']._serialized_end=104
  _globals['_COMMITREQUEST']._serialized_start=106
  _globals['_COMMITREQUEST']._serialized_end=121
  _globals['_COMMITRESPONSE']._serialized_start=123
  _globals['_COMMITRESPONSE']._serialized_end=156
  _globals['_ABORTREQUEST']._serialized_start=158
  _globals['_ABORTREQUEST']._serialized_end=172
  _globals['_ABORTRESPONSE']._serialized_start=174
  _globals['_ABORTRESPONSE']._serialized_end=206
# @@protoc_insertion_point(module_scope)
