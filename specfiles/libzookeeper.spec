Name:           libzookeeper
Version:        3.4.7
Release:        1%{?dist}
Summary:        Zookeeper C binding library

Group:          System Environment/Libraries
License:        Apache License, Version 2.0
URL:            http://zookeeper.apache.org/
Source0:        zookeeper-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{release}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool

Provides:       libzookeeper

%description
ZooKeeper C client library for communicating with ZooKeeper Server.


%prep
%setup -n zookeeper-release-%{version} -q


%build
ant compile_jute
cd src/c
autoreconf -i -f
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd src/c
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/load_gen


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/cli_mt
%{_bindir}/cli_st
%{_includedir}/zookeeper/proto.h
%{_includedir}/zookeeper/recordio.h
%{_includedir}/zookeeper/zookeeper.h
%{_includedir}/zookeeper/zookeeper.jute.h
%{_includedir}/zookeeper/zookeeper_log.h
%{_includedir}/zookeeper/zookeeper_version.h
%{_libdir}/libzookeeper_mt.a
%{_libdir}/libzookeeper_mt.la
%{_libdir}/libzookeeper_mt.so
%{_libdir}/libzookeeper_mt.so.2
%{_libdir}/libzookeeper_mt.so.2.0.0
%{_libdir}/libzookeeper_st.a
%{_libdir}/libzookeeper_st.la
%{_libdir}/libzookeeper_st.so
%{_libdir}/libzookeeper_st.so.2
%{_libdir}/libzookeeper_st.so.2.0.0
