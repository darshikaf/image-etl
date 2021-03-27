#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

import tests.helpers as helpers

from etl.errors import InvalidFilePath, InvalidInputData
from etl.execute import Executor
from etl.extract import DataBunch


def test_invalid_source_path():
    with pytest.raises(InvalidFilePath):
        executor = Executor(helpers.invalid_config())

    helpers.clean_up()


def test_missing_manifest_file():
    with pytest.raises(InvalidInputData):
        helpers.create_databunch_with_missing_manifest().execute()
    helpers.clean_up()


def test_only_manifest_in_data():
    with pytest.raises(InvalidInputData):
        helpers.create_databunch_with_only_manifest().execute()
    helpers.clean_up
