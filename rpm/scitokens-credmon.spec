%global pypi_name scitokens-credmon

Name:           %{pypi_name}
Version:        0.7
Release:        2%{?dist}
Summary:        SciTokens credential monitor for use with HTCondor

License:        MIT
URL:            https://github.com/htcondor/scitokens-credmon
Source0:        %{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
%if 0%{?rhel} >= 8
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%else
BuildRequires:  python2-devel >=2.7
BuildRequires:  python-setuptools
%endif

%description
A HTCondor credentials monitor specific for OAuth2 and SciTokens workflows.

%if 0%{?rhel} >= 8
%package -n     python3-%{pypi_name}
%else
%package -n     python2-%{pypi_name}
%endif

Summary:        SciTokens credential monitor for use with HTCondor
%if 0%{?rhel} >= 8
%{?python_provide:%python_provide python3-%{pypi_name}}
%else
%{?python_provide:%python_provide python2-%{pypi_name}}
%endif

%if 0%{?rhel} >= 8
Requires:       python2-condor
Requires:       python2-requests-oauthlib
Requires:       python-six
Requires:       python-flask
Requires:       python2-cryptography
Requires:       python2-scitokens
%else
Requires:       python2-condor
Requires:       python2-requests-oauthlib
Requires:       python-six
Requires:       python-flask
Requires:       python2-cryptography
Requires:       python2-scitokens
%endif

Requires:       condor >= 8.8.2
Requires:       httpd
Requires:       mod_wsgi

%if 0%{?rhel} >= 8
%description -n python3-%{pypi_name}
%else
%description -n python2-%{pypi_name}
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove pre-built egg-info
rm -rf %{pypi_name}.egg-info

%build
%if 0%{?rhel} >= 8
%py2_build
%else
%py3_build
%endif

%install
%if 0%{?rhel} >= 8
%py2_install
%else
%py3_install
%endif

ln -s %{_bindir}/condor_credmon_oauth %{buildroot}/%{_bindir}/scitokens_credmon
mkdir -p %{buildroot}/%{_var}/lib/condor/oauth_credentials
mv examples/config/README.credentials %{buildroot}/%{_var}/lib/condor/oauth_credentials
mkdir -p %{buildroot}/%{_var}/www/wsgi-scripts/scitokens-credmon
mv examples/wsgi/scitokens-credmon.wsgi %{buildroot}/%{_var}/www/wsgi-scripts/scitokens-credmon/scitokens-credmon.wsgi
rmdir examples/wsgi

%if 0%{?rhel} >= 8
%files -n python2-%{pypi_name}
%else
%files -n python2-%{pypi_name}
%endif

%doc LICENSE README.md examples
%{_bindir}/condor_credmon_oauth
%{_bindir}/scitokens_credmon
%{_bindir}/scitokens_credential_producer

%if 0%{?rhel} >= 8
%{python2_sitelib}/credmon
%{python2_sitelib}/scitokens_credmon-*.egg-info
%else
%{python2_sitelib}/credmon
%{python2_sitelib}/scitokens_credmon-*.egg-info
%endif

%{_var}/lib/condor/oauth_credentials/README.credentials
%ghost %{_var}/lib/condor/oauth_credentials/wsgi_session_key
%ghost %{_var}/lib/condor/oauth_credentials/CREDMON_COMPLETE
%ghost %{_var}/lib/condor/oauth_credentials/pid
%{_var}/www/wsgi-scripts/scitokens-credmon

%changelog
* Tue Aug 11 2020 Diego Davila <didavila@ucsd.edu> - 0.7-2
- Add conditions to build for el8 (software-4126)

* Mon Jun 01 2020 Jason Patton <jpatton@cs.wisc.edu> - 0.7-1
- Use dweitzel\'s subprocess queuing

* Tue Mar 31 2020 Jason Patton <jpatton@cs.wisc.edu> - 0.6-1
- Conform to new HTCondor OAuth config behavior

* Thu Mar 05 2020 Jason Patton <jpatton@cs.wisc.edu> - 0.5-1
- Change token deletion behavior.

* Tue Oct 08 2019 Jason Patton <jpatton@cs.wisc.edu> - 0.4-1
- Move configuration into examples directory.

* Thu May 02 2019 Jason Patton <jpatton@cs.wisc.edu> - 0.3-1
- Remove automatic install of config files. Put README in creddir.

* Fri Feb 08 2019 Brian Bockelman <brian.bockelman@cern.ch> - 0.2-1
- Include proper packaging and WSGI scripts for credmon.

* Fri Feb 08 2019 Brian Bockelman <brian.bockelman@cern.ch> - 0.1-1
- Initial package version as uploaded to the Test PyPI instance.
