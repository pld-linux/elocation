#
# Conditional build:
%bcond_without	apidocs		# API docs
%bcond_without	static_libs	# static library
#
Summary:	Enlightenment location library
Summary(pl.UTF-8):	Biblioteka lokalizacji dla środowiska Enlightenment
Name:		elocation
Version:	0.1.0
%define	snap	20130813
Release:	0.%{snap}.1
License:	unknown
Group:		Libraries
# git clone http://git.enlightenment.org/devs/stefan/elocation.git
Source0:	%{name}.tar.xz
# Source0-md5:	1710301b6bc0f2e38e4b057a059380e3
URL:		http://git.enlightenment.org/devs/stefan/elocation.git/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
BuildRequires:	ecore-devel
BuildRequires:	eldbus-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Elocation is a small library that allows application to get some basic
location awareness if this is supported on the platform.

%description -l pl.UTF-8
Elocation to mała biblioteka pozwalająca aplikacjom uzyskać pewne
podstawoe informacje o położeniu, jeśli jest to obsługiwane przez
platformę.

%package devel
Summary:	Header files for Elocation library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Elocation
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ecore-devel
Requires:	eldbus-devel

%description devel
Header files for Elocation library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Elocation.

%package static
Summary:	Static Elocation library
Summary(pl.UTF-8):	Statyczna biblioteka Elocation
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Elocation library.

%description static -l pl.UTF-8
Statyczna biblioteka Elocation.

%package apidocs
Summary:	API documentation for Elocation library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Elocation
Group:		Documentation

%description apidocs
API documentation for Elocation library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Elocation.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with apidocs}
%{__make} -C doc doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libelocation.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/elocation-test
%attr(755,root,root) %{_libdir}/libelocation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelocation.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libelocation.so
%{_includedir}/elocation-0
%{_pkgconfigdir}/elocation.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libelocation.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
