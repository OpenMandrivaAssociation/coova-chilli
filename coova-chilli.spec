%define	major 0
%define libname	%mklibname chilli %{major}
%define develname %mklibname -d chilli

Summary:	Wireless LAN Access Point Controller
Name:		coova-chilli
Version:	1.0.13
Release:	%mkrel 1
License:	GPLv2
Group:		System/Servers
URL:		http://coova.org/wiki/index.php/CoovaChilli
Source0:	http://ap.coova.org/chilli/%{name}-%{version}.tar.gz
Patch0:		coova-chilli-1.0.12-linkage_fix.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	autoconf
BuildRequires:	libtool
Provides:	chillispot = %{version}-%{release}
Obsoletes:	chillispot
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
Coova-Chilli is a fork of the ChilliSpot project - an open source captive
portal or wireless LAN access point controller. It supports web based login
(Universal Access Method, or UAM), standard for public HotSpots, and it
supports Wireless Protected Access (WPA), the standard for secure roamable
networks. Authentication, Authorization and Accounting (AAA) is handled by
your favorite radius server. Read more at http://coova.org/ and
http://www.chillispot.org/.

%package -n	%{libname}
Summary:	Shared libraries for %{name}
Group:          System/Libraries

%description -n	%{libname}
Coova-Chilli is a fork of the ChilliSpot project - an open source captive
portal or wireless LAN access point controller. It supports web based login
(Universal Access Method, or UAM), standard for public HotSpots, and it
supports Wireless Protected Access (WPA), the standard for secure roamable
networks. Authentication, Authorization and Accounting (AAA) is handled by
your favorite radius server. Read more at http://coova.org/ and
http://www.chillispot.org/.

This package contains the shared libraries for %{name}.

%package -n	%{develname}
Summary:	Static library and header files for the %{name} library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{develname}
Coova-Chilli is a fork of the ChilliSpot project - an open source captive
portal or wireless LAN access point controller. It supports web based login
(Universal Access Method, or UAM), standard for public HotSpots, and it
supports Wireless Protected Access (WPA), the standard for secure roamable
networks. Authentication, Authorization and Accounting (AAA) is handled by
your favorite radius server. Read more at http://coova.org/ and
http://www.chillispot.org/.

This package contains the static %{name} library and its header files.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0

# fix strange perms
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
# cleanup cvs junk
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
autoreconf -fis
%serverbuild

%configure2_5x \
    --enable-static-exec

%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_initrddir}
mv %{buildroot}%{_sysconfdir}/init.d/chilli %{buildroot}%{_initrddir}/chilli

%post
%_post_service chilli

%preun
%_preun_service chilli

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README doc/dictionary.chillispot doc/hotspotlogin.cgi
%attr(0755,root,root) %{_initrddir}/chilli
%attr(0644,root,root) %config %{_sysconfdir}/chilli.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/chilli/defaults
%dir %{_sysconfdir}/chilli
%dir %{_sysconfdir}/chilli/www
%attr(0755,root,root) %{_sysconfdir}/chilli/www/config.sh
%{_sysconfdir}/chilli/www/*
%{_sysconfdir}/chilli/wwwsh
%{_sysconfdir}/chilli/functions
%{_sysconfdir}/chilli/*.sh
%attr(0755,root,root) %{_sbindir}/chilli
%attr(0755,root,root) %{_sbindir}/chilli_query
%attr(0755,root,root) %{_sbindir}/chilli_radconfig
%attr(0755,root,root) %{_sbindir}/chilli_response
%attr(0755,root,root) %{_sbindir}/test_radius
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la

