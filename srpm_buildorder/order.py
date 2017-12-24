from copy import deepcopy
from .graph import DirectedGraph

__all__ = [
        'BuildOrderResolver',
        ]

class BuildOrderResolver(object):

    def __init__(self, pkgs=None):
        self._pkgs = {}          # {pkg_id: SourcePackage}
        self._buildreq_pkgs = {} # {dep: set([pkg_id])}
        self._provide_pkgs = {}  # {dep: set([pkg_id])}
        self._dep_graph = DirectedGraph()

        if pkgs:
            for pkg_id, pkg in pkgs.items():
                self.add_source_package(pkg_id, pkg)

    def _check_depends(self, pkg_a_id, pkg_b_id, dep):
        if pkg_a_id == pkg_b_id:
            return False
        pkg_a = self._pkgs[pkg_a_id]
        pkg_b = self._pkgs[pkg_b_id]
        return pkg_a.depends_on_dep(pkg_b, dep)

    def _add_pkg_provide(self, pkg_id, dep):
        self._provide_pkgs.setdefault(dep, set()).add(pkg_id)
        for other_pkg_id in self._buildreq_pkgs.get(dep, []):
            if self._check_depends(other_pkg_id, pkg_id, dep):
                self._dep_graph.add_edge((other_pkg_id, pkg_id))

    def _add_pkg_buildreq(self, pkg_id, dep):
        self._buildreq_pkgs.setdefault(dep, set()).add(pkg_id)
        for other_pkg_id in self._provide_pkgs.get(dep, []):
            if self._check_depends(pkg_id, other_pkg_id, dep):
                self._dep_graph.add_edge((pkg_id, other_pkg_id))

    def add_source_package(self, pkg_id, pkg):
        if pkg_id in self._pkgs:
            raise ValueError('SourcePackage "{}" already present'.format(pkg_id))
        pkg = deepcopy(pkg)
        self._pkgs[pkg_id] = pkg
        self._dep_graph.add_node(pkg_id)

        for dep in pkg._provides:
            self._add_pkg_provide(pkg_id, dep)
        for dep in pkg.build_requires:
            self._add_pkg_buildreq(pkg_id, dep)

    def build_order_serial(self):
        return self._dep_graph.topological_sort()

    def build_order_graph(self):
        return self._dep_graph.simple_graph()

    def unresolved_buildreqs(self):
        unresolved_pkgs = {}
        for dep in set(self._buildreq_pkgs) - set(self._provide_pkgs):
            unresolved_pkgs[dep] = {}
            for pkg in self._buildreq_pkgs[dep]:
                unresolved_pkgs[dep][pkg] = deepcopy(self._pkgs[pkg].build_requires[dep])
        return unresolved_pkgs

