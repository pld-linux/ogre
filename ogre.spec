# TODO
# - unify ogre caps
%define 	_rc	RC1
%define 	_rel 0.1
Summary:	Ogre
Summary(pl):	Ogre
Name:		ogre
Version:	1.2.0
Release:	%{_rc}.%{_rel}
License:	LGPL
Group:		Applications
Source0:	http://dl.sourceforge.net/ogre/%{name}-linux_osx-v1-2-0%{_rc}.tar.bz2
# Source0-md5:	23e17ef81f1d7e159c0ba626a27c7681
#Patch0: %{name}-DESTDIR.patch
URL:		http://www.ogre3d.org/
BuildRequires:	DevIL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	zziplib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OGRE Library

%package examples
Summary:	ogre samples
Group:		Examples
######		Unknown group!

%description examples
OGRE samples

%package devel
Summary:	Header files for OGRE library
Summary(pl):	Pliki nag³ówkowe biblioteki OGRE
Group:		Development/Libraries
#Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for OGRE library.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe biblioteki OGRE

%prep
%setup -q -n %{name}new
#%patch0 -p1

find -name CVS -print0 | xargs -0 rm -rf

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cp -f /usr/share/automake/config.sub .
%configure \
	--disable-cg

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr Samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS README INSTALL
%attr(755,root,root) %{_libdir}/libOgre*so*
%attr(755,root,root) %{_bindir}/Ogre*

%files devel
%defattr(644,root,root,755)
%doc Docs/*
%dir %{_includedir}/OGRE
%{_includedir}/OGRE/*.h
%{_pkgconfigdir}/OGRE.pc
%dir %{_libdir}/OGRE
%{_libdir}/OGRE/*so

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
