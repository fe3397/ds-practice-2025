# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0border.proto\x12\x05order\"\xa0\x01\n\tOrderData\x12\n\n\x02id\x18\x01 \x01(\t\x12!\n\x08userdata\x18\x02 \x01(\x0b\x32\x0f.order.UserData\x12!\n\x08\x63\x61rddata\x18\x03 \x01(\x0b\x32\x0f.order.CardData\x12%\n\nuseradress\x18\x04 \x01(\x0b\x32\x11.order.UserAdress\x12\x1a\n\x05\x62ooks\x18\x05 \x03(\x0b\x32\x0b.order.Book\")\n\x08UserData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\"@\n\x08\x43\x61rdData\x12\x13\n\x0b\x63\x61rd_number\x18\x01 \x01(\t\x12\x12\n\nexpiration\x18\x02 \x01(\t\x12\x0b\n\x03\x63vv\x18\x03 \x01(\t\"W\n\nUserAdress\x12\x0e\n\x06street\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0b\n\x03zip\x18\x04 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x05 \x01(\t\"$\n\x04\x42ook\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ORDERDATA']._serialized_start=23
  _globals['_ORDERDATA']._serialized_end=183
  _globals['_USERDATA']._serialized_start=185
  _globals['_USERDATA']._serialized_end=226
  _globals['_CARDDATA']._serialized_start=228
  _globals['_CARDDATA']._serialized_end=292
  _globals['_USERADRESS']._serialized_start=294
  _globals['_USERADRESS']._serialized_end=381
  _globals['_BOOK']._serialized_start=383
  _globals['_BOOK']._serialized_end=419
# @@protoc_insertion_point(module_scope)
