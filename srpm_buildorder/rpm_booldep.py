import re

from .parser import RecursiveDescentParser

class BooleanDependencyParser(RecursiveDescentParser):
    """
    Parse RPM v4.13 Boolean Dependencies
    http://rpm.org/user_doc/boolean_dependencies.html

    As we only care about build dependency order, we simply return all
    packages found.

    E.g.
    >>> BooleanDependencyParser('pkgX > 4').parse()
    [('pkgX', '>', 4)]
    >>> BooleanDependencyParser('(pkgA >= 3.2 or (pkgB and pkgC))').parse()
    [('pkgA', '>=', '3.2'), ('pkgB', None, None), ('pkgC', None, None)]
    >>> BooleanDependencyParser('((pkgD if pkgE) or pkgF)').parse()
    [('pkgD', None, None), ('pkgE', None, None), ('pkgF', None, None)]
    """
    SYMBOLS = [
            ('END', re.compile('$')),
            ('LPAREN', re.compile('\\(')),
            ('RPAREN', re.compile('\\)')),
            ('AND', re.compile('and ')),
            ('OR', re.compile('or ')),
            ('IF', re.compile('if ')),
            ('ELSE', re.compile('else ')),
            ('DEP', re.compile('(?P<name>[^\\s)]+)( (?P<op>(=|<|>|<=|>=)) (?P<version>[^\\s)]+))?')),
            ]

    def boolean(self):
        deps = self.expr()
        if self.accept('AND'):
            deps.extend(self.boolean_and())
        elif self.accept('OR'):
            deps.extend(self.boolean_or())
        elif self.accept('IF'):
            deps.extend(self.expr())
            if self.accept('ELSE'):
                deps.extend(self.expr())
        return deps

    def boolean_and(self):
        deps = self.expr()
        if self.accept('AND'):
            deps.extend(self.boolean_and())
        return deps

    def boolean_or(self):
        deps = self.expr()
        if self.accept('OR'):
            deps.extend(self.boolean_or())
        return deps

    def expr(self):
        deps = []
        if self.accept('LPAREN'):
            deps.extend(self.boolean())
            self.expect('RPAREN')
        elif self.sym == 'DEP':
            deps.append((self.val['name'], self.val['op'], self.val['version']))
            self.nextsym()
        else:
            self.error(['LPAREN', 'DEP'])
        return deps

    def parse(self):
        self.nextsym()
        deps = self.expr()
        self.expect('END')
        return deps
