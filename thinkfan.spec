%define debug_package %{nil}

Name:           thinkfan
Version:        0.8.0
Release:        10
Summary:        Simple and lightweight fan control program
Group:		System/Base
License:        GPLv3+
URL:            http://thinkfan.sourceforge.net/
Source0:        http://downloads.sourceforge.net/thinkfan/%{name}-%{version}.tar.gz
Source1:        %{name}.service
BuildRequires:  systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%define unitdir /lib/systemd/system/

%description
Thinkfan is a simple, lightweight fan control program. Originally designed
specifically for IBM/Lenovo Thinkpads, it now supports any kind of system via
the sysfs hwmon interface (/sys/class/hwmon). It is designed to eat as little
CPU power as possible.

%prep
%setup -q


%build
%make


%install
install -p -D -m 0755 thinkfan %{buildroot}%{_sbindir}/%{name}
#install -p -D -m 644 rcscripts/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
# this is more complete:
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 644 examples/thinkfan.conf.complex  %{buildroot}%{_sysconfdir}/%{name}.conf

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
%doc README ChangeLog NEWS examples/
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service


%changelog
* Sun May 13 2012 Alexander Khrukin <akhrukin@mandriva.org> 0.8.0-1
+ Revision: 798537
- version update 0.8.0

* Mon Feb 13 2012 Alexander Khrukin <akhrukin@mandriva.org> 0.8_alpha2-1
+ Revision: 773745
- _unitdir insted own macro
- imported package thinkfan

