from copy import deepcopy

from .rpm_version import version_match


class SourcePackage(object):

    def __init__(self, name, version, build_requires, build_conflicts, packages):
        self.name = str(name),
        self.version = str(version),
        self.build_requires = {str(pkgn): [[str(op), str(ver)] for op,ver in vers] for pkgn, vers in build_requires.items()}
        self.build_conflicts = {str(pkgn): [[str(op), str(ver)] for op,ver in vers] for pkgn, vers in build_conflicts.items()}
        self.packages = []
        self._provides = {}
        for pkg in packages:
            self.add_package(pkg)

    def add_package(self, pkg):
        pkg = Package.from_dict(pkg.to_dict())
        self.packages.append(pkg)
        for dep in pkg.provides:
            self._provides.setdefault(dep, []).append(pkg)

    def depends_on(self, other):
        return any(self.depends_on_dep(other, dep) for dep in self.build_requires)

    def depends_on_dep(self, other, dep):
        if dep not in self.build_requires or dep not in other._provides:
            return False
        for other_pkg in other._provides[dep]:
            for version in other_pkg.provides[dep]:
                if not version_match(self.build_requires[dep], version):
                    continue
                if dep in self.build_conflicts:
                    if version_match(self.build_conflicts[dep], version):
                        continue
                return True     # At least one matched
        return False    # None matched

    @classmethod
    def from_dict(cls, indict):
        indict = dict(indict)
        obj = cls(
                name = indict.pop('name'),
                version = indict.pop('version'),
                build_requires = indict.pop('build_requires'),
                build_conflicts = indict.pop('build_conflicts'),
                packages = [Package.from_dict(pkg) for pkg in indict.pop('packages')])
        if indict:
            raise ValueError('Unrecognized keys: {}'.format(indict.keys()))
        return obj

    def to_dict(self):
        return {
                'name': self.name,
                'version': self.version,
                'build_requires': deepcopy(self.build_requires),
                'build_conflicts': deepcopy(self.build_conflicts),
                'packages': [pkg.to_dict() for pkg in self.packages]
                }


class Package(object):
    def __init__(self, name, version, provides):
        self.name = str(name)
        self.version = str(version)
        self.provides = {str(pkgn): [str(ver) for ver in vers] for pkgn,vers in provides.items()}

    @classmethod
    def from_dict(cls, indict):
        indict = dict(indict)
        obj = cls(
            name = indict.pop('name'),
            version = indict.pop('version'),
            provides = indict.pop('provides'))
        if indict:
            raise ValueError('Unrecognized keys: {}'.format(indict.keys()))
        return obj

    def to_dict(self):
        return {
                'name': self.name,
                'version': self.version,
                'provides': deepcopy(self.provides)
                }

