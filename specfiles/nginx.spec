%define _user                   nginx
%define _cache_dir            %{_localstatedir}/cache/nginx
%define _push_stream_version    0.5.2

Name:           nginx
Version:        1.11.5
Release:        1%{?dist}
Summary:        High performance web server
Group:          System Environment/Daemons
License:        2-clause BSD-like license
URL:            http://nginx.org

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

BuildRequires:      gcc
BuildRequires:      pcre-devel
BuildRequires:      zlib-devel
BuildRequires:      openldap-devel
BuildRequires:      openssl-devel
BuildRequires:      perl(ExtUtils::Embed)

Requires:           pcre
Requires:           zlib
Requires:           openldap
Requires:           openssl
Requires:           perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Requires(pre):      shadow-utils
Requires(pre):      glibc-common
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(preun):    initscripts
Requires(postun):   initscripts

Source0:    http://%{name}.org/download/%{name}-%{version}.tar.gz
            # https://github.com/wandenburg/nginx-push-stream-module
Source1:    %{name}-push-stream-module-%{_push_stream_version}.tar.gz
Source2:    https://github.com/GrayTShirt/specfiles/raw/master/extras/%{name}.initd.tar.gz
            # https://github.com/kvspb/nginx-auth-ldap
            # curl https://codeload.github.com/kvspb/nginx-auth-ldap/tar.gz/master  -o ~/rpmbuild/SOURCES/nginx-auth-ldap-master.tar.gz
Source3:    %{name}-auth-ldap-master.tar.gz
Patch0:     %{name}-auth-ldap-master-pragma.patch


%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server.

One third party module, ngx_http_push_stream has been added.


%prep
%setup -q
%setup -T -D -a 1
%setup -T -D -a 2
%setup -T -D -a 3
%patch0 -p0


%build
./configure \
	--prefix=%{_datadir}/%{name} \
	--sbin-path=%{_sbindir}/%{name} \
	--conf-path=/etc/nginx/nginx.conf \
	--error-log-path=/var/log/nginx/error.log \
	--http-log-path=/var/log/nginx/access.log \
	--pid-path=/var/run/nginx.pid \
	--lock-path=/var/run/nginx.lock \
	--http-client-body-temp-path=%{_cache_dir}/client_temp \
	--http-proxy-temp-path=%{_cache_dir}/proxy_temp \
	--http-fastcgi-temp-path=%{_cache_dir}/fastcgi_temp \
	--http-uwsgi-temp-path=%{_cache_dir}/uwsgi_temp \
	--http-scgi-temp-path=%{_cache_dir}/scgi_temp \
	--user=%{_user} \
	--group=%{_user} \
	--with-threads \
	--with-file-aio \
	--with-ipv6  \
	--with-poll_module \
	--with-stream \
	--with-stream_ssl_module \
	--with-http_ssl_module \
	--with-http_v2_module \
	--with-http_perl_module \
	--with-http_realip_module \
	--with-http_addition_module \
	--with-http_sub_module  \
	--with-http_gunzip_module \
	--with-http_gzip_static_module \
	--with-http_random_index_module \
	--with-http_secure_link_module \
	--with-http_stub_status_module \
	--with-http_auth_request_module \
	--with-cc-opt='-O2 -g -pipe -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic' \
	--add-module=%{_builddir}/nginx-%{version}/nginx-push-stream-module-%{_push_stream_version} \
	--add-module=%{_builddir}/nginx-%{version}/nginx-auth-ldap-master
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} \;
%{__install} -D -p -m 644 contrib/vim/ftdetect/%{name}.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/%{name}.vim
%{__install} -D -p -m 644 contrib/vim/indent/%{name}.vim   %{buildroot}%{_datadir}/vim/vimfiles/ident/%{name}.vim
%{__install} -D -p -m 644 contrib/vim/syntax/%{name}.vim   %{buildroot}%{_datadir}/vim/vimfiles/syntax/%{name}.vim
%{__install} -D -p -m 755 %{name}.initd %{buildroot}%{_initrddir}/%{name}
rm -f %{buildroot}%{_sysconfdir}/%{name}/koi-win
rm -f %{buildroot}%{_sysconfdir}/%{name}/win-utf


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
if [ $1 -ge 1 ]; then
	/sbin/service %{name} condrestart
fi


%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_initrddir}/%{name}

%{perl_vendorarch}/%{name}.pm
%{perl_vendorarch}/auto/%{name}/%{name}.so

%{_datadir}/%{name}/html/index.html
%{_datadir}/%{name}/html/50x.html

%doc LICENSE CHANGES README
%doc %{_mandir}/man3/%{name}.3pm.gz
%doc %{_datadir}/vim/vimfiles/ftdetect/%{name}.vim
%doc %{_datadir}/vim/vimfiles/ident/%{name}.vim
%doc %{_datadir}/vim/vimfiles/syntax/%{name}.vim

%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi.conf
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi_params
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params
%config(noreplace) %{_sysconfdir}/%{name}/mime.types
%config(noreplace) %{_sysconfdir}/%{name}/koi-utf

%config %{_sysconfdir}/%{name}/%{name}.conf.default
%config %{_sysconfdir}/%{name}/fastcgi.conf.default
%config %{_sysconfdir}/%{name}/fastcgi_params.default
%config %{_sysconfdir}/%{name}/scgi_params.default
%config %{_sysconfdir}/%{name}/mime.types.default
%config %{_sysconfdir}/%{name}/uwsgi_params.default


%changelog
* Mon Feb 29 2016 Dan Molik <dan@d3fy.net> 1.9.12-1
- Reimport with push_stream
