Name:           libmill
Version:        1.4
Release:        1%{?dist}
Summary:        Go-style concurrency in C

Group:          System Environment/Libraries
License:        GPLv3+
URL:            https://libmill.org
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool

%description
Libmill is a lightweight coroutine library bringing Go-style concurrency to C language.
It also contains simple networking library that allows users to quickly bootstrap
application development.

Libmill runs in following environments:

Microarchitecture: x86_64, ARM
Compiler: gcc, clang
Operating system: Linux, OSX, FreeBSD, OpenBSD, NetBSD, DragonFlyBSD
Whether it works in different environments is not known - please, do report any successes
or failures to the project mailing list.

%package devel
Summary:  Go-style concurrency in C
Group:    Development/Libraries

%description devel
Libmill is a lightweight coroutine library bringing Go-style concurrency to C language.
It also contains simple networking library that allows users to quickly bootstrap
application development.

Libmill runs in following environments:

Microarchitecture: x86_64, ARM
Compiler: gcc, clang
Operating system: Linux, OSX, FreeBSD, OpenBSD, NetBSD, DragonFlyBSD
Whether it works in different environments is not known - please, do report any successes
or failures to the project mailing list.

This package contains the header files for developing code against libmill.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libdir}/libmill.so
%{_libdir}/libmill.so.12
%{_libdir}/libmill.so.12.2.0


%files devel
%defattr(-,root,root,-)
%{_includedir}/libmill.h
%{_libdir}/libmill.a
%{_libdir}/libmill.la
%{_libdir}/pkgconfig/libmill.pc

