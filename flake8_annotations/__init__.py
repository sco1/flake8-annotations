import sys

if sys.version_info >= (3, 8):
    PY_GTE_38 = True
else:
    PY_GTE_38 = False

if sys.version_info >= (3, 11):
    PY_GTE_311 = True
else:
    PY_GTE_311 = False

__version__ = "2.7.0"
