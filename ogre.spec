#
# TODO: - --enable-ogre-demos?
#	- enable static libs
#	- check if cmake use our flags
#	- check BRs
#
# Conditional build:
%bcond_with	cg		# build with cg

%ifnarch %{ix86} %{x8664}
%undefine	with_cg
%endif

%define	_rc	RC1
%define _ver    %(echo %{version} | tr . -)
Summary:	Object-oriented Graphics Rendering Engine
Summary(pl.UTF-8):	OGRE - zorientowany obiektowo silnik renderowania grafiki
Name:		ogre
Version:	1.7.0
Release:	0.%{_rc}.1
License:	LGPL
Group:		Applications
Source0:	http://dl.sourceforge.net/ogre/%{name}-v%{_ver}%{_rc}.tar.bz2
# Source0-md5:	d6c69a7b52b633cebc74b30c11954825
URL:		http://www.ogre3d.org/
BuildRequires:	CEGUI-devel
BuildRequires:	FreeImage-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-GLU-devel
%{?with_cg:BuildRequires:	cg-devel}
BuildRequires:	cmake
BuildRequires:	cppunit-devel >= 1.10.0
BuildRequires:	freetype-devel >= 2.1.0
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xorg-proto-xf86vidmodeproto-devel
BuildRequires:	zlib-devel
BuildRequires:	zziplib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
mkdir build && cd build
%cmake .. \
	-DCMAKE_INSTALL_PREFIX="%{_prefix}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr Samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/OGRE/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
#%defattr(644,root,root,755)
#%doc AUTHORS BUGS README INSTALL
%attr(755,root,root) %{_bindir}/Ogre*
#%%attr(755,root,root) %{_bindir}/rcapsdump
%dir %{_libdir}/OGRE
%attr(755,root,root) %{_libdir}/OGRE/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOgre*.so
#%attr(755,root,root) %{_libdir}/libCEGUIOgre*.so
#%{_libdir}/libOgreMain.la
#%{_libdir}/libCEGUIOgreRenderer.la
%{_includedir}/OGRE
%{_pkgconfigdir}/OGRE.pc
%{_pkgconfigdir}/OGRE-PCZ.pc
%{_pkgconfigdir}/OGRE-Paging.pc

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
