from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Modality(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODALITY_UNSPECIFIED: _ClassVar[Modality]
    MODALITY_IMAGE: _ClassVar[Modality]
    MODALITY_VIDEO: _ClassVar[Modality]
    MODALITY_AUDIO: _ClassVar[Modality]

class MediaSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEDIA_SOURCE_TYPE_UNSPECIFIED: _ClassVar[MediaSourceType]
    MEDIA_SOURCE_TYPE_URL: _ClassVar[MediaSourceType]
    MEDIA_SOURCE_TYPE_DATA_URI: _ClassVar[MediaSourceType]
    MEDIA_SOURCE_TYPE_RAW_BYTES: _ClassVar[MediaSourceType]

class TaskInputType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TASK_INPUT_TYPE_UNSPECIFIED: _ClassVar[TaskInputType]
    TASK_INPUT_TYPE_TEXT: _ClassVar[TaskInputType]
    TASK_INPUT_TYPE_TOKEN_IDS: _ClassVar[TaskInputType]
    TASK_INPUT_TYPE_MULTIMODAL: _ClassVar[TaskInputType]
MODALITY_UNSPECIFIED: Modality
MODALITY_IMAGE: Modality
MODALITY_VIDEO: Modality
MODALITY_AUDIO: Modality
MEDIA_SOURCE_TYPE_UNSPECIFIED: MediaSourceType
MEDIA_SOURCE_TYPE_URL: MediaSourceType
MEDIA_SOURCE_TYPE_DATA_URI: MediaSourceType
MEDIA_SOURCE_TYPE_RAW_BYTES: MediaSourceType
TASK_INPUT_TYPE_UNSPECIFIED: TaskInputType
TASK_INPUT_TYPE_TEXT: TaskInputType
TASK_INPUT_TYPE_TOKEN_IDS: TaskInputType
TASK_INPUT_TYPE_MULTIMODAL: TaskInputType

class TokenIds(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ids: _Optional[_Iterable[int]] = ...) -> None: ...

class MediaItem(_message.Message):
    __slots__ = ("modality", "url", "data_uri", "raw_bytes", "mime_type", "uuid")
    MODALITY_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DATA_URI_FIELD_NUMBER: _ClassVar[int]
    RAW_BYTES_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    modality: Modality
    url: str
    data_uri: str
    raw_bytes: bytes
    mime_type: str
    uuid: str
    def __init__(self, modality: _Optional[_Union[Modality, str]] = ..., url: _Optional[str] = ..., data_uri: _Optional[str] = ..., raw_bytes: _Optional[bytes] = ..., mime_type: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class MultimodalTaskInput(_message.Message):
    __slots__ = ("text", "token_ids", "media")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    text: str
    token_ids: TokenIds
    media: _containers.RepeatedCompositeFieldContainer[MediaItem]
    def __init__(self, text: _Optional[str] = ..., token_ids: _Optional[_Union[TokenIds, _Mapping]] = ..., media: _Optional[_Iterable[_Union[MediaItem, _Mapping]]] = ...) -> None: ...

class TaskInput(_message.Message):
    __slots__ = ("item_id", "text", "token_ids", "multimodal")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    MULTIMODAL_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    text: str
    token_ids: TokenIds
    multimodal: MultimodalTaskInput
    def __init__(self, item_id: _Optional[str] = ..., text: _Optional[str] = ..., token_ids: _Optional[_Union[TokenIds, _Mapping]] = ..., multimodal: _Optional[_Union[MultimodalTaskInput, _Mapping]] = ...) -> None: ...
