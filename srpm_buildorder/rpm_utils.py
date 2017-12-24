import re
import tempfile

import rpm

from .rpm_booldep import BooleanDependencyParser
from .package import Package, SourcePackage

__all__ = [
        ]

REGEX_PARSE_VERSION_LINE = re.compile('^(?P<name>\\S+)( = (?P<version>\\S+))?$')

def spec_from_srpm(srpm_path):
    ts = rpm.ts()
    fd = rpm.fd.open(srpm_path)
    try:
        hdr = ts.hdrFromFdno(fd)
        if not hdr.isSource():
            raise ValueError('Not an SRPM: {}'.format(srpm_path))
        files = rpm.files(hdr)
        payload = rpm.fd.open(fd, flags=bytes(hdr['PAYLOADCOMPRESSOR']).decode())
        try:
            archive = files.archive(payload)
            for f in archive:
                if f.fflags & rpm.RPMFILE_SPECFILE:
                    return archive.read()
        finally:
            rpm.fd.close(payload)
    finally:
        rpm.fd.close(fd)
    raise ValueError('No spec file found in SRPM: {}'.format(srpm_path))

def parse_spec(spec):
    rpm.reloadConfig()
    with tempfile.NamedTemporaryFile(suffix='.spec') as tmpfile:
        tmpfile.write(spec)
        tmpfile.flush()
        return rpm.spec(tmpfile.name)

def parse_version_line(line):
    m = REGEX_PARSE_VERSION_LINE.match(line)
    if not m:
        raise ValueError('Unable to parse spec version line: "{}"'.format(line))
    res = m.groupdict()
    return (res['name'], res['version'])

def parse_requires(require_strs):
    requires = {}
    for line in require_strs:
        parser = BooleanDependencyParser(line.strip())
        for name, op, version in parser.parse():
            requires.setdefault(name, [])
            if version:
                requires[name].append((op, version))
    return requires

def parse_provides(provide_strs):
    provides = {}
    for line in provide_strs:
        name, version = parse_version_line(line.strip())
        provides.setdefault(name, [])
        if version:
            provides[name].append(version)
    return provides

def hdr_to_pkg(spec):
    packages = [
        Package(
            bytes(pkg.header['NAME']).decode(),
            bytes(pkg.header['VERSION']).decode(),
            parse_provides(bytes(s).decode() for s in pkg.header['PROVIDENEVRS']))
        for pkg in spec.packages]
    return SourcePackage(
            bytes(spec.sourceHeader['NAME']).decode(),
            bytes(spec.sourceHeader['EVR']).decode(),
            parse_requires(bytes(s).decode() for s in spec.sourceHeader['REQUIRENEVRS']),
            parse_requires(bytes(s).decode() for s in spec.sourceHeader['CONFLICTNEVRS']),
            packages)

def srpm_to_pkg(srpm_path):
    spec = spec_from_srpm(srpm_path)
    spec_hdr = parse_spec(spec)
    return hdr_to_pkg(spec_hdr)
