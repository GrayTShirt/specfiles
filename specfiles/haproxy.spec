%define _user   haproxy

Name:           haproxy
Version:        1.7.4
Release:        1%{?dist}
Summary:        HA-Proxy is a TCP/HTTP reverse proxy for high availability environments
Group:          System Environment/Daemons
License:        GPL
URL:            http://www.haproxy.org/

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

BuildRequires:  pcre-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

Requires:       /sbin/chkconfig, /sbin/service

Source0:  http://www.%{name}.org/download/1.7/src/devel/%{name}-%{version}.tar.gz
Source1:  https://github.com/GrayTShirt/specfiles/raw/master/extras/%{name}.initd.tar.gz

%description
HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
- route HTTP requests depending on statically assigned cookies
- spread the load among several servers while assuring server persistence
  through the use of HTTP cookies
- switch to backup servers in the event a main one fails
- accept connections to special ports dedicated to service monitoring
- stop accepting connections without breaking existing ones
- add/modify/delete HTTP headers both ways
- block requests matching a particular pattern

It needs very little resource. Its event-driven architecture allows it to easily
handle thousands of simultaneous connections on hundreds of instances without
risking the system's stability.

%prep
%setup -q
%setup -T -D -a 1

# We don't want any perl dependecies in this RPM:
%define __perl_requires /bin/true


%build
make %{?_smp_mflags} \
	DEBUG="" \
	'LDFLAGS=-Wl,-O1 -Wl,--as-needed' \
	ARCH=%{_target_cpu} \
	TARGET=linux2628 \
	USE_GETADDRINFO=1 \
	USE_TFO=1 \
	USE_LIBCRYPT=1 \
	USE_NS= \
	USE_PCRE=1 \
	USE_OPENSSL=1 \
	USE_SLZ= \
	USE_ZLIB=1


%install
rm -rf %{buildroot}

%{__install} -d %{buildroot}%{_sbindir}
%{__install} -s %{name} %{buildroot}%{_sbindir}/
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d %{buildroot}%{_mandir}/man1/

%{__install} -D -p -m 755 %{name}.initd %{buildroot}%{_initrddir}/%{name}
%{__install} -c -m 755 doc/%{name}.1 %{buildroot}%{_mandir}/man1/


%clean
rm -rf %{buildroot}


%pre
getent group  %{_user} || groupadd -r %{_user}
getent passwd %{_user} || useradd  -r -g %{_user} -c 'nginx daemon' -d %{_datadir}/%{name} -s /sbin/nologin %{_user}


%post
/sbin/chkconfig --add %{name}


%preun
if [ $1 = 0 ]; then
	/sbin/service %{name} stop
	/sbin/chkconfig --del %{name}
fi


%postun
if [ "$1" -ge "1" ]; then
	/sbin/service %{name} condrestart
fi


%files
%defattr(-,root,root,-)
%doc CHANGELOG README doc/architecture.txt doc/configuration.txt doc/intro.txt doc/management.txt doc/proxy-protocol.txt
%doc %{_mandir}/man1/%{name}.1*

%defattr(0755,root,root,0755)
%{_sbindir}/%{name}
%{_initrddir}/%{name}

%dir  %{_sysconfdir}/%{name}

%changelog
* Mon Mar 27 2017 Willy Tarreau <w@1wt.eu>
- updated to 1.7.4
