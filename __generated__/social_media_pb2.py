# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: social_media.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12social_media.proto\x12\x0csocial_media\x1a\x1fgoogle/protobuf/timestamp.proto\"!\n\x0eGetUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"\x91\x01\n\x04User\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12-\n\tjoin_date\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1b\n\x13profile_picture_url\x18\x05 \x01(\t\x12\x0b\n\x03\x62io\x18\x06 \x01(\t\"P\n\x0fGetUserResponse\x12\r\n\x05\x66ound\x18\x01 \x01(\x08\x12%\n\x04user\x18\x02 \x01(\x0b\x32\x12.social_media.UserH\x00\x88\x01\x01\x42\x07\n\x05_user2W\n\x0bSocialMedia\x12H\n\x07GetUser\x12\x1c.social_media.GetUserRequest\x1a\x1d.social_media.GetUserResponse\"\x00\x42\x06\xa2\x02\x03RTGb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'social_media_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\242\002\003RTG'
  _globals['_GETUSERREQUEST']._serialized_start=69
  _globals['_GETUSERREQUEST']._serialized_end=102
  _globals['_USER']._serialized_start=105
  _globals['_USER']._serialized_end=250
  _globals['_GETUSERRESPONSE']._serialized_start=252
  _globals['_GETUSERRESPONSE']._serialized_end=332
  _globals['_SOCIALMEDIA']._serialized_start=334
  _globals['_SOCIALMEDIA']._serialized_end=421
# @@protoc_insertion_point(module_scope)
