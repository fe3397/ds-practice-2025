# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: database.proto
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
    'database.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x64\x61tabase.proto\x12\x08\x64\x61tabase\"\x1c\n\x0bReadRequest\x12\r\n\x05title\x18\x01 \x01(\t\"\x1d\n\x0cReadResponse\x12\r\n\x05stock\x18\x01 \x01(\x05\"0\n\x0cWriteRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x11\n\tnew_stock\x18\x02 \x01(\x05\" \n\rWriteResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x10\n\x0ePrepareRequest\" \n\x0fPrepareResponse\x12\r\n\x05ready\x18\x01 \x01(\x08\"\x0f\n\rCommitRequest\"!\n\x0e\x43ommitResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x0e\n\x0c\x41\x62ortRequest\" \n\rAbortResponse\x12\x0f\n\x07\x61\x62orted\x18\x01 \x01(\x08\"&\n\x15\x44\x65\x63rementStockRequest\x12\r\n\x05title\x18\x01 \x01(\t\")\n\x16\x44\x65\x63rementStockResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"&\n\x15IncrementStockRequest\x12\r\n\x05title\x18\x01 \x01(\t\")\n\x16IncrementStockResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x0f\n\rIsHeadRequest\"!\n\x0eIsHeadResponse\x12\x0f\n\x07is_head\x18\x01 \x01(\x08\"\x0f\n\rIsTailRequest\"!\n\x0eIsTailResponse\x12\x0f\n\x07is_tail\x18\x01 \x01(\x08\x32\xdb\x04\n\rBooksDatabase\x12\x35\n\x04Read\x12\x15.database.ReadRequest\x1a\x16.database.ReadResponse\x12\x38\n\x05Write\x12\x16.database.WriteRequest\x1a\x17.database.WriteResponse\x12S\n\x0e\x44\x65\x63rementStock\x12\x1f.database.DecrementStockRequest\x1a .database.DecrementStockResponse\x12S\n\x0eIncrementStock\x12\x1f.database.IncrementStockRequest\x1a .database.IncrementStockResponse\x12>\n\x07Prepare\x12\x18.database.PrepareRequest\x1a\x19.database.PrepareResponse\x12;\n\x06\x43ommit\x12\x17.database.CommitRequest\x1a\x18.database.CommitResponse\x12\x38\n\x05\x41\x62ort\x12\x16.database.AbortRequest\x1a\x17.database.AbortResponse\x12;\n\x06IsHead\x12\x17.database.IsHeadRequest\x1a\x18.database.IsHeadResponse\x12;\n\x06IsTail\x12\x17.database.IsTailRequest\x1a\x18.database.IsTailResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'database_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_READREQUEST']._serialized_start=28
  _globals['_READREQUEST']._serialized_end=56
  _globals['_READRESPONSE']._serialized_start=58
  _globals['_READRESPONSE']._serialized_end=87
  _globals['_WRITEREQUEST']._serialized_start=89
  _globals['_WRITEREQUEST']._serialized_end=137
  _globals['_WRITERESPONSE']._serialized_start=139
  _globals['_WRITERESPONSE']._serialized_end=171
  _globals['_PREPAREREQUEST']._serialized_start=173
  _globals['_PREPAREREQUEST']._serialized_end=189
  _globals['_PREPARERESPONSE']._serialized_start=191
  _globals['_PREPARERESPONSE']._serialized_end=223
  _globals['_COMMITREQUEST']._serialized_start=225
  _globals['_COMMITREQUEST']._serialized_end=240
  _globals['_COMMITRESPONSE']._serialized_start=242
  _globals['_COMMITRESPONSE']._serialized_end=275
  _globals['_ABORTREQUEST']._serialized_start=277
  _globals['_ABORTREQUEST']._serialized_end=291
  _globals['_ABORTRESPONSE']._serialized_start=293
  _globals['_ABORTRESPONSE']._serialized_end=325
  _globals['_DECREMENTSTOCKREQUEST']._serialized_start=327
  _globals['_DECREMENTSTOCKREQUEST']._serialized_end=365
  _globals['_DECREMENTSTOCKRESPONSE']._serialized_start=367
  _globals['_DECREMENTSTOCKRESPONSE']._serialized_end=408
  _globals['_INCREMENTSTOCKREQUEST']._serialized_start=410
  _globals['_INCREMENTSTOCKREQUEST']._serialized_end=448
  _globals['_INCREMENTSTOCKRESPONSE']._serialized_start=450
  _globals['_INCREMENTSTOCKRESPONSE']._serialized_end=491
  _globals['_ISHEADREQUEST']._serialized_start=493
  _globals['_ISHEADREQUEST']._serialized_end=508
  _globals['_ISHEADRESPONSE']._serialized_start=510
  _globals['_ISHEADRESPONSE']._serialized_end=543
  _globals['_ISTAILREQUEST']._serialized_start=545
  _globals['_ISTAILREQUEST']._serialized_end=560
  _globals['_ISTAILRESPONSE']._serialized_start=562
  _globals['_ISTAILRESPONSE']._serialized_end=595
  _globals['_BOOKSDATABASE']._serialized_start=598
  _globals['_BOOKSDATABASE']._serialized_end=1201
# @@protoc_insertion_point(module_scope)
