import sys

collect_ignore = ["setup.py"]
if sys.version_info[0] <= 2:
    collect_ignore.append("tests/python_3")
