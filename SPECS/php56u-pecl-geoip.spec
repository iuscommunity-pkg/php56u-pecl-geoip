%define pecl_name geoip
%define php_base php56u
%global ini_name 40-%{pecl_name}.ini

Name: %{php_base}-pecl-geoip
Version: 1.0.8
Release: 8.ius%{?dist}
Summary: Extension to map IP addresses to geographic places
Group: Development/Languages
License: PHP
URL: http://pecl.php.net/package/%{pecl_name}
Source0: http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRequires: GeoIP-devel
BuildRequires: %{php_base}-devel
BuildRequires: %{php_base}-pear >= 1:1.4.0
Requires: %{php_base}(zend-abi) = %{php_zend_api}
Requires: %{php_base}(api) = %{php_core_api}
Requires(post): %{php_base}-pear
Requires(postun): %{php_base}-pear

# provide the stock name
Provides: php-pecl-%{pecl_name} = %{version}
Provides: php-pecl-%{pecl_name}%{?_isa} = %{version}

# provide the stock and IUS names without pecl
Provides: php-%{pecl_name} = %{version}
Provides: php-%{pecl_name}%{?_isa} = %{version}
Provides: %{php_base}-%{pecl_name} = %{version}
Provides: %{php_base}-%{pecl_name}%{?_isa} = %{version}

# provide the stock and IUS names in pecl() format
Provides: php-pecl(%{pecl_name}) = %{version}
Provides: php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides: %{php_base}-pecl(%{pecl_name}) = %{version}
Provides: %{php_base}-pecl(%{pecl_name})%{?_isa} = %{version}

# conflict with the stock name
Conflicts: php-pecl-%{pecl_name} < %{version}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


%description
This PHP extension allows you to find the location of an IP address 
City, State, Country, Longitude, Latitude, and other information as 
all, such as ISP and connection type. It makes use of Maxminds geoip
database


%prep
%setup -c -q


%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}


%install
pushd %{pecl_name}-%{version}
%{__make} install INSTALL_ROOT=%{buildroot} INSTALL="install -p"

%{__mkdir_p} %{buildroot}%{php_inidir}
%{__cat} > %{buildroot}%{php_inidir}/%{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF
popd

%{__install} -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :
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
%{pecl_xmldir}/%{pecl_name}.xml


%changelog
* Wed Mar 16 2016 Carl George <carl.george@rackspace.com> - 1.0.8-8.ius
- Clean up provides
- Clean up filters
- Install package.xml as %%{pecl_name}.xml, not %%{name}.xml

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

* Mon Mar 28 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> 1.0.7-1.ius
- Porting from EPEL to IUS
