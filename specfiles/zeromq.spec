Name:           zeromq
Version:        4.1.4
Release:        1%{?dist}
Summary:        Software library for fast, message-based applications

Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://www.zeromq.org
Source0:        http://download.zeromq.org/zeromq-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

# BuildRequires:  glib2-devel
# BuildRequires:  openpgm-devel
BuildRequires:  libuuid-devel
BuildRequires:  libsodium-devel
BuildRequires:  gcc-c++


%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the ZeroMQ shared library.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for 
developing applications that use %{name}.


%prep
%setup -q


%build
%configure \
  --without-pgm \
  --disable-static \
  --with-pic \
  --with-libsodium
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
# remove *.la
find %{buildroot} -name \*.la -print0 | xargs -r0 rm -v

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING COPYING.LESSER NEWS
%{_bindir}/curve_keygen
%{_libdir}/libzmq.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/zmq*
%{_mandir}/man3/zmq*
%{_mandir}/man7/zmq*


%changelog
* Thu Jan 14 2016 Dan Molik <dan@d3fy.net> - 4.1.4-1
- Upstream release
