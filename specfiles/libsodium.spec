Name:      libsodium
Version:   1.0.8
Release:   1%{?dist}
Summary:   A modern and easy-to-use crypto library

Group:     System Environment/Libraries
License:   distributable
URL:       https://download.libsodium.org/doc/
Source0:   https://download.%{name}.org/%{name}/releases/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: libtool


%description
Sodium is a modern, easy-to-use software library for encryption, decryption,
signatures, password hashing and more. It is a portable, cross-compilable,
installable, packageable fork of NaCl, with a compatible API, and an extended
API to improve usability even further.

Its goal is to provide all of the core operations needed to build higher-level
cryptographic tools. Sodium supports a variety of compilers and operating systems,
including Windows (with MinGW or Visual Studio, x86 and x86_64), iOS and Android.

The design choices emphasize security, and "magic constants" have clear rationales.
And despite the emphasis on high security, primitives are faster across-the-board
than most implementations of the NIST standards.


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
