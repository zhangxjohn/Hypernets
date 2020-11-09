# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hypernets/dispatchers/cluster/grpc/proto/spec.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hypernets/dispatchers/cluster/grpc/proto/spec.proto',
  package='hypernets.dispatchers.cluster.grpc.proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n3hypernets/dispatchers/cluster/grpc/proto/spec.proto\x12(hypernets.dispatchers.cluster.grpc.proto\"\x1e\n\x0bPingMessage\x12\x0f\n\x07message\x18\x01 \x01(\t\"x\n\rSearchRequest\x12\x11\n\tsearch_id\x18\x01 \x01(\t\x12\x10\n\x08trail_no\x18\x02 \x01(\t\x12\x10\n\x08space_id\x18\x03 \x01(\t\x12\x0f\n\x07success\x18\x04 \x01(\x08\x12\x0e\n\x06reward\x18\x05 \x01(\x02\x12\x0f\n\x07message\x18\x06 \x01(\t\"\x8f\x02\n\x0eSearchResponse\x12Y\n\x04\x63ode\x18\x01 \x01(\x0e\x32K.hypernets.dispatchers.cluster.grpc.proto.SearchResponse.SearchResponseCode\x12\x11\n\tsearch_id\x18\x02 \x01(\t\x12\x10\n\x08trail_no\x18\x03 \x01(\t\x12\x10\n\x08space_id\x18\x04 \x01(\t\x12\x12\n\nspace_file\x18\x05 \x01(\t\x12\x12\n\nmodel_file\x18\x06 \x01(\t\"C\n\x12SearchResponseCode\x12\x06\n\x02OK\x10\x00\x12\x0b\n\x07WAITING\x10\x0b\x12\x0c\n\x08\x46INISHED\x10\x0c\x12\n\n\x06\x46\x41ILED\x10\x63\x32\x8a\x02\n\x0cSearchDriver\x12v\n\x04ping\x12\x35.hypernets.dispatchers.cluster.grpc.proto.PingMessage\x1a\x35.hypernets.dispatchers.cluster.grpc.proto.PingMessage\"\x00\x12\x81\x01\n\x06search\x12\x37.hypernets.dispatchers.cluster.grpc.proto.SearchRequest\x1a\x38.hypernets.dispatchers.cluster.grpc.proto.SearchResponse\"\x00(\x01\x30\x01\x62\x06proto3')
)



_SEARCHRESPONSE_SEARCHRESPONSECODE = _descriptor.EnumDescriptor(
  name='SearchResponseCode',
  full_name='hypernets.dispatchers.cluster.grpc.proto.SearchResponse.SearchResponseCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WAITING', index=1, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FINISHED', index=2, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAILED', index=3, number=99,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=456,
  serialized_end=523,
)
_sym_db.RegisterEnumDescriptor(_SEARCHRESPONSE_SEARCHRESPONSECODE)


_PINGMESSAGE = _descriptor.Descriptor(
  name='PingMessage',
  full_name='hypernets.dispatchers.cluster.grpc.proto.PingMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='hypernets.dispatchers.cluster.grpc.proto.PingMessage.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=97,
  serialized_end=127,
)


_SEARCHREQUEST = _descriptor.Descriptor(
  name='SearchRequest',
  full_name='hypernets.dispatchers.cluster.grpc.proto.SearchRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='search_id', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchRequest.search_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trail_no', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchRequest.trail_no', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='space_id', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchRequest.space_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='success', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchRequest.success', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reward', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchRequest.reward', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchRequest.message', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=129,
  serialized_end=249,
)


_SEARCHRESPONSE = _descriptor.Descriptor(
  name='SearchResponse',
  full_name='hypernets.dispatchers.cluster.grpc.proto.SearchResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchResponse.code', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='search_id', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchResponse.search_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trail_no', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchResponse.trail_no', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='space_id', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchResponse.space_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='space_file', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchResponse.space_file', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='model_file', full_name='hypernets.dispatchers.cluster.grpc.proto.SearchResponse.model_file', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SEARCHRESPONSE_SEARCHRESPONSECODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=252,
  serialized_end=523,
)

_SEARCHRESPONSE.fields_by_name['code'].enum_type = _SEARCHRESPONSE_SEARCHRESPONSECODE
_SEARCHRESPONSE_SEARCHRESPONSECODE.containing_type = _SEARCHRESPONSE
DESCRIPTOR.message_types_by_name['PingMessage'] = _PINGMESSAGE
DESCRIPTOR.message_types_by_name['SearchRequest'] = _SEARCHREQUEST
DESCRIPTOR.message_types_by_name['SearchResponse'] = _SEARCHRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PingMessage = _reflection.GeneratedProtocolMessageType('PingMessage', (_message.Message,), {
  'DESCRIPTOR' : _PINGMESSAGE,
  '__module__' : 'hypernets.dispatchers.cluster.grpc.proto.spec_pb2'
  # @@protoc_insertion_point(class_scope:hypernets.dispatchers.cluster.grpc.proto.PingMessage)
  })
_sym_db.RegisterMessage(PingMessage)

SearchRequest = _reflection.GeneratedProtocolMessageType('SearchRequest', (_message.Message,), {
  'DESCRIPTOR' : _SEARCHREQUEST,
  '__module__' : 'hypernets.dispatchers.cluster.grpc.proto.spec_pb2'
  # @@protoc_insertion_point(class_scope:hypernets.dispatchers.cluster.grpc.proto.SearchRequest)
  })
_sym_db.RegisterMessage(SearchRequest)

SearchResponse = _reflection.GeneratedProtocolMessageType('SearchResponse', (_message.Message,), {
  'DESCRIPTOR' : _SEARCHRESPONSE,
  '__module__' : 'hypernets.dispatchers.cluster.grpc.proto.spec_pb2'
  # @@protoc_insertion_point(class_scope:hypernets.dispatchers.cluster.grpc.proto.SearchResponse)
  })
_sym_db.RegisterMessage(SearchResponse)



_SEARCHDRIVER = _descriptor.ServiceDescriptor(
  name='SearchDriver',
  full_name='hypernets.dispatchers.cluster.grpc.proto.SearchDriver',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=526,
  serialized_end=792,
  methods=[
  _descriptor.MethodDescriptor(
    name='ping',
    full_name='hypernets.dispatchers.cluster.grpc.proto.SearchDriver.ping',
    index=0,
    containing_service=None,
    input_type=_PINGMESSAGE,
    output_type=_PINGMESSAGE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='search',
    full_name='hypernets.dispatchers.cluster.grpc.proto.SearchDriver.search',
    index=1,
    containing_service=None,
    input_type=_SEARCHREQUEST,
    output_type=_SEARCHRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SEARCHDRIVER)

DESCRIPTOR.services_by_name['SearchDriver'] = _SEARCHDRIVER

# @@protoc_insertion_point(module_scope)