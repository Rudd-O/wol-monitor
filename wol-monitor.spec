%define debug_package %{nil}

%define mybuildnumber %{?build_number}%{?!build_number:1}

Name:           wol-monitor
Version:        0.2.0
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
Requires(pre):  shadow-utils

%description
This program runs as a service listening on ports 9 and 40000 (UDP), then
when a message arrives on any of those ports (traditionally Wake-on-LAN
messages), it reacts by writing to a well-known socket in the local
file system.

%package -n kodi-wol-starter
Summary:  A demo client for wol-monitor that starts or activates Kodi when a WOL packet is received.

Requires: python3
Requires: kodi
Requires: xdotool

%description -n kodi-wol-starter
This is a demo client for wol-monitor that starts Kodi (if it is not running)
or activates its main window (if it is running) when a Wake-on-LAN packet is
received by wol-monitor.  It is set to autostart in your user session when you
log into your desktop.

%prep
%setup -q

%build
# variables must be kept in sync with install
make DESTDIR=$RPM_BUILD_ROOT LIBEXECDIR=%{_libexecdir} UNITDIR=%{_unitdir} PRESETDIR=%{_presetdir} BINDIR=%{_bindir} SYSCONFDIR=%{_sysconfdir}

%install
rm -rf $RPM_BUILD_ROOT
# variables must be kept in sync with build
make install DESTDIR=$RPM_BUILD_ROOT LIBEXECDIR=%{_libexecdir} UNITDIR=%{_unitdir} PRESETDIR=%{_presetdir} BINDIR=%{_bindir} SYSCONFDIR=%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/default
echo WOL_GROUP=wol > $RPM_BUILD_ROOT/%{_sysconfdir}/default/%{name}
make install-kodi-wol-starter DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} SYSCONFDIR=%{_sysconfdir}

%files
%attr(0755, root, root) %{_libexecdir}/%{name}
%config %attr(0644, root, root) %{_unitdir}/%{name}.service
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/default/%{name}
%attr(0644, root, root) %{_presetdir}/75-%{name}.preset
%doc README.md

%files -n kodi-wol-starter
%attr(0755, root, root) %{_bindir}/kodi-wol-starter
%config %attr(0644, root, root) %{_sysconfdir}/xdg/autostart/kodi-wol-starter.desktop

%pre
getent group wol >/dev/null || groupadd -r wol || true

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Thu May 7 2020 Manuel Amador (Rudd-O) <rudd-o@rudd-o.com>
- Initial release
