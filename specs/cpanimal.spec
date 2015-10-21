Name:            cpanimal
Version:         1.0.0
%if %{?_release:1}0
Release:       %{_release}%{?dist}
%else
Release:         1%{?dist}
%endif
Summary:         CPAN to RPM - RAWR!
License:         GPLv3+
Group:           Development/Tools
URL:             https://github.com/filefrog/cpanimal
Source0:       %{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{release}-root%(%{__id_u} -n)

BuildRequires:   rpm-build
BuildRequires:   perl


%description
We've all been there. A new Perl project, to be deployed on your favorite RPM-based OS stack. So many dependencies. And dependencies of dependencies. It's dependencies all the way down.

So you think about CPAN, if only for a fleeting minute. It would be so easy! Just CPAN it and forget about the whole mess.

What if there was a better way? Ideally, you want RPMs for all those dang CPAN modules, but building packages is hard. Then there's all those dependencies.

cpanimal to the rescue!

It uses the MetaCPAN API to crawl CPAN, find all the dependencies, and then builds concise little RPM packages for each module. Lather, rinse, repeat.


%prep
%setup -q


%install
rm -rf $RPM_BUILD_ROOT
install -m 0755 -D cpanimal          $RPM_BUILD_ROOT%{_bindir}/cpanimal
install -m 0755 -D src/perl-provides $RPM_BUILD_ROOT%{_bindir}/perl-provides
install -m 0755 -D src/perl-requires $RPM_BUILD_ROOT%{_bindir}/perl-requires


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/cpanimal
%{_bindir}/perl-requires
%{_bindir}/perl-provides


#######################################################

%changelog
* Wed Oct 21 2015 Dan Molik <dan@d3fy.net> 1.0.0-1
- Initial packaging
