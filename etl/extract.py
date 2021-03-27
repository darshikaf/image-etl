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
import etl.constants as constants

from etl.errors import InvalidAttributeManifest, InvalidInputData


class DataBunch(object):
    def __init__(self, src_path, dest_path, extracted_path, unified_path):
        self.src_path = src_path
        self.dest_path = dest_path
        self.extracted_path = extracted_path
        self.path_to_move = unified_path

    def execute(self):
        df = self._get_attribute_manifest(
            os.path.join(
                self.extracted_path,
                f"{constants.EXTRACTED_DIR_NAME}/{constants.ATTRIBUTE_MANIFEST}",
            )
        )
        df.to_csv(
            os.path.join(self.path_to_move, constants.ATTRIBUTE_MANIFEST)
        )
        comp_key = df["composite_key"].unique()

        utils.get_logger().info("Collating unique data.")
        self._create_unique_location(comp_key)

        utils.get_logger().info("Unifying data for unique location and date.")
        self._create_unified_location_sources(
            os.path.join(self.extracted_path, constants.UNIQUE_LOCATION_DIR),
            df,
        )

    def _get_attribute_manifest(self, path: str) -> pd.DataFrame:
        if not os.path.isfile(path):
            raise InvalidInputData(
                "Input data should contain one manifest file."
            )
        df = pd.read_csv(path)
        if not "loc_id" and "date" in df.columns:
            raise InvalidAttributeManifest(f"Missingloc_id and date in {path}")
        df["composite_key"] = df.apply(
            lambda x: f"{x['loc_id']}_{x['date']}", axis=1
        )
        return df

    def _create_unique_location(self, comp_key) -> None:
        for i in comp_key:
            archivelist = sorted(
                Path(self.extracted_path).glob(f"**/*{i}.tar.gz")
            )
            for x in archivelist:
                dest = os.path.basename(os.path.splitext(x)[0]).split(".")[0]
                tar = tarfile.open(x)
                for member in tar.getmembers():
                    if member.isreg():  # skip if the TarInfo is not files
                        member.name = os.path.basename(
                            member.name
                        )  # remove the path by reset it
                        tar.extract(
                            member,
                            os.path.join(
                                f"{self.extracted_path}/{constants.UNIQUE_LOCATION_DIR}",
                                dest,
                            ),
                        )  # extract

    def _create_unified_location_sources(
        self, input_path: str, df: pd.DataFrame
    ) -> None:
        file_locs = glob.glob(f"{input_path}/*/")
        if file_locs is None:
            raise InvalidInputData("Image Data not found.")
        for path in file_locs:
            files = [
                f
                for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))
            ]
            if not len(files) == 2:
                continue
            for file in files:
                if os.path.splitext(file)[1] not in ["jpg", "h5"]:
                    continue
                self._move_files_to_unified_location(file, path)

    def _move_files_to_unified_location(self, file: str, path: str) -> None:
        dirname_components = file.split("_")
        dirname = f"{dirname_components[1]}_{dirname_components[-1].split('.')[0]}"
        unified_loc = os.path.join(self.path_to_move, dirname)
        if not os.path.exists(unified_loc):
            Path(unified_loc).mkdir(parents=True, exist_ok=True)
            shutil.copy2(os.path.join(path, file), unified_loc)
        else:
            shutil.copy2(os.path.join(path, file), unified_loc)
