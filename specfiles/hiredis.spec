Name:           hiredis
Version:        0.13.3
Vendor:         Dan Molik <dan@danmolik.com>
%if %{?_release:1}0
Release:        %{_release}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        A minimalistic C client library for Redis

License:        BSD

Group:          System Environment/Libraries
URL:            http://github.com/redis/hiredis
#               https://github.com/redis/hiredis/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  make

%define MINOR %(echo %{version} | sed -e 's/\.[0-9]*$//')
%define MAJOR %(echo %{version} | sed -e 's/\.[0-9]*\.[0-9]*$//')

%description
Hiredis is a minimalistic C client library for the Redis database.

%package        devel
Summary:        Header files and libraries for hiredis C development
Group:          Development/Libraries

%description    devel
The hiredis-devel package contains the header files and
libraries to develop applications using a Redis database.

%prep
%setup -q

%build
make %{?_smp_mflags} LDFLAGS="%{?__global_ldflags}"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=/ INCLUDE_PATH=%{_includedir}/%{name} LIBRARY_PATH=%{_libdir}
ln -sf libhiredis.so.%{MINOR} $RPM_BUILD_ROOT%{_libdir}/libhiredis.so.%{MAJOR}
rm $RPM_BUILD_ROOT%{_includedir}/%{name}/adapters/glib.h
rm $RPM_BUILD_ROOT%{_includedir}/%{name}/adapters/ivykis.h
rm $RPM_BUILD_ROOT%{_includedir}/%{name}/adapters/libuv.h
rm $RPM_BUILD_ROOT%{_includedir}/%{name}/adapters/macosx.h
rm $RPM_BUILD_ROOT%{_includedir}/%{name}/adapters/qt.h

# install docs
install -m 0644 -D COPYING   $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/COPYING
install -m 0644 -D README.md $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/README.md

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libhiredis.so.%{MINOR}
%{_libdir}/libhiredis.so.%{MAJOR}
%{_libdir}/libhiredis.so
%{_docdir}/%{name}-%{version}/COPYING

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/adapters/ae.h
%{_includedir}/%{name}/adapters/libev.h
%{_includedir}/%{name}/adapters/libevent.h
%{_includedir}/%{name}/async.h
%{_includedir}/%{name}/hiredis.h
%{_includedir}/%{name}/read.h
%{_includedir}/%{name}/sds.h
%{_libdir}/libhiredis.a
%{_libdir}/pkgconfig/hiredis.pc
%{_docdir}/%{name}-%{version}/README.md

#######################################################

%changelog
* Tue Oct 20 2015 Dan Molik <dan@d3fy.net> 0.13.3-1
- upstream release

* Tue Oct 05 2010 Dan Molik <dan@d3fy.net> 0.0.20101005
- Initial release
