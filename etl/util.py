#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import sys
import zipfile

import numpy as np

import etl.constants as constants
from etl.errors import InvalidFilePath, PathExists


def normalize(x: np.array) -> np.array:
    for i in x:
        i[i > 0] = 1
        i[i <= 0] = 0
    return x


def filter_by_value(x: np.array, key: int) -> np.array:
    for i in x:
        i[i == key] = 1
        i[i != key] = 0
    return x


def sum_x(x) -> np.array:
    i = 0
    res = 0
    while i < len(x):
        res += x[i]
        i += 1
    return res


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()


def write_to_json(result: dict, path: str) -> None:
    if os.path.isfile(path):
        raise PathExists(f"{path} already exists.")
    json_str = json.dumps(result, default=np_encoder)
    try:
        with open(path, "w") as fp:
            fp.write(json_str)
        get_logger().info(f"Results are written to {path}.")
    except Exception as e:
        raise e


def unpack_zipfile(src_path: str, dest_path: str) -> str:
    if not os.path.exists(src_path):
        raise InvalidFilePath(f"File {src_path} does not exist.")
    target_path = os.path.join(dest_path, constants.RAW_DATA_LOCATION)
    get_logger().info(
        f"Starting extracting data from {src_path} to {dest_path}"
    )
    with zipfile.ZipFile(src_path, "r") as zip_ref:
        dirs = list(
            set(
                [
                    os.path.dirname(x)
                    for x in zip_ref.namelist()
                    if not os.path.dirname(x).startswith("__MACOSX")
                ]
            )
        )
        zip_ref.extractall(target_path)
        return target_path


def create_dir(path: str, dirname: str) -> str:
    outdir_path = os.path.join(path, dirname)
    if os.path.isdir(outdir_path):
        raise (PathExists(f"directory {outdir_path} already exists."))
    os.mkdir(outdir_path)
    return outdir_path


def get_logger(
    name: str = __name__, log_level: int = logging.INFO
) -> logging.Logger:
    # Set up default logging for submodules to use STDOUT
    logger = logging.getLogger(name)
    fmt = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)

    return logger
