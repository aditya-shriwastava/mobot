# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gyroscope.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import common_pb2 as common__pb2
from . import imu_pb2 as imu__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gyroscope.proto',
  package='mobot',
  syntax='proto3',
  serialized_options=b'\n\020io.github.mobotxP\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0fgyroscope.proto\x12\x05mobot\x1a\x0c\x63ommon.proto\x1a\timu.proto2\x82\x01\n\tGyroscope\x12?\n\x14SetGyroscopeMetadata\x12\x15.mobot.SensorMetadata\x1a\x0e.mobot.Success\"\x00\x12\x34\n\x10NewGyroscopeData\x12\x0e.mobot.Vector3\x1a\x0e.mobot.Success\"\x00\x42\x14\n\x10io.github.mobotxP\x01\x62\x06proto3'
  ,
  dependencies=[common__pb2.DESCRIPTOR,imu__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_GYROSCOPE = _descriptor.ServiceDescriptor(
  name='Gyroscope',
  full_name='mobot.Gyroscope',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=52,
  serialized_end=182,
  methods=[
  _descriptor.MethodDescriptor(
    name='SetGyroscopeMetadata',
    full_name='mobot.Gyroscope.SetGyroscopeMetadata',
    index=0,
    containing_service=None,
    input_type=imu__pb2._SENSORMETADATA,
    output_type=common__pb2._SUCCESS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='NewGyroscopeData',
    full_name='mobot.Gyroscope.NewGyroscopeData',
    index=1,
    containing_service=None,
    input_type=common__pb2._VECTOR3,
    output_type=common__pb2._SUCCESS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_GYROSCOPE)

DESCRIPTOR.services_by_name['Gyroscope'] = _GYROSCOPE

# @@protoc_insertion_point(module_scope)