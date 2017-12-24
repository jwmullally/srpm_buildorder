from copy import deepcopy

from .package import Package
from .rpm_version import version_match


class SourcePackageHints(object):
    def __init__(self, name, versions, provides):
        self.name = str(name),
        self.versions = [[str(op), str(ver)] for op,ver in versions]
        self.provides = {str(pkgn): [str(ver) for ver in vers] for pkgn,vers in provides.items()}

    @classmethod
    def from_dict(cls, indict):
        indict = dict(indict)
        obj = cls(
            name = indict.pop('name'),
            versions = indict.pop('versions', []),
            provides = indict.pop('provides'))
        if indict:
            raise ValueError('Unrecognized keys: {}'.format(indict.keys()))
        return obj


class HintAdder(object):

    HINT_PKG_NAME = '__srpm_buildorder_hints'
    HINT_PKG_VER = '1.0'

    def __init__(self, hints):
        self._hints = {}
        for pkghints in hints:
            self._hints.setdefault(pkghints.name, []).append(pkghints)

    def process(self, spkg):
        spkg = deepcopy(spkg)
        hpkg = Package(self.HINT_PKG_NAME, self.HINT_PKG_VER, {})
        for pkghints in self._hints.get(spkg.name, []):
            if version_match(pkghints.versions, spkg.version):
                for pkgn, vers in pkghints.provides.items():
                    hpkg.provides.setdefault(pkgn, []).extend(deepcopy(vers))
        if hpkg.provides:
           spkg.add_package(hpkg)
        return spkg
