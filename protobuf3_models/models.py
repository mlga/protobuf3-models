# -*- coding:utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Dict, Iterator, Optional, Tuple, Type, Union, cast

from google.protobuf.pyext._message import Message  # pylint: disable=no-name-in-module

from protobuf3_models.fields import Field


class _Ignore:
    # pylint: disable=too-few-public-methods
    __slots__: tuple = tuple()


@dataclass(frozen=True)
class ModelOptions:
    message_class: Type[Message]


def _filter_fields(attrs: Dict[str, Any]) -> Iterator[Tuple[str, Field]]:
    for name, attr in attrs.items():
        if isinstance(attr, Field):
            yield name, attr


class ModelMeta(type):
    def __new__(
        mcs: Type["ModelMeta"],
        name: str,
        bases: Tuple[Type],
        attrs: Dict[str, Any],
        protobuf_message: Union[None, Type[_Ignore], Type[Message]] = None,
    ) -> ModelMeta:
        if protobuf_message is _Ignore:
            return cast("ModelMeta", super().__new__(mcs, name, bases, attrs))

        if protobuf_message is None:
            raise RuntimeError(f"protobuf_message argument of class {name} must be set")

        if not issubclass(protobuf_message, Message):
            raise RuntimeError("protobuf_message must be a subclass of Protobuf message")

        # TODO: Validate fields against protobuf message definition
        attrs["protobuf_options"] = ModelOptions(
            message_class=protobuf_message,
        )

        mcs._make_fields(attrs)
        mcs._make_slots(attrs)

        cls = super().__new__(mcs, name, bases, attrs)

        return cast("ModelMeta", cls)

    @staticmethod
    def _make_fields(attrs: Dict[str, Any]) -> None:
        fields = {}

        for attr_name, attr in _filter_fields(attrs):  # type: str, Field
            fields[attr_name] = attr

        attrs["_fields"] = MappingProxyType(fields)

    @staticmethod
    def _make_slots(attrs: Dict[str, Any]) -> None:
        attrs["__slots__"] = tuple()


class Model(metaclass=ModelMeta, protobuf_message=_Ignore):
    # pylint: disable=too-few-public-methods
    __slots__ = ("_message", "_fields")

    _message: Optional[Message]
    _fields: Dict[str, Field]

    @property
    def message(self) -> Message:
        return self._message

    @property
    def fields(self) -> Dict[str, Field]:
        return self._fields
