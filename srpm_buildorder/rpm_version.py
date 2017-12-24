import re

import rpm

__all__ = [
        ]

REGEX_PARSE_VERSION = re.compile('^((?P<epoch>[^:]*):)?(?P<version>[^-]+)(-(?P<release>.+))?$')

def ver_to_label(version):
    m = REGEX_PARSE_VERSION.match(version)
    if not m:
        raise ValueError('Unable to parse version: "{}"'.format(version))
    res = m.groupdict()
    return (res.get('epoch', '0'),
            res['version'],
            res.get('release', None))

def version_test(version, c_op, c_ver):
    result = rpm.labelCompare(ver_to_label(version), ver_to_label(c_ver))
    if ((result == 1 and c_op in ['>', '>='])
            or (result == 0 and c_op in ['=', '>=', '<='])
            or (result == -1 and c_op in ['<', '<='])):
        return True
    return False

def version_match(constraints, version):
    if all(version_test(version, c_op, c_ver) for c_op, c_ver in constraints):
        return True
    return False
