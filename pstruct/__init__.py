#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .core import Pstruct, ValidatedPstruct
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
