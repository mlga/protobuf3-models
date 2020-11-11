# -*- coding:utf-8 -*-
from protobuf3_models.add import add


def test_dummy() -> None:
    assert 2 + 2 == 4


def test_add() -> None:
    assert add(2, 2) == 4
