%define 	_rc	RC1
%define 	_rel	1
Summary:	Object-oriented Graphics Rendering Engine
Summary(pl):	OGRE - zorientowany obiektowo silnik renderowania grafiki
Name:		ogre
Version:	1.2.0
Release:	0.%{_rc}.%{_rel}
License:	LGPL
Group:		Applications
Source0:	http://dl.sourceforge.net/ogre/%{name}-linux_osx-v1-2-0%{_rc}.tar.bz2
# Source0-md5:	23e17ef81f1d7e159c0ba626a27c7681
URL:		http://www.ogre3d.org/
BuildRequires:	DevIL-devel >= 1.6.7
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	XFree86-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	cppunit-devel >= 1.10.0
BuildRequires:	freetype-devel >= 2.1.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
# X11R7: xorg-lib-libXt-devel xorg-lib-libXaw-devel xorg-lib-libXrandr-devel
BuildRequires:	zlib-devel
BuildRequires:	zziplib-devel
# OpenEXR-devel (disabled by default)
# CEGUI >= 0.3.0 ???
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Object-oriented Graphics Rendering Engine.

%description -l pl
OGRE - zorientowany obiektowo silnik renderowania grafiki

%package devel
Summary:	Header files for OGRE library
Summary(pl):	Pliki nag��wkowe biblioteki OGRE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	DevIL-devel >= 1.6.7
Requires:	freetype-devel >= 2.1.0
Requires:	libstdc++-devel
Requires:	zlib-devel
Requires:	zziplib-devel
# libOgrePlatform additionally: XFree86-devel/xorg-lib-libX11-devel OpenGL-GLU-devel

%description devel
This is the package containing the header files for OGRE library.

%description devel -l pl
Ten pakiet zawiera pliki nag��wkowe biblioteki OGRE.

%package examples
Summary:	OGRE samples
Summary(pl):	Przyk�ady do OGRE
Group:		Applications

%description examples
OGRE samples.

%description examples -l pl
Przyk�ady do OGRE.

%prep
%setup -q -n %{name}new

find -name CVS -print0 | xargs -0 rm -rf

sed -i -e 's,"-L/usr/X11R6/lib ,"-L/usr/X11R6/%{_lib} ,' acinclude.m4
# X11R7
#sed -i -e 's,"-L/usr/X11R6/lib ,",' acinclude.m4
#sed -i -e 's,="-I/usr/X11R6/include",=,' acinclude.m4

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

rm -f $RPM_BUILD_ROOT%{_libdir}/OGRE/*.la

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
%attr(755,root,root) %{_libdir}/OGRE/*.so

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
