# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feature.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rfeature.proto\x12\x0e\x46\x65\x61tureService\"\x07\n\x05\x45mpty\">\n\rFeatureStruct\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0bpriority_id\x18\x03 \x01(\x04\"?\n\x0ePriorityStruct\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x63oefficient\x18\x03 \x01(\x02\"z\n\rHibrydFeature\x12\x12\n\nfeature_id\x18\x01 \x01(\x04\x12\x13\n\x0bpriority_id\x18\x02 \x01(\x04\x12\x14\n\x0c\x66\x65\x61ture_name\x18\x03 \x01(\t\x12\x15\n\rpriority_name\x18\x04 \x01(\t\x12\x13\n\x0b\x63oefficient\x18\x05 \x01(\x02\"A\n\x11HibrydFeatureList\x12,\n\x05items\x18\x01 \x03(\x0b\x32\x1d.FeatureService.HibrydFeature\"\x16\n\x08IdStruct\x12\n\n\x02id\x18\x01 \x01(\x04\"\x1a\n\nNameStruct\x12\x0c\n\x04name\x18\x01 \x01(\t2\x89\x05\n\x07\x46\x65\x61ture\x12I\n\x0b\x41\x64\x64Priority\x12\x1e.FeatureService.PriorityStruct\x1a\x18.FeatureService.IdStruct\"\x00\x12L\n\nAddFeature\x12\x1d.FeatureService.FeatureStruct\x1a\x1d.FeatureService.FeatureStruct\"\x00\x12@\n\x0b\x44\x65lPriority\x12\x18.FeatureService.IdStruct\x1a\x15.FeatureService.Empty\"\x00\x12?\n\nDelFeature\x12\x18.FeatureService.IdStruct\x1a\x15.FeatureService.Empty\"\x00\x12\x41\n\x0c\x45\x64itPriority\x12\x18.FeatureService.IdStruct\x1a\x15.FeatureService.Empty\"\x00\x12@\n\x0b\x45\x64itFeature\x12\x18.FeatureService.IdStruct\x1a\x15.FeatureService.Empty\"\x00\x12\x41\n\x03Get\x12\x15.FeatureService.Empty\x1a!.FeatureService.HibrydFeatureList\"\x00\x12J\n\x0fGetFeaturesById\x12\x18.FeatureService.IdStruct\x1a\x1d.FeatureService.HibrydFeature\x12N\n\x11GetFeaturesByName\x12\x1a.FeatureService.NameStruct\x1a\x1d.FeatureService.FeatureStructB\x0eZ\x0c\x61pi/featuresb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'feature_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\014api/features'
  _globals['_EMPTY']._serialized_start=33
  _globals['_EMPTY']._serialized_end=40
  _globals['_FEATURESTRUCT']._serialized_start=42
  _globals['_FEATURESTRUCT']._serialized_end=104
  _globals['_PRIORITYSTRUCT']._serialized_start=106
  _globals['_PRIORITYSTRUCT']._serialized_end=169
  _globals['_HIBRYDFEATURE']._serialized_start=171
  _globals['_HIBRYDFEATURE']._serialized_end=293
  _globals['_HIBRYDFEATURELIST']._serialized_start=295
  _globals['_HIBRYDFEATURELIST']._serialized_end=360
  _globals['_IDSTRUCT']._serialized_start=362
  _globals['_IDSTRUCT']._serialized_end=384
  _globals['_NAMESTRUCT']._serialized_start=386
  _globals['_NAMESTRUCT']._serialized_end=412
  _globals['_FEATURE']._serialized_start=415
  _globals['_FEATURE']._serialized_end=1064
# @@protoc_insertion_point(module_scope)
