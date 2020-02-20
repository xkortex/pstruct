#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dstruct.core import Dstruct
from .mixins import HashaDictMixin
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
