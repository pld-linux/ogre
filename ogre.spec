%define 	_rc	RC1
Summary:	Object-oriented Graphics Rendering Engine
Summary(pl):	OGRE - zorientowany obiektowo silnik renderowania grafiki
Name:		ogre
Version:	1.2.0
Release:	0.%{_rc}.1
License:	LGPL
Group:		Applications
Source0:	http://dl.sourceforge.net/ogre/%{name}-linux_osx-v1-2-0%{_rc}.tar.bz2
# Source0-md5:	23e17ef81f1d7e159c0ba626a27c7681
URL:		http://www.ogre3d.org/
BuildRequires:	DevIL-devel >= 1.6.7
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	zziplib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Object-oriented Graphics Rendering Engine.

%description -l Pl
OGRE - zorientowany obiektowo silnik renderowania grafiki

%package devel
Summary:	Header files for OGRE library
Summary(pl):	Pliki nag³ówkowe biblioteki OGRE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for OGRE library.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe biblioteki OGRE.

%package examples
Summary:	OGRE samples
Summary(pl):	Przyk³ady do OGRE
Group:		Applications

%description examples
OGRE samples.

%description examples -l pl
Przyk³ady do OGRE.

%prep
%setup -q -n %{name}new

find -name CVS -print0 | xargs -0 rm -rf

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-cg

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr Samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS README INSTALL
%attr(755,root,root) %{_bindir}/Ogre*
%attr(755,root,root) %{_libdir}/libOgre*.so.*.*.*
%dir %{_libdir}/OGRE
%attr(755,root,root) %{_libdir}/OGRE/*so
# needed or drop?
%{_libdir}/OGRE/Plugin_*.la
%{_libdir}/OGRE/RenderSystem_GL.la

%files devel
%defattr(644,root,root,755)
%doc Docs/*
%attr(755,root,root) %{_libdir}/libOgre*.so
%{_libdir}/libOgre*.la
%{_includedir}/OGRE
%{_pkgconfigdir}/OGRE.pc

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
