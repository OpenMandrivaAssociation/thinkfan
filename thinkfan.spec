%define debug_package %{nil}

Name:           thinkfan
Version:	1.1
Release:	2
Summary:        Simple and lightweight fan control program
Group:		System/Base
License:        GPLv3+
URL:            http://thinkfan.sourceforge.net/
Source0:	https://github.com/vmatare/thinkfan/archive/%{version}.tar.gz
Source1:        %{name}.service
BuildRequires:  pkgconfig(yaml-cpp)
BuildRequires:  pkgconfig(libatasmart)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  cmake
Requires(pre):	rpm-helper

%define unitdir /lib/systemd/system/

%description
Thinkfan is a simple, lightweight fan control program. Originally designed
specifically for IBM/Lenovo Thinkpads, it now supports any kind of system via
the sysfs hwmon interface (/sys/class/hwmon). It is designed to eat as little
CPU power as possible.

%prep
%setup -q

%build
%cmake
%make_build


%install
%make_install -C build
mkdir -p %{buildroot}/lib
mv %{buildroot}%{_libdir}/systemd/ %{buildroot}/lib

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable %{name}.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%files
%doc README COPYING examples/
#%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/systemd/system/thinkfan.service.d/override.conf
%{_sbindir}/%{name}
%{_unitdir}/%{name}*.service
%{_mandir}/man1/thinkfan.1.*
%{_mandir}/man5/thinkfan.conf.5.*
%{_datadir}/doc/thinkfan/thinkfan.conf.*
