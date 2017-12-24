import argparse
import json
import sys

from .order import BuildOrderResolver
from .package import SourcePackage, Package
from .hints import SourcePackageHints, HintAdder
from .rpm_utils import srpm_to_pkg

__all__ = [
        'main',
        'parse_args',
        ]

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['extract', 'graph', 'serial', 'unresolved'])
    parser.add_argument('--srpms', nargs='+', default=[])
    parser.add_argument('--json', nargs='+', type=argparse.FileType('r'), default=[])
    parser.add_argument('--hints', nargs='+', type=argparse.FileType('r'), default=[])
    parser.add_argument('--base', nargs='+', type=argparse.FileType('r'), default=[])
    parser.add_argument('--strict', action='store_true')
    parser.add_argument('--output', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args(argv[1:])
    return args

def main(args):

    hints = []
    for hintfile in args.hints:
        for hintpkg in json.load(hintfile):
            hints.append(SourcePackageHints.from_dict(hintpkg))
    hint_adder = HintAdder(hints)

    base_ids = []
    for jsonfile in args.base:
        for pkg_id in json.load(jsonfile).items():
            if pkg_id in packages:
                raise ValueError('Duplicate package: {}'.format(pkg_id))
            packages[pkg_id] = SourcePackage.from_dict(pkg)
            base_ids.add(pkg_id)

    input_packages = {}
    for jsonfile in args.json:
        for pkg_id, pkg in json.load(jsonfile).items():
            if pkg_id in input_packages:
                raise ValueError('Duplicate package: {}'.format(pkg_id))
            input_packages[pkg_id] = SourcePackage.from_dict(pkg)

    for srpm in args.srpms:
        if srpm in input_packages:
            raise ValueError('Duplicate package: {}'.format(srpm))
        input_packages[srpm] = srpm_to_pkg(srpm)

    packages = {}
    for pkg_id, pkg in input_packages.items():
        packages[pkg_id] = hint_adder.process(pkg)

    if args.action == 'extract':
        packages_dict = dict((pkg_id, pkg.to_dict()) for pkg_id, pkg in packages.items())
        json.dump(packages_dict, args.output, sort_keys=True, indent=4)
        return

    build_resolver = BuildOrderResolver(packages)

    unresolved = build_resolver.unresolved_buildreqs()
    if args.action == 'unresolved':
        json.dump(unresolved, args.output, sort_keys=True, indent=4)
        return
    if args.strict and unresolved:
        raise ValueError('Unresolved dependencies: \n{}'.format(
            json.dumps(unresolved, sort_keys=True, indent=4)))

    graph = build_resolver.build_order_graph()
    for base_id in base_ids:
        if base_id in graph.nodes:
            graph.remove(base_id)

    if args.action == 'graph':
        json.dump(build_resolver.build_order_graph(), args.output, sort_keys=True, indent=4)
        return
    if args.action == 'serial':
        args.output.write('\n'.join(build_resolver.build_order_serial())+'\n')
        return


def entrypoint():
    main(parse_args(sys.argv))

if __name__ == '__main__':
    entrypoint()
