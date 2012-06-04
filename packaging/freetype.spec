Name:       freetype
Summary:    A free and portable font rendering engine
Version:    2.4.9
Release:    1
Group:      System/Libraries
License:    FTL or GPLv2+
URL:        http://www.freetype.org
Source0:    http://download.savannah.gnu.org/releases-noredirect/freetype/freetype-%{version}.tar.bz2
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:   %{name}-bytecode


%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.



%package devel
Summary:    FreeType development libraries and header files
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   zlib-devel
Requires:   pkgconfig

%description devel
The freetype-devel package includes the static libraries and header files
for the FreeType font rendering engine.

Install freetype-devel if you want to develop programs which will use
FreeType.



%prep
%setup -q

%build

%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' builds/unix/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' builds/unix/libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%makeinstall gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale


# fix multilib issues
%ifarch x86_64 s390x ia64 ppc64 alpha sparc64
%define wordsize 64
%else
%define wordsize 32
%endif

mv $RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig.h \
$RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig-%{wordsize}.h
cat >$RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig.h <<EOF
#ifndef __FTCONFIG_H__MULTILIB
#define __FTCONFIG_H__MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "ftconfig-32.h"
#elif __WORDSIZE == 64
# include "ftconfig-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

# Don't package static a or .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libfreetype.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/freetype2
%{_datadir}/aclocal/freetype2.m4
%{_includedir}/freetype2/*
%{_includedir}/*.h
%{_libdir}/libfreetype.so
%{_bindir}/freetype-config
%{_libdir}/pkgconfig/*.pc

