#
# TODO:
#  - bconds for the rest of the plugins
#  - package csharp and python bindings
#
# Conditional build:
%bcond_with	cg		# build with cg
%bcond_with	samples		# build samples (not installed anyway)

%ifnarch %{ix86} %{x8664} x32
%undefine	with_cg
%endif

%define fver    %(echo %{version} | tr . -)
Summary:	Object-oriented Graphics Rendering Engine
Summary(pl.UTF-8):	OGRE - zorientowany obiektowo silnik renderowania grafiki
Name:		ogre
Version:	1.12.2
Release:	1
License:	MIT
Group:		Applications
Source0:	https://github.com/OGRECave/ogre/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6a1187615abb0eee5c658578da9cf001
Patch1:		x32.patch
URL:		http://www.ogre3d.org/
%{?with_samples:BuildRequires:	CEGUI-devel}
BuildRequires:	FreeImage-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	boost-devel >= 1.40
%{?with_cg:BuildRequires:	cg-devel}
BuildRequires:	cmake >= 2.6.2
BuildRequires:	cppunit-devel >= 1.10.0
BuildRequires:	freetype-devel >= 2.1.0
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	pugixml-devel
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	tinyxml-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXt-devel
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
BuildArch:	noarch

%description examples
OGRE samples.

%description examples -l pl.UTF-8
Przykłady do OGRE.

%prep
%setup -q
%patch1 -p1

%build

install -d build
cd build
# "None" is an alias for release, but uses plain CMAKE_CXX_FLAGS; "PLD" build type is not supported
%cmake .. \
	-DCMAKE_CXX_FLAGS="%{rpmcxxflags}" \
	-DCMAKE_BUILD_TYPE=%{?debug:Debug}%{!?debug:None} \
	-DOGRE_BUILD_DEPENDENCIES=FALSE \
	%{!?with_samples:-DOGRE_BUILD_SAMPLES=FALSE}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr Samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_bindir}/OgreMeshUpgrader
%attr(755,root,root) %{_bindir}/OgreXMLConverter
%attr(755,root,root) %{_bindir}/VRMLConverter
%attr(755,root,root) %{_libdir}/libOgreBites.so.*.*.*
%attr(755,root,root) %{_libdir}/libOgreHLMS.so.*.*.*
%attr(755,root,root) %{_libdir}/libOgreMain.so.*.*.*
%attr(755,root,root) %{_libdir}/libOgreMeshLodGenerator.so.*.*.*
%attr(755,root,root) %{_libdir}/libOgreOverlay.so.*.*.*
%attr(755,root,root) %{_libdir}/libOgrePaging.so.*.*.*
%attr(755,root,root) %{_libdir}/libOgreProperty.so.*.*.*
%attr(755,root,root) %{_libdir}/libOgreRTShaderSystem.so.*.*.*
%attr(755,root,root) %{_libdir}/libOgreTerrain.so.*.*.*
%attr(755,root,root) %{_libdir}/libOgreVolume.so.*.*.*
%dir %{_libdir}/OGRE
%attr(755,root,root) %{_libdir}/OGRE/Codec_EXR.so*
%attr(755,root,root) %{_libdir}/OGRE/Codec_FreeImage.so*
%attr(755,root,root) %{_libdir}/OGRE/Codec_STBI.so*
%attr(755,root,root) %{_libdir}/OGRE/Plugin_DotScene.so*
%attr(755,root,root) %{_libdir}/OGRE/RenderSystem_GL3Plus.so*
%attr(755,root,root) %{_libdir}/OGRE/Plugin_BSPSceneManager.so*
%if %{with cg}
%attr(755,root,root) %{_libdir}/OGRE/Plugin_CgProgramManager.so*
%endif
%attr(755,root,root) %{_libdir}/OGRE/Plugin_OctreeSceneManager.so*
%attr(755,root,root) %{_libdir}/OGRE/Plugin_OctreeZone.so*
%attr(755,root,root) %{_libdir}/OGRE/Plugin_PCZSceneManager.so*
%attr(755,root,root) %{_libdir}/OGRE/Plugin_ParticleFX.so*
%attr(755,root,root) %{_libdir}/OGRE/RenderSystem_GL.so*
%dir %{_datadir}/OGRE
%{_datadir}/OGRE/*.cfg
%{_datadir}/OGRE/*.png
%{_datadir}/OGRE/Media

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOgreMain.so
%attr(755,root,root) %{_libdir}/libOgrePaging.so
%attr(755,root,root) %{_libdir}/libOgreProperty.so
%attr(755,root,root) %{_libdir}/libOgreRTShaderSystem.so
%attr(755,root,root) %{_libdir}/libOgreTerrain.so
%attr(755,root,root) %{_libdir}/libOgreBites.so
%attr(755,root,root) %{_libdir}/libOgreHLMS.so
%attr(755,root,root) %{_libdir}/libOgreMeshLodGenerator.so
%attr(755,root,root) %{_libdir}/libOgreOverlay.so
%attr(755,root,root) %{_libdir}/libOgreVolume.so
%{_libdir}/libOgreGLSupport.a
%{_includedir}/OGRE
%{_pkgconfigdir}/OGRE.pc
%{_pkgconfigdir}/OGRE-Bites.pc
%{_pkgconfigdir}/OGRE-HLMS.pc
%{_pkgconfigdir}/OGRE-MeshLodGenerator.pc
%{_pkgconfigdir}/OGRE-Overlay.pc
%{_pkgconfigdir}/OGRE-Paging.pc
%{_pkgconfigdir}/OGRE-PCZ.pc
%{_pkgconfigdir}/OGRE-Property.pc
%{_pkgconfigdir}/OGRE-RTShaderSystem.pc
%{_pkgconfigdir}/OGRE-Terrain.pc
%{_pkgconfigdir}/OGRE-Volume.pc
%{_libdir}/OGRE/cmake

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
