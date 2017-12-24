%global pypi_name srpm_buildorder

Name:           python-%{pypi_name}
Version:        0.1
Release:        1%{?dist}
Summary:        Calculate SRPM build order
License:        GPLv2+
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-nose
BuildRequires:  python2-rpm
BuildRequires:  python-setuptools

#BuildRequires:  python-sphinx
 
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-rpm
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
Calculate SRPM build order. Useful for mockchain

%package -n     python2-%{pypi_name}
Summary:        %{summary}
Requires:       python
Requires:       python2-rpm
Requires:       python-setuptools

%description -n python2-%{pypi_name}
Calculate SRPM build order. Useful for mockchain

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
Requires:       python%{python3_pkgversion}
Requires:       python%{python3_pkgversion}-rpm
Requires:       python%{python3_pkgversion}-setuptools

%description -n python%{python3_pkgversion}-%{pypi_name}
Calculate SRPM build order. Useful for mockchain

#%package -n python-%{pypi_name}-doc
#Summary:        %{pypi_name} documentation
#
#%description -n python-%{pypi_name}-doc
#Documentation for %{pypi_name}

%prep
%autosetup

%build
%{__python2} setup.py build
%{__python3} setup.py build
# generate html docs 
#sphinx-build docs html
# remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}

%install
%{__python3} setup.py install --skip-build --root %{buildroot}
cp %{buildroot}/%{_bindir}/srpm_buildorder %{buildroot}/%{_bindir}/srpm_buildorder-3
ln -sf %{_bindir}/srpm_buildorder-3 %{buildroot}/%{_bindir}/srpm_buildorder-%{python3_version}

%{__python2} setup.py install --skip-build --root %{buildroot}
cp %{buildroot}/%{_bindir}/srpm_buildorder %{buildroot}/%{_bindir}/srpm_buildorder-2
ln -sf %{_bindir}/srpm_buildorder-2 %{buildroot}/%{_bindir}/srpm_buildorder-%{python2_version}

%check
%{__python2} setup.py nosetests
%{__python3} setup.py nosetests

%files -n python2-%{pypi_name}
#%doc 
%{_bindir}/srpm_buildorder
%{_bindir}/srpm_buildorder-2
%{_bindir}/srpm_buildorder-%{python2_version}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python%{python3_pkgversion}-%{pypi_name}
#%doc 
%{_bindir}/srpm_buildorder-3
%{_bindir}/srpm_buildorder-%{python3_version}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

#%files -n python-%{pypi_name}-doc
#%doc html 

%changelog
* Thu Aug 03 2017 Joseph Mullally <jwmullally@gmail.com> - 0.1-1
- Initial test package.
