Name:      htop
Summary:   Interactive process viewer
Version:   2.0.2
Release:   1%{?dist}
License:   GPL
Group:     Applications/System
URL:       http://htop.sourceforge.net/

Source:     http://download.sourceforge.net/htop/%{name}-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gcc
BuildRequires: make
BuildRequires: ncurses-devel


%description
htop is an interactive process viewer for Linux.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_datadir}/applications/htop.desktop
rm $RPM_BUILD_ROOT/%{_datadir}/pixmaps/htop.png


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%doc %{_mandir}/man1/htop.1*
%{_bindir}/htop


%changelog
* Tue May 17 2016 Dan Molik <dan@d3fy.net> - 2.0.1-1
- Cleanup and release 2.0.1
