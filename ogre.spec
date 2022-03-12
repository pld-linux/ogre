#
# TODO:
#  - unbundle imgui
#  - bconds for the rest of the plugins
#  - subpackages? (Qt library, some plugins?)
#  - package csharp bindings (adjust dirs for mono?)
#	/usr/lib/cli/ogre-sharp-1.12.13/Ogre.dll
#	/usr/lib/cli/ogre-sharp-1.12.13/libOgre.so
#  - GLSL Optimizer: GLSL Optimizer <http://github.com/aras-p/glsl-optimizer/>
#
#
# Conditional build:
%bcond_with	cg		# build with cg
%bcond_with	samples		# build samples (not installed anyway)
%bcond_with	dotnet		# C# support
%bcond_with	java		# Java support
%bcond_without	python		# Python support
%bcond_with	openexr		# OpenEXR plugin

%ifnarch %{ix86} %{x8664} x32
%undefine	with_cg
%endif

%define fver    %(echo %{version} | tr . -)
Summary:	Object-oriented Graphics Rendering Engine
Summary(pl.UTF-8):	OGRE - zorientowany obiektowo silnik renderowania grafiki
Name:		ogre
Version:	13.3.1
Release:	2
License:	MIT
Group:		Applications/Graphics
Source0:	https://github.com/OGRECave/ogre/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	60e71378fb97e4ff37012e9c162dafea
Source1:	https://github.com/ocornut/imgui/archive/v1.85/imgui-1.85.tar.gz
# Source1-md5:	bb710a24164a8dd54369bc4282d9d3b9
Patch0:		%{name}-python.patch
Patch1:		x32.patch
Patch2:		stringstream.patch
URL:		https://www.ogre3d.org/
%{?with_samples:BuildRequires:	CEGUI-devel}
BuildRequires:	FreeImage-devel
%{?with_openexr:BuildRequires:	OpenEXR-devel}
BuildRequires:	OpenGL-devel >= 3.0
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGLESv2-devel >= 2.0
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	SDL2-devel >= 2
BuildRequires:	assimp-devel
BuildRequires:	boost-devel >= 1.40
%{?with_cg:BuildRequires:	cg-devel}
BuildRequires:	cmake >= 2.6.2
BuildRequires:	cppunit-devel >= 1.10.0
BuildRequires:	freetype-devel >= 2.1.0
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRequires:	pugixml-devel
%{?with_python:BuildRequires:	python3-devel >= 1:3.4}
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	swig-python >= 3.0.8
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
Requires:	libstdc++-devel >= 6:4.7
Requires:	zlib-devel
Requires:	zziplib-devel
# libOgrePlatform additionally: XFree86-devel/xorg-lib-libX11-devel OpenGL-GLU-devel

%description devel
This is the package containing the header files for OGRE library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki OGRE.

%package -n python3-ogre
Summary:	Python interface to Ogre library
Summary(pl.UTF-8):	Pythonowy interfejs do biblioteki Ogre
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-ogre
Python interface to Ogre library.

%description -n python3-ogre -l pl.UTF-8
Pythonowy interfejs do biblioteki Ogre.

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
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1

install -d build
%{__mv} imgui-1.85 build/

