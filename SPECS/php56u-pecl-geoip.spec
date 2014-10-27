%global php_apiver	%((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:		%{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir:		%{expand: %%global php_extdir %(php-config --extension-dir)}}

%define pecl_name geoip
%define real_name php-pecl-geoip
%define php_base php56u
%global ini_name  40-%{pecl_name}.ini

Name:		%{php_base}-pecl-geoip
Version:	1.0.8
Release:	7.ius%{?dist}
Summary:	Extension to map IP addresses to geographic places
Group:		Development/Languages
License:	PHP
URL:		http://pecl.php.net/package/%{pecl_name}
Source0:	http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRequires:	GeoIP-devel
BuildRequires:  %{php_base}-devel
BuildRequires:  %{php_base}-pear >= 1:1.4.0
%if 0%{?php_zend_api:1}
Requires:	%{php_base}(zend-abi) = %{php_zend_api}
Requires:	%{php_base}(api) = %{php_core_api}
%else
Requires:	%{php_base}-api = %{php_apiver}
%endif
Requires(post):	%{php_base}-pear
Requires(postun):	%{php_base}-pear

Provides:	php-%{pecl_name} = %{version}
Provides:	php-%{pecl_name}%{?_isa} = %{version}
Provides:	php-pecl(%{pecl_name}) = %{version}
Provides:	php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:	%{php_base}-%{pecl_name} = %{version}
Provides:	%{php_base}-%{pecl_name}%{?_isa} = %{version}
Provides:	%{php_base}-pecl(%{pecl_name}) = %{version}
Provides:	%{php_base}-pecl(%{pecl_name})%{?_isa} = %{version}

Provides:	%{real_name} = %{version}
Conflicts:	%{real_name} < %{version}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}


%description
This PHP extension allows you to find the location of an IP address 
City, State, Country, Longitude, Latitude, and other information as 
all, such as ISP and connection type. It makes use of Maxminds geoip
database


%prep
%setup -c -q
[ -f package2.xml ] || %{__mv} package.xml package2.xml
%{__mv} package2.xml %{pecl_name}-%{version}/%{pecl_name}.xml


%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__make} install INSTALL_ROOT=%{buildroot} INSTALL="install -p"

%{__mkdir_p} %{buildroot}%{php_inidir}
%{__cat} > %{buildroot}%{php_inidir}/%{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -p -m 644 %{pecl_name}.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ]; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%doc %{pecl_name}-%{version}/{README,ChangeLog}
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Fri Oct 24 2014 Ben Harper <ben.harper@rackspace.com> - 1.0.8-7.ius
- porting from php55u-pecl-geoip

* Fri Oct 10 2014 Carl George <carl.george@rackspace.com> - 1.0.8-6.ius
- Conflict with stock package
- Use same provides as stock package

* Mon Oct 06 2014 Carl George <carl.george@rackspace.com> - 1.0.8-5.ius
- Add numerical prefix to extension configuration file
- Add filter to avoid private-shared-object-provides geoip.so

* Fri Dec 06 2013 Ben Harper <ben.harper@rackspace.com> - 1.0.8-4.ius
- porting from php54-pecl-geoip

* Tue Aug 21 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 1.0.8-3.ius
- Rebuilding against php54-5.4.6-2.ius as it is now using bundled PCRE.

* Fri May 11 2012 Dustin Henry Offutt <dustin.offutt@rackspace.com> 1.0.8-2.ius
- Building for php54

* Tue May 01 2012 Dustin Henry Offutt <dustin.offutt@rackspace.com> 1.0.8-1.ius
- Building for GeoIP version 1.0.8

* Wed Mar 28 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 1.0.7-1.ius
- Porting from EPEL to IUS
