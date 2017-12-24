from contextlib import contextmanager
from glob import glob
import os
import shutil
import subprocess
import sys
import tempfile

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

def make_srpm(spec, dest_dir):
    tmpdir = tempfile.mkdtemp('_test_rpmbuild')
    try:
        subprocess.check_output(['rpmbuild',
                '--define',
                '_topdir {}'.format(tmpdir),
                '-bs',
                spec])
        srpm_path = glob(os.path.join(tmpdir, 'SRPMS', '*.src.rpm'))[0]
        srpm = os.path.basename(srpm_path)
        dest = os.path.join(dest_dir, srpm)
        if os.path.exists(dest):
            raise Exception('Building {} failed, SRPM already exists {}'.format(spec, dest))
        shutil.move(srpm_path, dest)
    finally:
        shutil.rmtree(tmpdir)
    return srpm

def make_srpmsets(spec_dir, dest_dir):
    srpms = {}
    for testset in os.listdir(spec_dir):
        srpms[testset] = {}
        os.mkdir(os.path.join(dest_dir, testset))
        #for spec in glob(os.path.join(spec_dir, testset, '*.spec')):
        for f in glob(os.path.join(spec_dir, testset, '*')):
            if f.endswith('.spec'):
                srpm = make_srpm(f, os.path.join(dest_dir, testset))
                spec_name = os.path.basename(f)[:-len('.spec')]
                srpms[testset][spec_name] = srpm
            else:
                shutil.copy(f, os.path.join(dest_dir, testset))
    return srpms

