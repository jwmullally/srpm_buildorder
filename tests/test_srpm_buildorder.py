from glob import glob
import json
import os
import shutil
import tempfile
import unittest

from .utils import *

from srpm_buildorder import cli

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp('_test')
        test_dir = os.path.dirname(os.path.abspath(__file__))
        spec_dir = os.path.join(test_dir, 'specs')
        self.srpms = make_srpmsets(spec_dir, self.tmpdir)
        self.maxDiff = None

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_standard(self):
        os.chdir(os.path.join(self.tmpdir, 'standard'))
        argv = ['<prog>', 'serial', '--srpms'] + sorted(os.listdir('.'))
        args = cli.parse_args(argv)
        args.output = StringIO()
        cli.main(args)
        self.assertEqual(
                args.output.getvalue(),
                '\n'.join([
                    "pkgA-1.0-1.src.rpm",
                    "pkgE-1.0-1.src.rpm",
                    "pkgB-1.0-1.src.rpm",
                    "pkgC-1.0-1.src.rpm",
                    "pkgD-1.0-1.src.rpm"])+'\n')

    def test_graph(self):
        os.chdir(os.path.join(self.tmpdir, 'standard'))
        argv = ['<prog>', 'graph', '--srpms'] + sorted(os.listdir('.'))
        args = cli.parse_args(argv)
        args.output = StringIO()
        cli.main(args)
        self.assertEqual(
                json.loads(args.output.getvalue()),
                {
                    "pkgA-1.0-1.src.rpm": [],
                    "pkgB-1.0-1.src.rpm": [
                        "pkgA-1.0-1.src.rpm"
                    ],
                    "pkgC-1.0-1.src.rpm": [
                        "pkgA-1.0-1.src.rpm"
                    ],
                    "pkgD-1.0-1.src.rpm": [
                        "pkgB-1.0-1.src.rpm",
                        "pkgC-1.0-1.src.rpm"
                    ],
                    "pkgE-1.0-1.src.rpm": []
                })

    def test_versions(self):
        os.chdir(os.path.join(self.tmpdir, 'versions'))
        argv = ['<prog>', 'graph', '--strict', '--srpms'] + sorted(os.listdir('.'))
        args = cli.parse_args(argv)
        args.output = StringIO()
        cli.main(args)
        self.assertEqual(
                json.loads(args.output.getvalue()),
                {
                    "pkgA-1.0-1.src.rpm": [],
                    "pkgB-1.0-1.src.rpm": [
                        "pkgA-1.0-1.src.rpm"
                    ],
                    "pkgB-2.0-1.src.rpm": [
                        "pkgA-1.0-1.src.rpm"
                    ],
                    "pkgC-1.0-1.src.rpm": [
                        "pkgB-2.0-1.src.rpm"
                    ]
                })

    def test_hints(self):
        os.chdir(os.path.join(self.tmpdir, 'hints'))
        argv = ['<prog>', 'graph', '--hints', 'hints.json', '--srpms'] + sorted(glob('*.src.rpm'))
        args = cli.parse_args(argv)
        args.output = StringIO()
        cli.main(args)
        print(args.output.getvalue())
        self.assertEqual(
                json.loads(args.output.getvalue()),
                {
                    "pkgA-1.0-1.src.rpm": [],
                    "pkgB-1.0-1.src.rpm": [
                        "pkgA-1.0-1.src.rpm"
                    ]
                })


