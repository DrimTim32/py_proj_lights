import os
import re
import sys

total = 0.0
count = 0

BASE_DIRECTORY = os.getcwd()
EXTENDED = ""
TYPE = "text"

excluded_directories = ["develop_scripts", "tests", "docs"]
excluded_files = ["__init__.py", "setup.py", "custom_assertions.py","conftest.py"]


def check(module):
    global total, count, BASE_DIRECTORY

    if module[-3:] == ".py":

        pout = os.popen('pylint {} --output-format={}'.format(module, TYPE), 'r')
        print("Checking {}".format(module))
        for line in pout:
            if EXTENDED == "f":
                print(line)
            elif EXTENDED == "e" and line[0:2] in ["C:", "W:", "E:"]:
                print(line)
            elif "Your code has been rated at" in line:
                print(line)
            if "Your code has been rated at" in line:
                score = re.findall("\d.\d\d", line)[0]
                total += float(score)
                count += 1

        print("-" * 50 + "\n")


if __name__ == "__main__":

    BASE_DIRECTORY = sys.argv[1]
    EXTENDED = sys.argv[2]
    TYPE = sys.argv[3]
    if len(sys.argv) > 4:
        sys.stdout = open(sys.argv[4], 'w+')

    for root, dirs, files in os.walk(BASE_DIRECTORY):
        for ignore in excluded_directories:
            if ignore in dirs:
                dirs.remove(ignore)
        for name in files:
            if name in excluded_files:
                continue
            check(os.path.join(root, name))

    print("%d modules found" % count)
    print("AVERAGE SCORE = %.02f" % (total / count))
