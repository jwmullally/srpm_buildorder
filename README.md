# srpm_buildorder

**WORK IN PROGRESS**

This library and CLI tool calculates the build order for a collection of SRPM packages.

## NEXT

* Base dependencies - implement with hints for a hidden "base" node
* Increase test coverage

## Limitations 

### Automatic Dependencies

RPMs as packaged in many Linux distributions often make use of build-time generated Provide (see <http://rpm.org> - "Automatic Dependencies"). These are necessary to scalably manage thousands of interdependent packages in a distribution. Unfortunately these are not possible to know in advance without building the package, which prevents static analysis of the build dependencies and ordering. 

To workaround this, this tool allows supplying "Provide hints" for packages through a seperate file. 

An alternative to this is to use Provide information from previously built RPM's (This is the approach used by [Fedora Koschei](https://fedoraproject.org/wiki/Koschei)). However this requires building everything first by hand and keeping old RPMs around for every build. This contaminates subsequent builds and prevents flushing of all build artifacts/cache and building everything from scratch.

(To keep build processes simple for packages under control, Automatic Dependencies can be disabled using "AutoReqProv: no".)


## Reference

* <http://rpm.org/documentation.html>
* <https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/index.html>
* <https://fedoraproject.org/wiki/Packaging:Guidelines>
* <https://fedoraproject.org/wiki/Category:Packaging_guidelines>
* <https://fedoraproject.org/wiki/Archive:Tools/RPM/VersionComparison>
* <https://www.debian.org/doc/debian-policy/>
* <https://github.com/rpm-software-management/mock/blob/devel/mock/py/mockchain.py>
* <https://skvidal.wordpress.com/2013/05/17/sorting-srpms-by-buildorder/>
