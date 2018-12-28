# -*- coding: utf-8 -*-

"""Top-level package for kernelmethods."""

__all__ = ['PolyKernel', 'BaseKernelFunction']

from kernelmethods.base import BaseKernelFunction
from kernelmethods.numeric_kernels import PolyKernel

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__author__ = """Pradeep Reddy Raamana"""
__email__ = 'raamana@gmail.com'