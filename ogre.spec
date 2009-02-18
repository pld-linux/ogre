# TODO:
# - better fix for --as-needed (im too stupid to fix this in a correct way:/)
#
# Conditional build:
%bcond_with	cg		# build with cg

%ifnarch %{ix86} %{x8664}
%undefine	with_cg
%endif

%define _ver    %(echo %{version} | tr . -)
Summary:	Object-oriented Graphics Rendering Engine
Summary(pl.UTF-8):	OGRE - zorientowany obiektowo silnik renderowania grafiki
Name:		ogre
Version:	1.6.1
Release:	0.3
License:	LGPL
Group:		Applications
Source0:	http://dl.sourceforge.net/ogre/%{name}-v%{_ver}.tar.bz2
# Source0-md5:	6fbd72e81dd4c135a2cc4f78d596aeb4
URL:		http://www.ogre3d.org/
BuildRequires:	CEGUI-devel
BuildRequires:	FreeImage-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_cg:BuildRequires:	cg-devel}
BuildRequires:	cppunit-devel >= 1.10.0
BuildRequires:	freetype-devel >= 2.1.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-xf86vidmodeproto-devel
BuildRequires:	zlib-devel
BuildRequires:	zziplib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         filterout_ld    -Wl,--as-needed

%description
Object-oriented Graphics Rendering Engine.

%description -l pl.UTF-8
OGRE - zorientowany obiektowo silnik renderowania grafiki

%package devel
Summary:	Header files for OGRE library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OGRE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	FreeImage-devel
Requires:	freetype-devel >= 2.1.0
Requires:	libstdc++-devel
Requires:	zlib-devel
Requires:	zziplib-devel
# libOgrePlatform additionally: XFree86-devel/xorg-lib-libX11-devel OpenGL-GLU-devel

%description devel
This is the package containing the header files for OGRE library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki OGRE.

%package examples
Summary:	OGRE samples
Summary(pl.UTF-8):	Przykłady do OGRE
Group:		Applications

%description examples
OGRE samples.

%description examples -l pl.UTF-8
Przykłady do OGRE.

%prep
%setup -q -n %{name}

find -name CVS -print0 | xargs -0 rm -rf

sed -i -e 's,"-L/usr/X11R6/lib ,"-L/usr/X11R6/%{_lib} ,' acinclude.m4

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_cg:--enable-cg} \
	--disable-devil \
	--enable-openexr

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
%attr(755,root,root) %{_libdir}/libOgre*.so
%attr(755,root,root) %{_libdir}/libCEGUIOgre*.so
%dir %{_libdir}/OGRE
%attr(755,root,root) %{_libdir}/OGRE/Plugin_BSPSceneManager.so
%attr(755,root,root) %{_libdir}/OGRE/Plugin_EXRCodec.so
%attr(755,root,root) %{_libdir}/OGRE/Plugin_OctreeSceneManager.so
%attr(755,root,root) %{_libdir}/OGRE/Plugin_ParticleFX.so
%attr(755,root,root) %{_libdir}/OGRE/RenderSystem_GL.so
%{?with_cg:%attr(755,root,root) %{_libdir}/OGRE/Plugin_CgProgramManager.so}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOgre*.so
%attr(755,root,root) %{_libdir}/libCEGUIOgre*.so
%{_libdir}/libOgreMain.la
%{_libdir}/libCEGUIOgreRenderer.la
%{_includedir}/OGRE
%{_pkgconfigdir}/OGRE.pc
%{_pkgconfigdir}/CEGUI-OGRE.pc

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
