%define debug_package %{nil}

%define mybuildnumber %{?build_number}%{?!build_number:1}

Name:           wol-monitor
Version:        0.0.1
Release:        %{mybuildnumber}%{?dist}
Summary:        Monitor for Wake-on-LAN packets.
BuildArch:      noarch

License:        GPLv2+
URL:            https://github.com/Rudd-O/%{name}
Source0:        https://github.com/Rudd-O/%{name}/archive/{%version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  coreutils
BuildRequires:  tar
BuildRequires:  findutils
BuildRequires:  systemd-rpm-macros

%{?systemd_requires}
Requires:       python3

%description
This program runs as a service listening on ports 9 and 40000 (UDP), then
when a message arrives on any of those ports (traditionally Wake-on-LAN
messages), it reacts by writing to a well-known socket in the local
file system.

%prep
%setup -q

%build
# variables must be kept in sync with install
make DESTDIR=$RPM_BUILD_ROOT LIBEXECDIR=%{_libexecdir} UNITDIR=%{_unitdir}

%install
rm -rf $RPM_BUILD_ROOT
# variables must be kept in sync with build
make install DESTDIR=$RPM_BUILD_ROOT LIBEXECDIR=%{_libexecdir} UNITDIR=%{_unitdir} PRESETDIR=%{_presetdir}

%files
%attr(0755, root, root) %{_libexecdir}/%{name}
%config %attr(0644, root, root) %{_unitdir}/%{name}.service
%attr(0644, root, root) %{_presetdir}/75-%{name}.preset

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Wed May 07 2020 Manuel Amador (Rudd-O) <rudd-o@rudd-o.com>
- Initial release
