Name:           freetype2
BuildRequires:  pkg-config
BuildRequires:  zlib-devel
Version:        2.4.9
Release:        0
Summary:        A TrueType Font Library
License:        Freetype or GPL-2.0+
Group:          Graphics/Font Management
Url:            http://www.freetype.org
Source0:        http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	freetype2.manifest

%description
This library features TrueType fonts for open source projects. This
version also contains an autohinter for producing improved output.

%package -n libfreetype
Summary:        A TrueType Font Library
Group:          Graphics/Font Management

%description -n libfreetype
This library features TrueType fonts for open source projects. This
version also contains an autohinter for producing improved output.

%package devel
Summary:        Development environment for the freetype2 TrueType font library
Group:          Development/Libraries
Requires:       libfreetype = %{version}
Requires:       zlib-devel
Provides:       freetype-devel

%description devel
This package contains all necessary include files, libraries and
documentation needed to develop applications that require the freetype2
TrueType font library.

It also contains a small tutorial for using that library.

%prep
%define enable_subpixel_rendering 0
%setup -q -n freetype-%{version} 
cp %{SOURCE1001} .

%build
export CFLAGS="%optflags -std=gnu99 -D_GNU_SOURCE"
%configure --without-bzip2 \
           --disable-static
make %{?_smp_mflags}

%install
%make_install

rm docs/INSTALL*

%post -n libfreetype -p /sbin/ldconfig

%postun -n libfreetype -p /sbin/ldconfig

%files -n libfreetype
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libfreetype.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libfreetype.so
%{_libdir}/pkgconfig/freetype2.pc
%{_bindir}/*
%{_datadir}/aclocal

%changelog
