Name:           lmdb
Version:        0.9.17
Release:        1%{?dist}
Summary:        An ultra-fast, ultra-compact key-value embedded data store

Group:          System Environment/Libraries
License:        OpenLDAP Public License
URL:            http://symas.com/mdb/
Source0:        https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool

%description
LMDB may also be used concurrently in a multi-threaded or multi-processing
environment, with read performance scaling linearly by design. LMDB
databases may have only one writer at a time, however unlike many similar
key-value store databases, write transactions do not block readers, nor do
readers block writers. LMDB is also unusual in that multiple applications
on the same system may simultaneously open and use the same LMDB store, as
a means to scale up performance. Also LMDB does not require a transaction
log (thereby increasing write performance by not needing to write data twice)
because it maintains data integrity inherently by design.

%package devel
Summary:        An ultra-fast, ultra-compact key-value store - Development Files
Group:          Development/Libraries

%description devel
LMDB may also be used concurrently in a multi-threaded or multi-processing
environment, with read performance scaling linearly by design. LMDB
databases may have only one writer at a time, however unlike many similar
key-value store databases, write transactions do not block readers, nor do
readers block writers. LMDB is also unusual in that multiple applications
on the same system may simultaneously open and use the same LMDB store, as
a means to scale up performance. Also LMDB does not require a transaction
log (thereby increasing write performance by not needing to write data twice)
because it maintains data integrity inherently by design.

This package contains the header files for developing against lmdb


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
%{_libdir}/libvigor.so
%{_libdir}/libvigor.so.1
%{_libdir}/libvigor.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/vigor.h
%{_libdir}/libvigor.a
%{_libdir}/libvigor.la


%changelog
* Wed Jan 20 2016 Dan Molik <dan@d3fy.net> 0.9.17-1
- New Release
