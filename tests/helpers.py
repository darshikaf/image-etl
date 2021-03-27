#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

import etl.constants as constants
import etl.util as utils
from etl.execute import Configuration
from etl.extract import DataBunch


def create_databunch_with_missing_manifest():
    src_path  = "tests/data/toy_dataset/empty_data.zip",
    dest_path = outdir()
    extracted_path = "tests/data/unique"
    unified_path = "tests/data/unified"
    db = DataBunch(src_path, dest_path, extracted_path, unified_path) 
    return db

def create_databunch_with_only_manifest():
    src_path  = "tests/data/toy_dataset/only_manifest.zip",
    dest_path = outdir()
    extracted_path = "tests/data/unique"
    unified_path = "tests/data/unified"
    db = DataBunch(src_path, dest_path, extracted_path, unified_path) 
    return db

def create_config():
    src_path  = "tests/data/toy_dataset"
    dest_path = outdir()
    config = Configuration(src_path, dest_path)
    return config

def invalid_config():
    src_path = "invalid/path"
    dest_path = outdir()
    return Configuration(src_path, dest_path)

def outdir():
    return "tests/data/out"

def clean_up():
    if os.path.exists(outdir()):
        shutil.rmtree(outdir())
    extracted_files = "tests/data/toy_dataset/New_Data"
    if os.path.exists(extracted_files):
        shutil.rmtree(extracted_files)
    if os.path.exists("tests/data/unified"):
        shutil.rmtree("tests/data/unified")

