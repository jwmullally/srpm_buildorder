import os
from pprint import pprint
import shutil

from .utils import make_srpmsets

if __name__ == '__main__':
    test_dir = os.path.dirname(os.path.abspath(__file__))
    spec_dir = os.path.join(test_dir, 'specs')
    build_dir = os.path.join(os.path.abspath(os.curdir), 'build', 'testrpms')
    shutil.rmtree(build_dir, ignore_errors=True)
    os.mkdir(os.path.join(os.path.abspath(os.curdir), 'build'))
    os.mkdir(build_dir)
    make_srpmsets(spec_dir, build_dir)
