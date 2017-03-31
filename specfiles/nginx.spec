%define _user                   nginx
%define _cache_dir            %{_localstatedir}/cache/nginx
%define _push_stream_version    0.5.2
%define _vts_version            0.1.14

Name:           nginx
Version:        1.11.12
Release:        1%{?dist}
Summary:        High performance web server
Group:          System Environment/Daemons
Vendor:         Dan Molik <dan@danmolik.com>
License:        2-clause BSD-like license
URL:            http://nginx.org

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

BuildRequires:      gcc
BuildRequires:      gd-devel
BuildRequires:      GeoIP-devel
BuildRequires:      libxml2-devel
BuildRequires:      libxslt-devel
BuildRequires:      openldap-devel
BuildRequires:      openssl-devel
BuildRequires:      pcre-devel
BuildRequires:      perl(ExtUtils::Embed)
BuildRequires:      zlib-devel

Requires:           pcre
Requires:           zlib
Requires:           openssl

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
            # https://github.com/vozlt/nginx-module-vts/archive/v0.1.14.tar.gz
Source4:    %{name}-module-vts-%{_vts_version}.tar.gz
Patch0:     %{name}-auth-ldap-master-pragma.patch


%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server.


%prep
%setup -q
%setup -T -D -a 1
%setup -T -D -a 2
%setup -T -D -a 3
%setup -T -D -a 4
%patch0 -p0


%build
./configure \
	--prefix=%{_datadir}/%{name} \
	--sbin-path=%{_sbindir}/%{name} \
	--conf-path=/etc/nginx/nginx.conf \
	--error-log-path=/var/log/%{name}error.log \
	--http-log-path=/var/log/${name}/access.log \
	--pid-path=/var/run/nginx.pid \
	--lock-path=/var/run/nginx.lock \
	--modules-path=%{_datadir}/%{name}/modules \
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
	--with-http_ssl_module \
	--with-http_v2_module \
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
	\
	--with-stream=dynamic \
	--with-stream_ssl_module \
	--with-stream_realip_module \
	--with-stream_geoip_module \
	--with-stream_geoip_module=dynamic \
	--with-stream_ssl_preread_module \
	\
	--with-http_xslt_module=dynamic \
	--with-http_image_filter_module=dynamic \
	\
	--with-mail=dynamic \
	--with-mail_ssl_module \
	\
	--with-http_geoip_module=dynamic \
	--with-http_perl_module=dynamic \
	--add-dynamic-module=%{_builddir}/%{name}-%{version}/%{name}-push-stream-module-%{_push_stream_version} \
	--add-dynamic-module=%{_builddir}/%{name}-%{version}/%{name}-auth-ldap-master \
	--add-dynamic-module=%{_builddir}/%{name}-%{version}/%{name}-module-vts-%{_vts_version}
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
%{__install} -D -d -p -m 755 %{buildroot}/var/log/%{name}
%{__install} -D -d -p -m 755 %{buildroot}%{_cache_dir}/client_temp
%{__install} -D -d -p -m 755 %{buildroot}%{_cache_dir}/proxy_temp
%{__install} -D -d -p -m 755 %{buildroot}%{_cache_dir}/fastcgi_temp
%{__install} -D -d -p -m 755 %{buildroot}%{_cache_dir}/uwsgi_temp
%{__install} -D -d -p -m 755 %{buildroot}%{_cache_dir}/scgi_temp
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

%{_datadir}/%{name}/html/index.html
%{_datadir}/%{name}/html/50x.html

%doc LICENSE CHANGES README
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

%defattr(-,%{_user},%{_user},-)
%dir /var/log/%{name}
%dir %{_cache_dir}/client_temp
%dir %{_cache_dir}/proxy_temp
%dir %{_cache_dir}/fastcgi_temp
%dir %{_cache_dir}/uwsgi_temp
%dir %{_cache_dir}/scgi_temp

%package      module-perl
Summary:      Dynamic Nginx Perl module
Group:        System Environment/Daemons

Requires:     perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description  module-perl
Dynamic Nginx Perl module

%files        module-perl
%defattr(-,root,root,-)
%{perl_vendorarch}/%{name}.pm
%{perl_vendorarch}/auto/%{name}/%{name}.bs
%{perl_vendorarch}/auto/%{name}/%{name}.so

%{_datadir}/%{name}/modules/ngx_http_perl_module.so

%doc %{_mandir}/man3/%{name}.3pm.gz


%package      module-auth-ldap
Summary:      Dynamic Nginx ldap module
Group:        System Environment/Daemons

%description  module-auth-ldap
Dynamic Nginx ldap module

%files        module-auth-ldap
%defattr(-,root,root,-)
%{_datadir}/%{name}/modules/ngx_http_auth_ldap_module.so


%package      module-geoip
Summary:      Dynamic Nginx GeoIP module
Group:        System Environment/Daemons

%description  module-geoip
Dynamic Nginx GeoIP module

%files        module-geoip
%defattr(-,root,root,-)
%{_datadir}/%{name}/modules/ngx_http_geoip_module.so


%package      module-image-filter
Summary:      Dynamic Nginx image filter module
Group:        System Environment/Daemons

%description  module-image-filter
Dynamic Nginx image filter module

%files        module-image-filter
%defattr(-,root,root,-)
%{_datadir}/%{name}/modules/ngx_http_image_filter_module.so


%package      module-push-stream
Summary:      Dynamic Nginx Push Stream module
Group:        System Environment/Daemons

%description  module-push-stream
Wandenburg's Dynamic Nginx Push Stream module

%files        module-push-stream
%defattr(-,root,root,-)
%{_datadir}/%{name}/modules/ngx_http_push_stream_module.so


%package      module-xslt
Summary:      Dynamic Nginx xslt module
Group:        System Environment/Daemons

%description  module-xslt
Dynamic Nginx XSLT module

%files        module-xslt
%defattr(-,root,root,-)
%{_datadir}/%{name}/modules/ngx_http_xslt_filter_module.so


%package      module-mail
Summary:      Dynamic Nginx email module
Group:        System Environment/Daemons

%description  module-mail
Dynamic Nginx email module

%files        module-mail
%defattr(-,root,root,-)
%{_datadir}/%{name}/modules/ngx_mail_module.so


%package      module-stream
Summary:      Dynamic Nginx Streaming module
Group:        System Environment/Daemons

%description  module-stream
Dynamic Nginx Streaming module

%files        module-stream
%defattr(-,root,root,-)
%{_datadir}/%{name}/modules/ngx_stream_module.so


%package      module-stream-geoip
Summary:      Dynamic Nginx Geo-Streaming nmodule
Group:        System Environment/Daemons

%description  module-stream-geoip
Dynamic Nginx Geo-Streaming module

%files        module-stream-geoip
%defattr(-,root,root,-)
%{_datadir}/%{name}/modules/ngx_stream_geoip_module.so


%package      module-vts
Summary:      Nginx virtual host traffic status module
Group:        System Environment/Daemons

%description  module-vts
Nginx virtual host traffic status module

%files        module-vts
%defattr(-,root,root,-)
%{_datadir}/%{name}/modules/ngx_http_vhost_traffic_status_module.so


%changelog
* Fri Mar 31 2017 Dan Molik <dan@d3fy.net> 1.11.12-1
- nginx 1.11.12
  vts module
  many other dynamic modoules
