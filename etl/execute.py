#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from dataclasses import dataclass
from typing import Dict

import etl.constants as constants
import etl.util as utils

from etl.extract import DataBunch
from etl.transform import Transform

@dataclass
class Configuration():
    src_path: str
    dest_path: str


class Executor(object):
    def __init__(self, config: Configuration) -> None:
        self.src_path = config.src_path
        self.dest_path = config.dest_path
        self.extracted_path = utils.unpack_zipfile(self.src_path, self.dest_path)
        self.unified_path = utils.create_dir(self.dest_path, constants.UNIFIED_LOCATION)

    def execute(self):
        db = DataBunch(
            src_path=self.src_path,
            dest_path=self.dest_path,
            extracted_path=self.extracted_path,
            unified_path=self.unified_path,
        )
        utils.get_logger().info("Starting Data Extraction.")
        try:
            db.execute()
        except Exception as e:
            raise e

        utils.get_logger().info("Starting tranformation actions.")
        try:
            tf = Transform(
                src_path=self.unified_path, dest_path=self.unified_path
            )
            result = tf.execute()
        except Exception as e:
            raise e

        utils.write_to_json(result, f"{self.unified_path}/result.json")
