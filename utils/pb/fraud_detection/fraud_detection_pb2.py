# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fraud_detection.proto
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
    'fraud_detection.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2
import order_pb2 as order__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66raud_detection.proto\x12\x0f\x66raud_detection\x1a\x0c\x63ommon.proto\x1a\x0border.proto\"K\n\x0c\x46raudRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12)\n\x0cvector_clock\x18\x02 \x01(\x0b\x32\x13.common.VectorClock\"I\n\rFraudResponse\x12\r\n\x05\x66raud\x18\x01 \x01(\t\x12)\n\x0cvector_clock\x18\x02 \x01(\x0b\x32\x13.common.VectorClock\"8\n\x10InitFraudRequest\x12$\n\norder_data\x18\x01 \x01(\x0b\x32\x10.order.OrderData\"#\n\x11InitFraudResponse\x12\x0e\n\x06status\x18\x01 \x01(\t2\xb3\x01\n\x0e\x46raudDetection\x12M\n\x0cLookforFraud\x12\x1d.fraud_detection.FraudRequest\x1a\x1e.fraud_detection.FraudResponse\x12R\n\tInitOrder\x12!.fraud_detection.InitFraudRequest\x1a\".fraud_detection.InitFraudResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fraud_detection_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FRAUDREQUEST']._serialized_start=69
  _globals['_FRAUDREQUEST']._serialized_end=144
  _globals['_FRAUDRESPONSE']._serialized_start=146
  _globals['_FRAUDRESPONSE']._serialized_end=219
  _globals['_INITFRAUDREQUEST']._serialized_start=221
  _globals['_INITFRAUDREQUEST']._serialized_end=277
  _globals['_INITFRAUDRESPONSE']._serialized_start=279
  _globals['_INITFRAUDRESPONSE']._serialized_end=314
  _globals['_FRAUDDETECTION']._serialized_start=317
  _globals['_FRAUDDETECTION']._serialized_end=496
# @@protoc_insertion_point(module_scope)