%build
cd build
# "None" is an alias for release, but uses plain CMAKE_CXX_FLAGS; "PLD" build type is not supported
%cmake .. \
	-DCMAKE_CXX_FLAGS="%{rpmcxxflags}" \
	-DCMAKE_BUILD_TYPE=%{?debug:Debug}%{!?debug:None} \
	%{cmake_on_off dotnet OGRE_BUILD_COMPONENT_CSHARP} \
	%{cmake_on_off java OGRE_BUILD_COMPONENT_JAVA} \
	%{cmake_on_off python OGRE_BUILD_COMPONENT_PYTHON} \
	-DOGRE_BUILD_DEPENDENCIES=FALSE \
	%{cmake_on_off openexr OGRE_BUILD_PLUGIN_EXRCODEC} \
	%{!?with_samples:-DOGRE_BUILD_SAMPLES=FALSE} \
	-DPython_EXECUTABLE:PATH=%{__python3}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr Samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/OGRE

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md Docs/{1.*-Notes.md,ChangeLog.md,License.md}
%attr(755,root,root) %{_bindir}/OgreAssimpConverter
%attr(755,root,root) %{_bindir}/OgreMeshUpgrader
%attr(755,root,root) %{_bindir}/OgreXMLConverter
%attr(755,root,root) %{_bindir}/VRMLConverter
%attr(755,root,root) %{_libdir}/libOgreBites.so.*.*
%attr(755,root,root) %{_libdir}/libOgreBitesQt.so.*.*
%attr(755,root,root) %{_libdir}/libOgreMain.so.*.*
%attr(755,root,root) %{_libdir}/libOgreMeshLodGenerator.so.*.*
%attr(755,root,root) %{_libdir}/libOgreOverlay.so.*.*
%attr(755,root,root) %{_libdir}/libOgrePaging.so.*.*
%attr(755,root,root) %{_libdir}/libOgreProperty.so.*.*
%attr(755,root,root) %{_libdir}/libOgreRTShaderSystem.so.*.*
%attr(755,root,root) %{_libdir}/libOgreTerrain.so.*.*
%attr(755,root,root) %{_libdir}/libOgreVolume.so.*.*
%dir %{_libdir}/OGRE
%attr(755,root,root) %{_libdir}/OGRE/Codec_Assimp.so*
%{?with_openexr:%attr(755,root,root) %{_libdir}/OGRE/Codec_EXR.so*}
%attr(755,root,root) %{_libdir}/OGRE/Codec_FreeImage.so*
%attr(755,root,root) %{_libdir}/OGRE/Codec_STBI.so*
%attr(755,root,root) %{_libdir}/OGRE/Plugin_DotScene.so*
%attr(755,root,root) %{_libdir}/OGRE/Plugin_BSPSceneManager.so*
%if %{with cg}
%attr(755,root,root) %{_libdir}/OGRE/Plugin_CgProgramManager.so*
%endif
%attr(755,root,root) %{_libdir}/OGRE/Plugin_OctreeSceneManager.so*
%attr(755,root,root) %{_libdir}/OGRE/Plugin_OctreeZone.so*
%attr(755,root,root) %{_libdir}/OGRE/Plugin_PCZSceneManager.so*
%attr(755,root,root) %{_libdir}/OGRE/Plugin_ParticleFX.so*
%attr(755,root,root) %{_libdir}/OGRE/RenderSystem_GL.so*
%attr(755,root,root) %{_libdir}/OGRE/RenderSystem_GL3Plus.so*
%attr(755,root,root) %{_libdir}/OGRE/RenderSystem_GLES2.so*
%dir %{_datadir}/OGRE
%{_datadir}/OGRE/*.cfg
%{_datadir}/OGRE/*.png
%{_datadir}/OGRE/Media

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOgreBites.so
%attr(755,root,root) %{_libdir}/libOgreBitesQt.so
%attr(755,root,root) %{_libdir}/libOgreMain.so
%attr(755,root,root) %{_libdir}/libOgreMeshLodGenerator.so
%attr(755,root,root) %{_libdir}/libOgreOverlay.so
%attr(755,root,root) %{_libdir}/libOgrePaging.so
%attr(755,root,root) %{_libdir}/libOgreProperty.so
%attr(755,root,root) %{_libdir}/libOgreRTShaderSystem.so
%attr(755,root,root) %{_libdir}/libOgreTerrain.so
%attr(755,root,root) %{_libdir}/libOgreVolume.so
%{_includedir}/OGRE
%{_pkgconfigdir}/OGRE.pc
%{_pkgconfigdir}/OGRE-Bites.pc
%{_pkgconfigdir}/OGRE-MeshLodGenerator.pc
%{_pkgconfigdir}/OGRE-Overlay.pc
%{_pkgconfigdir}/OGRE-Paging.pc
%{_pkgconfigdir}/OGRE-PCZ.pc
%{_pkgconfigdir}/OGRE-Property.pc
%{_pkgconfigdir}/OGRE-RTShaderSystem.pc
%{_pkgconfigdir}/OGRE-Terrain.pc
%{_pkgconfigdir}/OGRE-Volume.pc
%{_libdir}/OGRE/cmake

%if %{with python}
%files -n python3-ogre
%defattr(644,root,root,755)
%dir %{py3_sitedir}/Ogre
%attr(755,root,root) %{py3_sitedir}/Ogre/*.so
%{py3_sitedir}/Ogre/*.py
%{py3_sitedir}/Ogre/__pycache__
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
