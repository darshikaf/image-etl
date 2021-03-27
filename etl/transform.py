#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import json
import os
import sys

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import h5py
import numpy as np
import pandas as pd

import etl.constants as constants
import etl.util as utils

from etl.errors import InvalidInputData


@dataclass
class DataUnit:
    u_loc: str
    job_id: int
    category: int
    data: np.ndarray
    size: int


@dataclass
class DUByCategory:
    dunits: List[DataUnit]
    category: str


@dataclass
class Metadata:
    loc_id: str
    category: str
    size: set
    corner: tuple = None
    height: int = None
    width: int = None
    segmentation: List[tuple] = None

    def to_json(self):
        return {
            "loc_id": self.loc_id,
            "category": self.category,
            "size": self.size,
            "corner": self.corner,
            "height": self.height,
            "width": self.width,
            "segmentation": self.segmentation,
        }


class Transform(object):
    def __init__(self, src_path, dest_path):
        self.src_path = src_path
        self.dest_path = dest_path

    def execute(self):
        jobs = self._get_all_jobs()
        metadata = self._construct_metadata(jobs)
        df = pd.read_csv(
            os.path.join(self.src_path, constants.ATTRIBUTE_MANIFEST)
        )
        unique_dunits = self._get_dunits_by_cat_loc(jobs, df)
        final_metadata = self.produce_final_dataset(unique_dunits)
        return final_metadata

    def _get_all_jobs(self):
        jobs = {}
        unified_locations = glob.glob(os.path.join(self.src_path, "**"))
        for i in unified_locations:
            if not os.path.basename(i) == constants.ATTRIBUTE_MANIFEST:
                jobs[os.path.basename(i)] = glob.glob(f"{i}/*.h5")
        if not jobs:
            raise InvalidInputData("Annotation jobs cannot be found.")
        return jobs

    def _get_annotation_jobs(self, paths: List[str]) -> Dict:
        jobs = {}
        for i in paths:
            jobs[i] = os.path.basename(i)[0]
        return jobs

    def _construct_metadata(self, jobs: Dict) -> Dict:
        metadata = {}
        for i in jobs:
            annotations = self._get_annotation_jobs(jobs[i])
            for i in annotations:
                with h5py.File(i, "r") as f:
                    keys = list(f.keys())
                    categories_for_job = (annotations[i], keys)
                    metadata[i] = categories_for_job
        return metadata

    def _get_category(self, comp_key: str, df: pd.DataFrame):
        row = df.loc[df["composite_key"] == comp_key]
        str = list(row["classes"])[0]
        return [int(s) for s in str if s.isdigit()]

    def _get_dunits_by_cat_loc(self, jobs: Dict, df: pd.DataFrame) -> Dict:
        dunits_by_cat_loc = {}
        for u_loc in jobs:
            categories = self._get_category(u_loc, df)
            dunits = []
            for path in jobs[u_loc]:
                with h5py.File(path, "r") as f:
                    u_loc = path.split("/")[-2]
                    job_id = path.split("/")[-1].split("_")[0]
                    for i, x in enumerate(categories):
                        data = np.array(f[list(f.keys())[i]])
                        dunits.append(
                            DataUnit(
                                u_loc=u_loc,
                                job_id=job_id,
                                category=categories[i],
                                size=data.shape,
                                data=data,
                            )
                        )
            dunits_by_cat = {}
            for i in categories:
                dunits_by_cat[i] = DUByCategory(
                    dunits=[d for d in dunits if d.category == i], category=i
                )
            dunits_by_cat_loc[u_loc] = dunits_by_cat
        return dunits_by_cat_loc

    def _get_polygon_data(self, data: tuple) -> tuple:
        polygon_boundary = list(zip(data[0], data[1]))
        if polygon_boundary:
            bottom_left = polygon_boundary[0]
            bottom_right = data[-1][-1]
            top_left = data[0][-1]
            width = abs(bottom_right - bottom_left[0])
            height = abs(top_left - bottom_left[1])
        return (polygon_boundary, bottom_left, width, height)

    def produce_final_dataset(self, dunits_by_cat_loc) -> dict:
        final_metadata = {}
        for i in dunits_by_cat_loc:
            keys = list(dunits_by_cat_loc[i].keys())
            li = []
            for val in dunits_by_cat_loc[i].values():
                loc_specific_metadata = {}
                du_arr = [i.data for i in val.dunits]
                shape = (len(du_arr[0]), len(du_arr[0]))
                filtered_by_cat = utils.normalize(du_arr)
                concat_arr = utils.normalize(utils.sum_x(filtered_by_cat))
                object_detected = np.where(concat_arr == 1)
                if any(map(len, object_detected)):
                    (
                        segmentation,
                        corner,
                        width,
                        height,
                    ) = self._get_polygon_data(object_detected)
                loc_specific_metadata[val.category] = Metadata(
                    loc_id=i,
                    category=val.category,
                    size=shape,
                    corner=corner,
                    height=height,
                    width=width,
                    segmentation=segmentation,
                ).to_json()
                li.append(loc_specific_metadata)
            final_metadata[i] = li
        return final_metadata
