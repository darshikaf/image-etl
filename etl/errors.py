#!/usr/bin/env python
# -*- coding: utf-8 -*-


class InvalidFilePath(Exception):
    pass


class InvalidInputData(Exception):
    pass


class InvalidAttributeManifest(InvalidInputData):
    pass


class PathExists(Exception):
    pass


class FileHandlingError(Exception):
    pass
