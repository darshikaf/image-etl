#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import logging
import os
import shutil
import sys
import tarfile
import zipfile

from pathlib import Path

import pandas as pd

import etl.util as utils

from etl.errors import InvalidAttributeManifest, InvalidInputData


ATTRIBUTE_MANIFEST = "attribute_manifest.csv"


class DataBunch(object):
    def __init__(self, src_path, dest_path):
        self.src_path = src_path
        self.dest_path = dest_path
        self.extracted_path = utils.unpack_zipfile(src_path, dest_path)
        self.path_to_move = utils.create_dir(dest_path, "unified")
        
    def execute(self):
        df = self._get_attribute_manifest(os.path.join(self.extracted_path, f"New_Data/{ATTRIBUTE_MANIFEST}"))
        comp_key = df['composite_key'].unique()
        self._create_unique_location(comp_key)
        self._create_unified_location_sources(os.path.join(self.extracted_path, "unique"), df)
        
        
    def _get_attribute_manifest(self, path: str) -> pd.DataFrame:
        if not os.path.isfile(path) :
            raise InvalidInputData("Input data should contain one manifest file.")
        df = pd.read_csv(path)
        if not 'loc_id' and 'date' in df.columns:
            raise InvalidAttributeManifest(f"Missingloc_id and date in {path}")
        df["composite_key"] = df.apply(lambda x:f"{x['loc_id']}_{x['date']}",axis=1)
        return df
    
    def _create_unique_location(self, comp_key) -> None:
        for i in comp_key:
            archivelist = sorted(Path(self.extracted_path).glob(f"**/*{i}.tar.gz"))
            for x in archivelist:
                dest = os.path.basename(os.path.splitext(x)[0]).split('.')[0]
                tar=tarfile.open(x)
                for member in tar.getmembers():
                    if member.isreg():  # skip if the TarInfo is not files
                        member.name = os.path.basename(member.name) # remove the path by reset it
                        tar.extract(member,os.path.join(f"{self.extracted_path}/unique", dest)) # extract  
                        
    def _create_unified_location_sources(self, input_path: str, df:pd.DataFrame) -> None:
        file_locs = glob.glob(f"{input_path}/*/")
        for path in file_locs:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
            for file in files:
                dirname_components = file.split("_")
                dirname = f"{dirname_components[1]}_{dirname_components[-1].split('.')[0]}"
                unified_loc = os.path.join(self.path_to_move, dirname)
                if not os.path.exists(unified_loc):
                    Path(unified_loc).mkdir(parents=True, exist_ok=True)
                    shutil.copy2(os.path.join(path,file), unified_loc)
                else:
                    shutil.copy2(os.path.join(path,file), unified_loc)
        df.to_csv(os.path.join(self.path_to_move, "attribute_manifest.csv"))




db = DataBunch(
    src_path="/Users/weerakda/workspace/CV/AI_Data_Software_Engineering_Question.zip",
    dest_path="/Users/weerakda/workspace/CV/",
)
db.execute()
