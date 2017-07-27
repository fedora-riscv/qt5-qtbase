# See http://bugzilla.redhat.com/223663
%global multilib_archs x86_64 %{ix86} %{?mips} ppc64 ppc s390x s390 sparc64 sparcv9
%global multilib_basearchs x86_64 %{?mips64} ppc64 s390x sparc64

# support openssl-1.1
%global openssl11 1
%global openssl -openssl-linked

# support qtchooser (adds qtchooser .conf file)
%global qtchooser 1
%if 0%{?qtchooser}
%global priority 10
%ifarch %{multilib_basearchs}
%global priority 15
%endif
%endif

%global platform linux-g++

%if 0%{?use_clang}
%global platform linux-clang
%endif

%global qt_module qtbase

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

%if 0%{?fedora} > 21
# use external qt_settings pkg
%global qt_settings 1
%endif

# See http://bugzilla.redhat.com/1279265
%if 0%{?fedora} < 24
%global inject_optflags 1
%endif

%if 0%{?fedora} > 23 || 0%{?rhel} > 6
%global journald -journald
BuildRequires: pkgconfig(libsystemd)
%endif

%if 0%{?fedora} > 23
# gcc6: FTBFS
%global qt5_deprecated_flag -Wno-deprecated-declarations
# gcc6: Qt assumes this in places
%global qt5_null_flag -fno-delete-null-pointer-checks
%endif

%global examples 1
%global tests 1

Name:    qt5-qtbase
Summary: Qt5 - QtBase components
Version: 5.9.1
Release: 3%{?dist}

# See LGPL_EXCEPTIONS.txt, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://qt-project.org/
Source0: https://download.qt.io/official_releases/qt/5.9/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

# https://bugzilla.redhat.com/show_bug.cgi?id=1227295
Source1: qtlogging.ini

# header file to workaround multilib issue
# https://bugzilla.redhat.com/show_bug.cgi?id=1036956
Source5: qconfig-multilib.h

# xinitrc script to check for OpenGL 1 only drivers and automatically set
# QT_XCB_FORCE_SOFTWARE_OPENGL for them
Source6: 10-qt5-check-opengl2.sh

# macros
Source10: macros.qt5-qtbase

# support multilib optflags
Patch2: qtbase-multilib_optflags.patch

# fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
Patch4: qtbase-opensource-src-5.3.2-QTBUG-35459.patch

# upstreamable patches
# namespace QT_VERSION_CHECK to workaround major/minor being pre-defined (#1396755)
Patch50: qtbase-opensource-src-5.8.0-QT_VERSION_CHECK.patch

# 1381828 - Broken window scaling for some QT5 applications (#1381828)
# This patch moves the threshold for 2x scaling from the DPI of 144 to 192,
# the same value GNOME uses. It's not a complete solution...
Patch51: qtbase-hidpi_scale_at_192.patch

# 1. Workaround moc/multilib issues
# https://bugzilla.redhat.com/show_bug.cgi?id=1290020
# https://bugreports.qt.io/browse/QTBUG-49972
# 2. Workaround sysmacros.h (pre)defining major/minor a breaking stuff
Patch52: qtbase-opensource-src-5.7.1-moc_macros.patch

# drop -O3 and make -O2 by default
Patch61: qt5-qtbase-cxxflag.patch

# backport from upstream
Patch63: qt5-qtbase-5.9.1-openssl11.patch

# support firebird version 3.x
Patch64: qt5-qtbase-5.9.1-firebird.patch

# fix for new mariadb
Patch65: qtbase-opensource-src-5.9.0-mysql.patch

## upstream patches (5.9 branch)
Patch486: 0086-Fix-detection-of-AT-SPI.patch

# Do not check any files in %%{_qt5_plugindir}/platformthemes/ for requires.
# Those themes are there for platform integration. If the required libraries are
# not there, the platform to integrate with isn't either. Then Qt will just
# silently ignore the plugin that fails to load. Thus, there is no need to let
# RPM drag in gtk3 as a dependency for the GTK+3 dialog support.
%global __requires_exclude_from ^%{_qt5_plugindir}/platformthemes/.*$
# filter plugin provides
%global __provides_exclude_from ^%{_qt5_plugindir}/.*\\.so$

BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(alsa)
# required for -accessibility
BuildRequires: pkgconfig(atspi-2)
%if 0%{?use_clang}
BuildRequires: clang >= 3.7.0
%endif
# http://bugzilla.redhat.com/1196359
%if 0%{?fedora} || 0%{?rhel} > 6
%global dbus -dbus-linked
BuildRequires: pkgconfig(dbus-1)
%endif
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libproxy-1.0)
# xcb-sm
BuildRequires: pkgconfig(ice) pkgconfig(sm)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libudev)
BuildRequires: openssl-devel
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
%if 0%{?fedora}
%global xkbcommon -system-xkbcommon
BuildRequires: pkgconfig(libinput)
BuildRequires: pkgconfig(xcb-xkb) >= 1.10
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1
BuildRequires: pkgconfig(xkbcommon-x11) >= 0.4.1
%else
# not Fedora
%if 0%{?rhel} == 6
%global xcb -qt-xcb
%endif
%global xkbcommon -qt-xkbcommon
Provides: bundled(libxkbcommon) = 0.4.1
%endif
BuildRequires: pkgconfig(xkeyboard-config)
%if 0%{?fedora} || 0%{?rhel} > 6
%global egl 1
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(glesv2)
%global sqlite -system-sqlite
BuildRequires: pkgconfig(sqlite3) >= 3.7
%if 0%{?fedora} > 22
%global harfbuzz -system-harfbuzz
BuildRequires: pkgconfig(harfbuzz) >= 0.9.42
%endif
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(libpcre2-posix) >= 10.20
BuildRequires: pkgconfig(libpcre) >= 8.0
%global pcre -system-pcre
BuildRequires: pkgconfig(xcb-xkb)
%else
BuildRequires: libicu-devel
%global pcre -qt-pcre
%endif
BuildRequires: pkgconfig(xcb) pkgconfig(xcb-glx) pkgconfig(xcb-icccm) pkgconfig(xcb-image) pkgconfig(xcb-keysyms) pkgconfig(xcb-renderutil)
BuildRequires: pkgconfig(zlib)
BuildRequires: perl-generators
BuildRequires: qt5-rpm-macros >= 5.7.1

%if 0%{?tests}
BuildRequires: dbus-x11
BuildRequires: mesa-dri-drivers
BuildRequires: time
BuildRequires: xorg-x11-server-Xvfb
%endif

%if 0%{?qtchooser}
%if 0%{?fedora}
Conflicts: qt < 1:4.8.6-10
%endif
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%endif
%if 0%{?qt_settings}
Requires: qt-settings
%endif
Requires: %{name}-common = %{version}-%{release}

## Sql drivers
%if 0%{?rhel}
%global ibase -no-sql-ibase
%global tds -no-sql-tds
%endif

# workaround gold linker bug by not using it
# https://bugzilla.redhat.com/1458003
# https://sourceware.org/bugzilla/show_bug.cgi?id=21074
%if 0%{?fedora} > 26
%global use_gold_linker -no-use-gold-linker
%endif

%description
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package common
Summary: Common files for Qt5
# offer upgrade path for qtquick1 somewhere... may as well be here -- rex
Obsoletes: qt5-qtquick1 < 5.9.0
Obsoletes: qt5-qtquick1-devel < 5.9.0
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Provides: %{name}-private-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-gui%{?_isa}
%if 0%{?egl}
Requires: pkgconfig(egl)
%endif
Requires: pkgconfig(gl)
Requires: qt5-rpm-macros >= 5.7.1
%if 0%{?use_clang}
Requires: clang >= 3.7.0
%endif
%description devel
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description examples
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig(fontconfig)
Requires: pkgconfig(glib-2.0)
%if 0%{?fedora}
Requires: pkgconfig(libinput)
Requires: pkgconfig(xkbcommon)
%endif
Requires: pkgconfig(zlib)

%description static
%{summary}.

%if "%{?ibase}" != "-no-sql-ibase"
%package ibase
Summary: IBase driver for Qt5's SQL classes
BuildRequires: firebird-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description ibase
%{summary}.
%endif

%package mysql
Summary: MySQL driver for Qt5's SQL classes
BuildRequires: mysql-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description mysql
%{summary}.

%package odbc
Summary: ODBC driver for Qt5's SQL classes
BuildRequires: unixODBC-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description odbc
%{summary}.

%package postgresql
Summary: PostgreSQL driver for Qt5's SQL classes
BuildRequires: postgresql-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description postgresql
%{summary}.

%if "%{?tds}" != "-no-sql-tds"
%package tds
Summary: TDS driver for Qt5's SQL classes
BuildRequires: freetds-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description tds
%{summary}.
%endif

# debating whether to do 1 subpkg per library or not -- rex
%package gui
Summary: Qt5 GUI-related libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} > 20
Recommends: mesa-dri-drivers
%endif
Obsoletes: qt5-qtbase-x11 < 5.2.0
Provides:  qt5-qtbase-x11 = %{version}-%{release}
# for Source6: 10-qt5-check-opengl2.sh:
# glxinfo
Requires: glx-utils
%description gui
Qt5 libraries used for drawing widgets and OpenGL items.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}

%patch4 -p1 -b .QTBUG-35459

%patch50 -p1 -b .QT_VERSION_CHECK
#patch51 -p1 -b .hidpi_scale_at_192
%patch52 -p1 -b .moc_macros
#patch61 -p1 -b .qt5-qtbase-cxxflag
%if 0%{?openssl11}
%patch63 -p1 -b .openssl11
%endif
%patch64 -p1 -b .firebird
%patch65 -p1 -b .mysql

%patch486 -p1 -b .0086

%if 0%{?inject_optflags}
## adjust $RPM_OPT_FLAGS

%patch2 -p1 -b .multilib_optflags
# drop backup file(s), else they get installed too, http://bugzilla.redhat.com/639463
rm -fv mkspecs/linux-g++*/qmake.conf.multilib-optflags

sed -i -e "s|-O2|$RPM_OPT_FLAGS|g" \
  mkspecs/%{platform}/qmake.conf

sed -i -e "s|^\(QMAKE_LFLAGS_RELEASE.*\)|\1 $RPM_LD_FLAGS|" \
  mkspecs/common/g++-unix.conf

# undefine QMAKE_STRIP (and friends), so we get useful -debuginfo pkgs (#1065636)
sed -i -e 's|^\(QMAKE_STRIP.*=\).*$|\1|g' mkspecs/common/linux.conf
%endif

# move some bundled libs to ensure they're not accidentally used
pushd src/3rdparty
mkdir UNUSED
mv freetype libjpeg libpng zlib UNUSED/
%if "%{?sqlite}" == "-system-sqlite"
mv sqlite UNUSED/
%endif
%if "%{?xcb}" != "-qt-xcb"
mv xcb UNUSED/
%endif
popd

# builds failing mysteriously on f20
# ./configure: Permission denied
# check to ensure that can't happen -- rex
test -x configure || chmod +x configure

# use proper perl interpretter so autodeps work as expected
sed -i -e "s|^#!/usr/bin/env perl$|#!%{__perl}|" \
 bin/fixqt4headers.pl \
 bin/syncqt.pl \
 mkspecs/features/data/unix/findclasslist.pl

# Fix missing private includes https://bugreports.qt.io/browse/QTBUG-37417
sed -e '/CMAKE_NO_PRIVATE_INCLUDES\ \=\ true/d' -i \
  mkspecs/features/create_cmake.prf


%build
## FIXME/TODO:
# * for %%ix86, add sse2 enabled builds for Qt5Gui, Qt5Core, QtNetwork, see also:
#   http://anonscm.debian.org/cgit/pkg-kde/qt/qtbase.git/tree/debian/rules (234-249)

## adjust $RPM_OPT_FLAGS
# remove -fexceptions
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`
RPM_OPT_FLAGS="$RPM_OPT_FLAGS %{?qt5_arm_flag} %{?qt5_deprecated_flag} %{?qt5_null_flag}"

%if 0%{?use_clang}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fno-delete-null-pointer-checks||g'`
%endif

export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
export CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS $RPM_LD_FLAGS"
export MAKEFLAGS="%{?_smp_mflags}"

./configure \
  -verbose \
  -confirm-license \
  -opensource \
  -prefix %{_qt5_prefix} \
  -archdatadir %{_qt5_archdatadir} \
  -bindir %{_qt5_bindir} \
  -libdir %{_qt5_libdir} \
  -libexecdir %{_qt5_libexecdir} \
  -datadir %{_qt5_datadir} \
  -docdir %{_qt5_docdir} \
  -examplesdir %{_qt5_examplesdir} \
  -headerdir %{_qt5_headerdir} \
  -importdir %{_qt5_importdir} \
  -plugindir %{_qt5_plugindir} \
  -sysconfdir %{_qt5_sysconfdir} \
  -translationdir %{_qt5_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -accessibility \
  %{?dbus}%{!?dbus:-dbus-runtime} \
  -fontconfig \
  -glib \
  -gtk \
  %{?ibase} \
  -icu \
  %{?journald} \
  -optimized-qmake \
  %{?openssl} \
  %{!?examples:-nomake examples} \
  %{!?tests:-nomake tests} \
  -no-pch \
  -no-rpath \
  -no-separate-debug-info \
%ifarch %{ix86}
  -no-sse2 \
%endif
  -no-strip \
  -system-libjpeg \
  -system-libpng \
  %{?harfbuzz} \
  %{?pcre} \
  %{?sqlite} \
  %{?tds} \
  %{?xcb} \
  %{?xkbcommon} \
  -system-zlib \
  %{?use_gold_linker} \
  -no-directfb

%if ! 0%{?inject_optflags}
# ensure qmake build using optflags (which can happen if not munging qmake.conf defaults)
make clean -C qmake
make %{?_smp_mflags} -C qmake \
  QMAKE_CFLAGS_RELEASE="${CFLAGS:-$RPM_OPT_FLAGS}" \
  QMAKE_CXXFLAGS_RELEASE="${CXXFLAGS:-$RPM_OPT_FLAGS}" \
  QMAKE_LFLAGS_RELEASE="${LDFLAGS:-$RPM_LD_FLAGS}" \
  QMAKE_STRIP=
%endif

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

install -m644 -p -D %{SOURCE1} %{buildroot}%{_qt5_datadir}/qtlogging.ini

# Qt5.pc
cat >%{buildroot}%{_libdir}/pkgconfig/Qt5.pc<<EOF
prefix=%{_qt5_prefix}
archdatadir=%{_qt5_archdatadir}
bindir=%{_qt5_bindir}
datadir=%{_qt5_datadir}

docdir=%{_qt5_docdir}
examplesdir=%{_qt5_examplesdir}
headerdir=%{_qt5_headerdir}
importdir=%{_qt5_importdir}
libdir=%{_qt5_libdir}
libexecdir=%{_qt5_libexecdir}
moc=%{_qt5_bindir}/moc
plugindir=%{_qt5_plugindir}
qmake=%{_qt5_bindir}/qmake
settingsdir=%{_qt5_settingsdir}
sysconfdir=%{_qt5_sysconfdir}
translationdir=%{_qt5_translationdir}

Name: Qt5
Description: Qt5 Configuration
Version: 5.9.0
EOF

# rpm macros
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtbase
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtbase

# create/own dirs
mkdir -p %{buildroot}{%{_qt5_archdatadir}/mkspecs/modules,%{_qt5_importdir},%{_qt5_libexecdir},%{_qt5_plugindir}/{designer,iconengines,script,styles},%{_qt5_translationdir}}
mkdir -p %{buildroot}%{_sysconfdir}/xdg/QtProject

# hardlink files to {_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
    moc|qdbuscpp2xml|qdbusxml2cpp|qmake|rcc|syncqt|uic)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt5
      ln -sv ${i} ${i}-qt5
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

%ifarch %{multilib_archs}
# multilib: qconfig.h
  mv %{buildroot}%{_qt5_headerdir}/QtCore/qconfig.h %{buildroot}%{_qt5_headerdir}/QtCore/qconfig-%{__isa_bits}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt5_headerdir}/QtCore/qconfig.h
%endif

# qtchooser conf
%if 0%{?qtchooser}
  mkdir -p %{buildroot}%{_sysconfdir}/xdg/qtchooser
  pushd    %{buildroot}%{_sysconfdir}/xdg/qtchooser
  echo "%{_qt5_bindir}" >  5-%{__isa_bits}.conf
  echo "%{_qt5_prefix}" >> 5-%{__isa_bits}.conf
  # alternatives targets
  touch default.conf 5.conf
  popd
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

install -p -m755 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh

# fix bz#1442553 multilib issue
privat_header_file=%{buildroot}%{_qt5_headerdir}/QtCore/%{version}/QtCore/private/qconfig_p.h
grep -v QT_FEATURE_sse2 $privat_header_file > ${privat_header_file}.me
mv ${privat_header_file}.me ${privat_header_file}
cat >>${privat_header_file}<<EOF
#if defined(__x86_64__)
#define QT_FEATURE_sse2 1
#elif defined(__i386__)
#define QT_FEATURE_sse2 -1
#endif
EOF


%check
%if 0%{?tests}
## see tests/README for expected environment (running a plasma session essentially)
## we are not quite there yet
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_qt5_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
# dbus tests error out when building if session bus is not available
dbus-launch --exit-with-session \
make sub-tests %{?_smp_mflags} -k ||:
xvfb-run -a --server-args="-screen 0 1280x1024x32" \
dbus-launch --exit-with-session \
time \
make check -k ||:
%endif


%if 0%{?qtchooser}
%pre
if [ $1 -gt 1 ] ; then
# remove short-lived qt5.conf alternatives
%{_sbindir}/update-alternatives  \
  --remove qtchooser-qt5 \
  %{_sysconfdir}/xdg/qtchooser/qt5-%{__isa_bits}.conf >& /dev/null ||:

%{_sbindir}/update-alternatives  \
  --remove qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/qt5.conf >& /dev/null ||:
fi
%endif

%post
/sbin/ldconfig
%if 0%{?qtchooser}
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/xdg/qtchooser/5.conf \
  qtchooser-5 \
  %{_sysconfdir}/xdg/qtchooser/5-%{__isa_bits}.conf \
  %{priority}

%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/xdg/qtchooser/default.conf \
  qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/5.conf \
  %{priority}
%endif

%postun
/sbin/ldconfig
%if 0%{?qtchooser}
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives  \
  --remove qtchooser-5 \
  %{_sysconfdir}/xdg/qtchooser/5-%{__isa_bits}.conf

%{_sbindir}/update-alternatives  \
  --remove qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/5.conf
fi
%endif

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.LGPL* LGPL_EXCEPTION.txt LICENSE.FDL
%if 0%{?qtchooser}
%dir %{_sysconfdir}/xdg/qtchooser
# not editable config files, so not using %%config here
%ghost %{_sysconfdir}/xdg/qtchooser/default.conf
%ghost %{_sysconfdir}/xdg/qtchooser/5.conf
%{_sysconfdir}/xdg/qtchooser/5-%{__isa_bits}.conf
%endif
%dir %{_sysconfdir}/xdg/QtProject/
%{_qt5_libdir}/libQt5Concurrent.so.5*
%{_qt5_libdir}/libQt5Core.so.5*
%{_qt5_libdir}/libQt5DBus.so.5*
%{_qt5_libdir}/libQt5Network.so.5*
%{_qt5_libdir}/libQt5Sql.so.5*
%{_qt5_libdir}/libQt5Test.so.5*
%{_qt5_libdir}/libQt5Xml.so.5*
%{_qt5_libdir}/libQt5EglFSDeviceIntegration.so.5*
%dir %{_qt5_libdir}/cmake/
%dir %{_qt5_libdir}/cmake/Qt5/
%dir %{_qt5_libdir}/cmake/Qt5Concurrent/
%dir %{_qt5_libdir}/cmake/Qt5Core/
%dir %{_qt5_libdir}/cmake/Qt5DBus/
%dir %{_qt5_libdir}/cmake/Qt5Gui/
%dir %{_qt5_libdir}/cmake/Qt5Network/
%dir %{_qt5_libdir}/cmake/Qt5OpenGL/
%dir %{_qt5_libdir}/cmake/Qt5PrintSupport/
%dir %{_qt5_libdir}/cmake/Qt5Sql/
%dir %{_qt5_libdir}/cmake/Qt5Test/
%dir %{_qt5_libdir}/cmake/Qt5Widgets/
%dir %{_qt5_libdir}/cmake/Qt5Xml/
%dir %{_qt5_docdir}/
%{_qt5_docdir}/global/
%{_qt5_importdir}/
%{_qt5_translationdir}/
%dir %{_qt5_prefix}/
%dir %{_qt5_datadir}/
%{_qt5_datadir}/qtlogging.ini
%dir %{_qt5_libexecdir}/
%dir %{_qt5_plugindir}/
%dir %{_qt5_plugindir}/bearer/
%{_qt5_plugindir}/bearer/libqconnmanbearer.so
%{_qt5_plugindir}/bearer/libqgenericbearer.so
%{_qt5_plugindir}/bearer/libqnmbearer.so
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_QConnmanEnginePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_QGenericEnginePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_QNetworkManagerEnginePlugin.cmake
%dir %{_qt5_plugindir}/designer/
%dir %{_qt5_plugindir}/generic/
%dir %{_qt5_plugindir}/iconengines/
%dir %{_qt5_plugindir}/imageformats/
%dir %{_qt5_plugindir}/platforminputcontexts/
%dir %{_qt5_plugindir}/platforms/
%dir %{_qt5_plugindir}/platformthemes/
%dir %{_qt5_plugindir}/printsupport/
%dir %{_qt5_plugindir}/script/
%dir %{_qt5_plugindir}/sqldrivers/
%dir %{_qt5_plugindir}/styles/
%{_qt5_plugindir}/sqldrivers/libqsqlite.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QSQLiteDriverPlugin.cmake

%files common
# mostly empty for now, consider: filesystem/dir ownership, licenses
%{rpm_macros_dir}/macros.qt5-qtbase

%files devel
%if "%{_qt5_bindir}" != "%{_bindir}"
%dir %{_qt5_bindir}
%endif
%{_bindir}/moc*
%{_bindir}/qdbuscpp2xml*
%{_bindir}/qdbusxml2cpp*
%{_bindir}/qmake*
%{_bindir}/rcc*
%{_bindir}/syncqt*
%{_bindir}/uic*
%{_bindir}/qlalr
%{_bindir}/fixqt4headers.pl
%{_qt5_bindir}/moc*
%{_qt5_bindir}/qdbuscpp2xml*
%{_qt5_bindir}/qdbusxml2cpp*
%{_qt5_bindir}/qmake*
%{_qt5_bindir}/rcc*
%{_qt5_bindir}/syncqt*
%{_qt5_bindir}/uic*
%{_qt5_bindir}/qlalr
%{_qt5_bindir}/fixqt4headers.pl
%if "%{_qt5_headerdir}" != "%{_includedir}"
%dir %{_qt5_headerdir}
%endif
%{_qt5_headerdir}/QtConcurrent/
%{_qt5_headerdir}/QtCore/
%{_qt5_headerdir}/QtDBus/
%{_qt5_headerdir}/QtGui/
%{_qt5_headerdir}/QtNetwork/
%{_qt5_headerdir}/QtOpenGL/
%{_qt5_headerdir}/QtPlatformHeaders/
%{_qt5_headerdir}/QtPrintSupport/
%{_qt5_headerdir}/QtSql/
%{_qt5_headerdir}/QtTest/
%{_qt5_headerdir}/QtWidgets/
%{_qt5_headerdir}/QtXml/
%{_qt5_headerdir}/QtEglFSDeviceIntegration
%{_qt5_headerdir}/QtInputSupport
%{_qt5_archdatadir}/mkspecs/
%{_qt5_libdir}/libQt5Concurrent.prl
%{_qt5_libdir}/libQt5Concurrent.so
%{_qt5_libdir}/libQt5Core.prl
%{_qt5_libdir}/libQt5Core.so
%{_qt5_libdir}/libQt5DBus.prl
%{_qt5_libdir}/libQt5DBus.so
%{_qt5_libdir}/libQt5Gui.prl
%{_qt5_libdir}/libQt5Gui.so
%{_qt5_libdir}/libQt5Network.prl
%{_qt5_libdir}/libQt5Network.so
%{_qt5_libdir}/libQt5OpenGL.prl
%{_qt5_libdir}/libQt5OpenGL.so
%{_qt5_libdir}/libQt5PrintSupport.prl
%{_qt5_libdir}/libQt5PrintSupport.so
%{_qt5_libdir}/libQt5Sql.prl
%{_qt5_libdir}/libQt5Sql.so
%{_qt5_libdir}/libQt5Test.prl
%{_qt5_libdir}/libQt5Test.so
%{_qt5_libdir}/libQt5Widgets.prl
%{_qt5_libdir}/libQt5Widgets.so
%{_qt5_libdir}/libQt5XcbQpa.prl
%{_qt5_libdir}/libQt5XcbQpa.so
%{_qt5_libdir}/libQt5Xml.prl
%{_qt5_libdir}/libQt5Xml.so
%{_qt5_libdir}/libQt5EglFSDeviceIntegration.prl
%{_qt5_libdir}/libQt5EglFSDeviceIntegration.so
%{_qt5_libdir}/cmake/Qt5/Qt5Config*.cmake
%{_qt5_libdir}/cmake/Qt5Concurrent/Qt5ConcurrentConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CoreConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CoreMacros.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CTestMacros.cmake
%{_qt5_libdir}/cmake/Qt5DBus/Qt5DBusConfig*.cmake
%{_qt5_libdir}/cmake/Qt5DBus/Qt5DBusMacros.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5GuiConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5NetworkConfig*.cmake
%{_qt5_libdir}/cmake/Qt5OpenGL/Qt5OpenGLConfig*.cmake
%{_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Sql/Qt5SqlConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Test/Qt5TestConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Widgets/Qt5WidgetsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Widgets/Qt5WidgetsMacros.cmake
%{_qt5_libdir}/cmake/Qt5Xml/Qt5XmlConfig*.cmake
%{_qt5_libdir}/cmake/Qt5/Qt5ModuleLocation.cmake
%{_qt5_libdir}/pkgconfig/Qt5.pc
%{_qt5_libdir}/pkgconfig/Qt5Concurrent.pc
%{_qt5_libdir}/pkgconfig/Qt5Core.pc
%{_qt5_libdir}/pkgconfig/Qt5DBus.pc
%{_qt5_libdir}/pkgconfig/Qt5Gui.pc
%{_qt5_libdir}/pkgconfig/Qt5Network.pc
%{_qt5_libdir}/pkgconfig/Qt5OpenGL.pc
%{_qt5_libdir}/pkgconfig/Qt5PrintSupport.pc
%{_qt5_libdir}/pkgconfig/Qt5Sql.pc
%{_qt5_libdir}/pkgconfig/Qt5Test.pc
%{_qt5_libdir}/pkgconfig/Qt5Widgets.pc
%{_qt5_libdir}/pkgconfig/Qt5Xml.pc
%if 0%{?egl}
%{_qt5_libdir}/libQt5EglFsKmsSupport.prl
%{_qt5_libdir}/libQt5EglFsKmsSupport.so
%endif


%files static
%{_qt5_libdir}/libQt5Bootstrap.*a
%{_qt5_libdir}/libQt5Bootstrap.prl
%{_qt5_headerdir}/QtOpenGLExtensions/
%{_qt5_libdir}/libQt5OpenGLExtensions.*a
%{_qt5_libdir}/libQt5OpenGLExtensions.prl
%{_qt5_libdir}/cmake/Qt5OpenGLExtensions/
%{_qt5_libdir}/pkgconfig/Qt5OpenGLExtensions.pc
%{_qt5_libdir}/libQt5AccessibilitySupport.*a
%{_qt5_libdir}/libQt5AccessibilitySupport.prl
%{_qt5_headerdir}/QtAccessibilitySupport
%{_qt5_libdir}/libQt5DeviceDiscoverySupport.*a
%{_qt5_libdir}/libQt5DeviceDiscoverySupport.prl
%{_qt5_headerdir}/QtDeviceDiscoverySupport
%{_qt5_libdir}/libQt5EglSupport.*a
%{_qt5_libdir}/libQt5EglSupport.prl
%{_qt5_headerdir}/QtEglSupport
%{_qt5_libdir}/libQt5EventDispatcherSupport.*a
%{_qt5_libdir}/libQt5EventDispatcherSupport.prl
%{_qt5_headerdir}/QtEventDispatcherSupport
%{_qt5_libdir}/libQt5FbSupport.*a
%{_qt5_libdir}/libQt5FbSupport.prl
%{_qt5_headerdir}/QtFbSupport
%{_qt5_libdir}/libQt5FontDatabaseSupport.*a
%{_qt5_libdir}/libQt5FontDatabaseSupport.prl
%{_qt5_headerdir}/QtFontDatabaseSupport
%{_qt5_libdir}/libQt5GlxSupport.*a
%{_qt5_libdir}/libQt5GlxSupport.prl
%{_qt5_headerdir}/QtGlxSupport
%{_qt5_libdir}/libQt5InputSupport.*a
%{_qt5_libdir}/libQt5InputSupport.prl
%{_qt5_libdir}/libQt5LinuxAccessibilitySupport.*a
%{_qt5_libdir}/libQt5LinuxAccessibilitySupport.prl
%{_qt5_headerdir}/QtLinuxAccessibilitySupport
%{_qt5_libdir}/libQt5PlatformCompositorSupport.*a
%{_qt5_libdir}/libQt5PlatformCompositorSupport.prl
%{_qt5_headerdir}/QtPlatformCompositorSupport
%{_qt5_libdir}/libQt5ServiceSupport.*a
%{_qt5_libdir}/libQt5ServiceSupport.prl
%{_qt5_headerdir}/QtServiceSupport
%{_qt5_libdir}/libQt5ThemeSupport.*a
%{_qt5_libdir}/libQt5ThemeSupport.prl
%{_qt5_headerdir}/QtThemeSupport
%{_qt5_libdir}/libQt5KmsSupport.*a
%{_qt5_libdir}/libQt5KmsSupport.prl
%{_qt5_headerdir}/QtKmsSupport

%if 0%{?examples}
%files examples
%{_qt5_examplesdir}/
%endif

%if "%{?ibase}" != "-no-sql-ibase"
%files ibase
%{_qt5_plugindir}/sqldrivers/libqsqlibase.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QIBaseDriverPlugin.cmake
%endif

%files mysql
%{_qt5_plugindir}/sqldrivers/libqsqlmysql.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QMYSQLDriverPlugin.cmake

%files odbc
%{_qt5_plugindir}/sqldrivers/libqsqlodbc.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QODBCDriverPlugin.cmake

%files postgresql
%{_qt5_plugindir}/sqldrivers/libqsqlpsql.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QPSQLDriverPlugin.cmake

%if "%{?tds}" != "-no-sql-tds"
%files tds
%{_qt5_plugindir}/sqldrivers/libqsqltds.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QTDSDriverPlugin.cmake
%endif

%post gui -p /sbin/ldconfig
%postun gui -p /sbin/ldconfig

%files gui
%dir %{_sysconfdir}/X11/xinit
%dir %{_sysconfdir}/X11/xinit/xinitrc.d/
%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh
%{_qt5_libdir}/libQt5Gui.so.5*
%{_qt5_libdir}/libQt5OpenGL.so.5*
%{_qt5_libdir}/libQt5PrintSupport.so.5*
%{_qt5_libdir}/libQt5Widgets.so.5*
%{_qt5_libdir}/libQt5XcbQpa.so.5*
%{_qt5_plugindir}/generic/libqevdevkeyboardplugin.so
%{_qt5_plugindir}/generic/libqevdevmouseplugin.so
%{_qt5_plugindir}/generic/libqevdevtabletplugin.so
%{_qt5_plugindir}/generic/libqevdevtouchplugin.so
%if 0%{?fedora}
%{_qt5_plugindir}/generic/libqlibinputplugin.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QLibInputPlugin.cmake
%endif
%{_qt5_plugindir}/generic/libqtuiotouchplugin.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevKeyboardPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevMousePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevTabletPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevTouchScreenPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QTuioTouchPlugin.cmake
%{_qt5_plugindir}/imageformats/libqgif.so
%{_qt5_plugindir}/imageformats/libqico.so
%{_qt5_plugindir}/imageformats/libqjpeg.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QGifPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QICOPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QJpegPlugin.cmake
%{_qt5_plugindir}/platforminputcontexts/libcomposeplatforminputcontextplugin.so
%{_qt5_plugindir}/platforminputcontexts/libibusplatforminputcontextplugin.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QComposePlatformInputContextPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QIbusPlatformInputContextPlugin.cmake
%if 0%{?egl}
%{_qt5_libdir}/libQt5EglFsKmsSupport.so.5*
%{_qt5_plugindir}/platforms/libqeglfs.so
%{_qt5_plugindir}/platforms/libqminimalegl.so
%dir %{_qt5_plugindir}/egldeviceintegrations/
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-kms-integration.so
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-x11-integration.so
%{_qt5_plugindir}/xcbglintegrations/libqxcb-egl-integration.so
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-kms-egldevice-integration.so
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-emu-integration.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalEglIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSX11IntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsGbmIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbEglIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsEglDeviceIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSEmulatorIntegrationPlugin.cmake
%endif
%{_qt5_plugindir}/platforms/libqlinuxfb.so
%{_qt5_plugindir}/platforms/libqminimal.so
%{_qt5_plugindir}/platforms/libqoffscreen.so
%{_qt5_plugindir}/platforms/libqxcb.so
%{_qt5_plugindir}/platforms/libqvnc.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QLinuxFbIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QOffscreenIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QVncIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbIntegrationPlugin.cmake
%{_qt5_plugindir}/xcbglintegrations/libqxcb-glx-integration.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbGlxIntegrationPlugin.cmake
%{_qt5_plugindir}/platformthemes/libqgtk3.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QGtk3ThemePlugin.cmake
%{_qt5_plugindir}/printsupport/libcupsprintersupport.so
%{_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupport_QCupsPrinterSupportPlugin.cmake


%changelog
* Thu Jul 27 2017 Than Ngo <than@redhat.com> - 5.9.1-3
- fixed bz#1401459, backport openssl-1.1 support

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Tue Jul 18 2017 Than Ngo <than@redhat.com> - 5.9.0-6
- fixed bz#1442553, multilib issue

* Fri Jul 14 2017 Than Ngo <than@redhat.com> - 5.9.0-5
- fixed build issue with new mariadb

* Thu Jul 06 2017 Than Ngo <than@redhat.com> - 5.9.0-4
- fixed bz#1409600, stack overflow in QXmlSimpleReader, CVE-2016-10040

* Fri Jun 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-3
- create_cmake.prf: adjust CMAKE_NO_PRIVATE_INCLUDES (#1456211,QTBUG-37417)

* Thu Jun 01 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- workaround gold linker issue with duplicate symbols (f27+, #1458003)

* Wed May 31 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Upstream official release

* Fri May 26 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.1.rc
- Upstream Release Candidate retagged

* Wed May 24 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.rc.1
- Upstream Release Candidate 1

* Tue May 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-0.6.beta3
- -common: Obsoletes: qt5-qtquick1(-devel)

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.0-0.5.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon May 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-0.4.beta3
- include recommended qtdbus patches, fix Release

* Fri May 05 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.3
- Beta 3 release

* Fri Apr 14 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.1
- No more docs, no more bootstrap. Docs comes now on a single package.

* Thu Mar 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-8
- de-bootstrap
- make -doc arch'd (workaround bug #1437522)

* Wed Mar 29 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-7
- rebuild

* Mon Mar 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-6
- bootstrap (rawhide)
- revert some minor changes introduced since 5.7
- move *Plugin.cmake items to runtime (not -devel)

* Sat Jan 28 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-5
- Really debootstrap :-P

* Fri Jan 27 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-4
- Debootstrap
- Use meta doctools package to build docs

* Fri Jan 27 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-3
- Unify firebird patch for both versions
- Bootstrap again for copr

* Thu Jan 26 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-2
- Debootstrap after tools built. New tool needed qtattributionsscanner

* Thu Jan 26 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-1
- Initial update for 5.8.0

* Tue Jan 24 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-13
- Broken window scaling (#1381828)

* Wed Jan 04 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.7.1-12
- readd plugin __requires_exclude_from filter, it is still needed

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-11
- filter plugin provides, drop filter plugin excludes (no longer needed)

* Mon Dec 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-10
- backport 5.8 patch for wayland crasher (#1403500,QTBUG-55583)

* Fri Dec 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-9
- restore moc_system_defines.patch lost in 5.7.0 rebase

* Fri Dec 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-8
- update moc patch to define _SYS_SYSMACROS_H_OUTER instead (#1396755)

* Thu Dec 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-7
- really apply QT_VERSION_CHECK workaround (#1396755)

* Thu Dec 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-6
- namespace QT_VERSION_CHECK to workaround major/minor being pre-defined (#1396755)
- update moc patch to define _SYS_SYSMACROS_H (#1396755)

* Thu Dec 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-5
- 5.7.1 dec5 snapshot

* Wed Dec 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-4
- disable openssl11 (for now, FTBFS), use -openssl-linked (bug #1401459)
- BR: perl-generators

* Mon Nov 28 2016 Than Ngo <than@redhat.com> - 5.7.1-3
- add condition for rhel
- add support for firebird-3.x

* Thu Nov 24 2016 Than Ngo <than@redhat.com> - 5.7.1-2
- adapted the berolinux's patch for new openssl-1.1.x

* Wed Nov 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- New upstream version

* Thu Oct 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-10
- fix Source0: https://download.qt.io/official_releases/qt/5.9/5.9.0/submodules/qtbase-opensource-src-5.9.0.tar.xz

* Thu Sep 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-9
- Requires: openssl-libs%%{?_isa} (#1328659)

* Wed Sep 28 2016 Than Ngo <than@redhat.com> - 5.7.0-8
- bz#1328659, load openssl libs dynamically

* Tue Sep 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-7
- drop BR: cmake (handled by qt5-rpm-macros now)

* Wed Sep 14 2016 Than Ngo <than@redhat.com> - 5.7.0-6
- add macros qtwebengine_arches in qt5

* Tue Sep 13 2016 Than Ngo <than@redhat.com> - 5.7.0-5
- add rpm macros qtwebengine_arches for qtwebengine

* Mon Sep 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-4
- use '#!/usr/bin/perl' instead of '#!/usr/bin/env perl'

* Tue Jul 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-3
- introduce macros.qt5-qtbase (for %%_qt5, %%_qt5_epoch, %%_qt5_version, %%_qt5_evr)

* Tue Jun 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-2
- Compiled with gcc

* Tue Jun 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Qt 5.7.0 release

* Thu Jun 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-0.1
- Prepare 5.7
- Move macros package away from qtbase. Now is called qt5-rpm-macros

* Thu Jun 02 2016 Than Ngo <than@redhat.com> - 5.6.0-21
- drop gcc6 workaround on arm

* Fri May 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-20
- -Wno-deprecated-declarations (typo missed trailing 's')

* Fri May 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-19
- pull in upstream drag-n-drop related fixes (QTBUG-45812, QTBUG-51215)

* Sat May 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-18
- revert out-of-tree build, breaks Qt5*Config.cmake *_PRIVATE_INCLUDE_DIRS entries (all blank)

* Thu May 05 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-17
- support out-of-tree build
- better %%check
- pull in final/upstream fixes for QTBUG-51648,QTBUG-51649
- disable examples/tests in bootstrap mode

* Sat Apr 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-16
- own %%{_qt5_plugindir}/egldeviceintegrations

* Mon Apr 18 2016 Caolán McNamara <caolanm@redhat.com> - 5.6.0-15
- full rebuild for hunspell 1.4.0

* Mon Apr 18 2016 Caolán McNamara <caolanm@redhat.com> - 5.6.0-14
- bootstrap rebuild for hunspell 1.4.0

* Sat Apr 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-13
- -devel: Provides: qt5-qtbase-private-devel (#1233829)

* Sat Apr 16 2016 David Tardon <dtardon@redhat.com> - 5.6.0-12
- full build

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 5.6.0-11
- rebuild for ICU 57.1

* Thu Mar 31 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-10
- Fix build on MIPS (#1322537)
- drop BR: valgrind (not used, for awhile)

* Fri Mar 25 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-9
- pull upstream patches (upstreamed versions, gcc6-related bits mostly)

* Thu Mar 24 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-8
- make 10-qt5-check-opengl2.sh xinit script more robust
- enable journald support for el7+ (#1315239)

* Sat Mar 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-7
- macros.qt5: null-pointer-checks flag isn't c++-specific

* Sat Mar 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-6
- macros.qt5: we really only want the null-pointer-checks flag here
  and definitely no arch-specific ones

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-5
- macros.qt5: cleanup, %%_qt5_cflags, %%_qt5_cxxflags (for f24+)

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-3
- rebuild

* Tue Mar 15 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-2
- respin QTBUG-51767 patch

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 release

* Sat Mar 12 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.41.rc
- %%build: restore -dbus-linked

* Fri Mar 11 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.40.rc
- respin QTBUG-51649 patch
- %%build: use -dbus-runtime unconditionally
- drop (unused) build deps: atspi, dbus, networkmanager

* Thu Mar 10 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.39.rc
- candidate fixes for various QtDBus deadlocks (QTBUG-51648,QTBUG-51676)

* Mon Mar 07 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.38.rc
- backport "crash on start if system bus is not available" (QTBUG-51299)

* Sat Mar 05 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.37.rc
- build: ./configure -journal (f24+)

* Wed Mar 02 2016 Daniel Vrátil <dvratil@fedoraproject.org> 5.6.0-0.36.rc
- Non-bootstrapped build

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> 5.6.0-0.35.rc
- Rebuild against new openssl

* Fri Feb 26 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.34.rc
- qtlogging.ini: remove comments

* Thu Feb 25 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.33.rc
- ship $$[QT_INSTALL_DATA]/qtlogging.ini for packaged logging defaults (#1227295)

* Thu Feb 25 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.32.rc
- qt5-qtbase-static missing dependencies (#1311311)

* Wed Feb 24 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.31.rc
- Item views don't handle insert/remove of rows robustly (QTBUG-48870)

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.30.rc
- Update to final RC

* Mon Feb 22 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.29.rc
- Update tarball with https://bugreports.qt.io/browse/QTBUG-50703 fix

* Wed Feb 17 2016 Than Ngo <than@redhat.com> - 5.6.0-0.28.rc
- fix build issue with gcc6

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.27.rc
- Update proper tarball. Need avoid the fix branch

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.26.rc
- Integrate rc releases now.

* Sat Feb 13 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.25.beta
- macros.qt5: fix %%qt5_ldflags macro

* Thu Feb 11 2016 Than Ngo <than@redhat.com> - 5.6.0-0.24.beta
- fix build issue with gcc6
- fix check for alsa 1.1.x

* Wed Feb 03 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.23.beta
- qt5-rpm-macros pkg

* Tue Feb 02 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.22.beta
- don't inject $RPM_OPT_FLAGS/$RPM_LD_FLAGS into qmake defaults f24+ (#1279265)

* Tue Feb 02 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.21.beta
- build with and add to macros.qt5 flags: -fno-delete-null-pointer-checks

* Fri Jan 15 2016 Than Ngo <than@redhat.com> - 5.6.0-0.20.beta
- enable -qt-xcb to fix non-US keys under VNC (#1295713)

* Mon Jan 04 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.19.beta
- Crash in QXcbWindow::setParent() due to NULL xcbScreen (QTBUG-50081, #1291003)

* Mon Dec 21 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.17.beta
- fix/update Release: 1%{?dist}

* Fri Dec 18 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.16
- 5.6.0-beta (final)

* Wed Dec 16 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-0.15
- pull in another upstream moc fix/improvement (#1290020,QTBUG-49972)
- fix bootstrap/docs

* Wed Dec 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.13
- workaround moc/qconfig-multilib issues (#1290020,QTBUG-49972)

* Wed Dec 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 5.6.0-0.12
- aarch64 is secondary arch too
- ppc64le is NOT multilib
- Fix Power 64 macro use

* Mon Dec 14 2015 Than Ngo <than@redhat.com> - 5.6.0-0.11
- fix build failure on secondary arch

* Sun Dec 13 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.10
- We're back to gold linker
- Remove reduce relocations

* Sat Dec 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.9
- drop disconnect_displays.patch so we can better test latest xcb/display work

* Fri Dec 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.8
- sync latest xcb/screen/display related upstream commits

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.7
- Official beta release

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.6
- Official beta release

* Wed Dec 09 2015 Daniel Vratil <dvratil@fedoraproject.org> - 5.6.0-0.5
- try reverting from -optimized-tools to -optimized-qmake

* Sun Dec 06 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-0.4
- re-introduce bootstrap/examples macros
- put examples-manifest.xml in -examples
- restore -doc multilib hack (to be on the safe side, can't hurt)
- %%build: s/-optimized-qmake/-optimized-tools/

* Sat Dec 05 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.3
- Beta 3
- Reintroduce xcb patch from https://codereview.qt-project.org/#/c/138201/

* Fri Nov 27 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.2
- Valgrind still needed as buildreq due recent split qdoc package, but we can get rid of
  specific arch set.
- Added missing libproxy buildreq
- Epel and RHEL doesn't have libinput, so a plugin need to be excluded for this distros

* Wed Nov 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-10
- -devel: Requires: redhat-rpm-config (#1248174)

* Wed Nov 18 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-9
- Get rid of valgrind hack. It sort out that we don't need it anymore (#1211203)

* Mon Nov 09 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-8
- qt5-qdoc need requires >= current version, otherwise will prevent the usage further when moved to qttools

* Mon Nov 09 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-7
- qt5-qdoc subpkg

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 5.5.1-6
- full build

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 5.5.1-5
- rebuild for ICU 56.1

* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Mon Oct 05 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1
- Patchs 13, 52, 53, 101, 155, 223, 297 removed due to inclusion upstream

* Mon Oct 05 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-18
- When a screen comes back online, the windows need to be told about it (QTBUG-47041)
- xcb: Ignore disabling of outputs in the middle of the mode switch

* Wed Aug 19 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-17
- unconditionally undo valgrind hack when done (#1255054)

* Sat Aug 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-16
- backport 0055-Respect-manual-set-icon-themes.patch (kde#344469)
- conditionally use valgrind only if needed

* Fri Aug 07 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.5.0-15
- use valgrind to debug qdoc HTML generation

* Fri Aug 07 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.5.0-14
- remove GDB hackery again, -12 built fine on i686, hack breaks ARM build
- fix 10-qt5-check-opengl2.sh for multiple screens (#1245755)

* Thu Aug 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-13
- use upstream commit/fix for QTBUG-46310
- restore qdoc/gdb hackery, i686 still needs it :(

* Wed Aug 05 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.5.0-12
- remove GDB hackery, it is not producing useful backtraces for the ARM crash

* Mon Aug 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-11
- Add mesa-dri-drivers as recommends on gui package as reported by Kevin Kofler
- Reference https://bugzilla.redhat.com/1249280

* Wed Jul 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-10
- -docs: BuildRequires: qt5-qhelpgenerator

* Fri Jul 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-9
- use qdoc.gdb wrapper

* Wed Jul 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-8
- %%build: hack around 'make docs' failures (on f22+)

* Wed Jul 15 2015 Jan Grulich <jgrulich@redhat.com> 5.5.0-7
- restore previously dropped patches

* Tue Jul 14 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-6
- disable bootstrap again

* Tue Jul 14 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-5
- enable bootstrap (and disable failing docs)

* Mon Jul 13 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-4
- Qt5 application crashes when connecting/disconnecting displays (#1083664)

* Fri Jul 10 2015 Than Ngo <than@redhat.com> - 5.5.0-3
- add better fix for compile error on big endian

* Thu Jul 09 2015 Than Ngo <than@redhat.com> - 5.5.0-2
- fix build failure on big endian platform (ppc64,s390x)

* Mon Jun 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.5.rc
- Second round of builds now with bootstrap enabled due new qttools

* Mon Jun 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.4.rc
- Enable bootstrap to first import on rawhide

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.3.rc
- Disable bootstrap

* Wed Jun 24 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Mon Jun 15 2015 Daniel Vratil <dvratil@redhat.com> 5.5.0-0.1.rc
- Qt 5.5 RC 1

* Mon Jun 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-2
- rebase to latest SM patches (QTBUG-45484, QTBUG-46310)

* Tue Jun 02 2015 Jan Grulich <jgrulich@redhat.com> 5.4.2-1
- Update to 5.4.2

* Tue May 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-20
- SM_CLIENT_ID property is not set (QTBUG-46310)

* Mon May 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-19
- QWidget::setWindowRole does nothing (QTBUG-45484)

* Wed May 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-18
- own /etc/xdg/QtProject
- Requires: qt-settings (f22+)

* Sat May 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-17
- Try to ensure that -fPIC is used in CMake builds (QTBUG-45755)

* Thu May 14 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-16
- Some Qt apps crash if they are compiled with gcc5 (QTBUG-45755)

* Thu May 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-15
- try harder to avoid doc/multilib conflicts (#1212750)

* Wed May 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-14
- Shortcuts with KeypadModifier not working (QTBUG-33093,#1219173)

* Tue May 05 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-13
- backport: data corruption in QNetworkAccessManager

* Fri May 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-12
- backport a couple more upstream fixes
- introduce -common noarch subpkg, should help multilib issues

* Sat Apr 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-11
- port qtdbusconnection_no_debug.patch from qt(4)

* Fri Apr 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-10
- -examples: include %%{_qt5_docdir}/qdoc/examples-manifest.xml (#1212750)

* Mon Apr 13 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-9
- Multiple Vulnerabilities in Qt Image Format Handling (CVE-2015-1860 CVE-2015-1859 CVE-2015-1858)

* Fri Apr 10 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-8
- -dbus=runtime on el6 (#1196359)
- %%build: -no-directfb

* Wed Apr 01 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-7
- drop 5.5 XCB patches, the rebase is incomplete and does not work properly with Qt 5.4

* Mon Mar 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-6
- Crash due to unsafe access to QTextLayout::lineCount (#1207279,QTBUG-43562)

* Mon Mar 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-5
- unable to use input methods in ibus-1.5.10 (#1203575)

* Wed Mar 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.1-4
- pull in set of upstream Qt 5.5 fixes and improvements for XCB screen handling rebased to 5.4

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-3
- pull in handful of upstream fixes, particularly...
- Fix a division by zero when processing malformed BMP files (QTBUG-44547, CVE-2015-0295)

* Wed Feb 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- try bootstrap=1 (f23)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- update to 5.4.1

* Mon Feb 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-13
- -no-use-gold-linker (f22+, #1193044)

* Thu Feb 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-12
- own  %%{_qt5_plugindir}/{designer,iconengines,script,styles}

* Thu Feb 05 2015 David Tardon <dtardon@redhat.com> - 5.4.0-11
- full build after ICU soname bump

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 5.4.0-10
- Bump for rebuild.

* Sat Jan 31 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-9
- crashes when connecting/disconnecting displays (#1083664,QTBUG-42985)

* Tue Jan 27 2015 David Tardon <dtardon@redhat.com> - 5.4.0-8
- full build

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 5.4.0-7
- rebuild for ICU 54.1

* Sun Jan 18 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-6
- fix %%pre scriptlet

* Sat Jan 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-5
- ship /etc/xdg/qtchooser/5.conf alternative instead (of qt5.conf)

* Wed Dec 17 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-4
- workaround 'make docs' crasher on el6 (QTBUG-43057)

* Thu Dec 11 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-3
- don't omit examples for bootstrap (needs work)

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-2
- fix bootstrapping logic

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.8.rc
- restore font rendering patch (#1052389,QTBUG-41590)

* Thu Nov 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.7.rc
- 5.4.0-rc

* Wed Nov 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.6.beta
- add versioned Requires: libxkbcommon dep

* Tue Nov 11 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.5.beta
- pull in slightly different upstreamed font rendering fix (#1052389,QTBUG-41590)

* Mon Nov 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.4.beta
- Bad font rendering (#1052389,QTBUG-41590)

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.beta
- macros.qt5: +%%qmake_qt5 , to help set standard build flags (CFLAGS, etc...)

* Wed Oct 22 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.4.0-0.2.beta
- -gui: don't require gtk2 (__requires_exclude_from platformthemes) (#1154884)

* Sat Oct 18 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.4.0-0.1.beta
- 5.4.0-beta
- avoid extra -devel deps by moving *Plugin.cmake files to base pkgs
- support bootstrap macro, to disable -doc,-examples

* Mon Oct 13 2014 Jan Grulich <jgrulich@redhat.com> 5.3.2-3
- QFileDialog: implement getOpenFileUrl and friends for real

* Thu Oct 09 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-2
- use linux-g++ platform unconditionally

* Thu Oct 09 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.3.2-1.1
- F20: require libxkbcommon >= 0.4.1, only patch for the old libxcb

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Wed Aug 27 2014 David Tardon <dtardon@redhat.com> - 5.3.1-8
- do a normal build with docs

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 5.3.1-7
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.3.1-5
- drop dep on xorg-x11-xinit (own shared dirs instead)
- fix/improve qtchooser support using alternatives (#1122316)

* Mon Jun 30 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.3.1-4
- support the old versions of libxcb and libxkbcommon in F19 and F20
- don't use the bundled libxkbcommon

* Mon Jun 30 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-3
- -devel: Requires: pkgconfig(egl)

* Fri Jun 27 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-2
- Prefer QPA implementation in qsystemtrayicon_x11 if available

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-6
- %%ix86: build -no-sse2 (#1103185)

* Tue May 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-5
- BR: pkgconfig(xcb-xkb) > 1.10 (f21+)
- allow possibility for libxkbcommon-0.4.x only

* Fri May 23 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-4
- -system-libxkbcommon (f21+)

* Thu May 22 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-3
- qt5-qtbase-5.3.0-2.fc21 breaks keyboard input (#1100213)

* Wed May 21 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-2
- limit -reduce-relocations to %%ix86 x86_64 archs (QTBUG-36129)

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Thu Apr 24 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-8
- DoS vulnerability in the GIF image handler (QTBUG-38367)

* Wed Mar 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-7
- support ppc64le multilib (#1080629)

* Wed Mar 12 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.2.1-6
- reenable documentation

* Sat Mar 08 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.2.1-5
- make the QMAKE_STRIP sed not sensitive to whitespace (see #1074041 in Qt 4)

* Tue Feb 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-4
- undefine QMAKE_STRIP (and friends), so we get useful -debuginfo pkgs (#1065636)

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- bootstrap for libicu bump

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- qconfig.pri: +alsa +kms +pulseaudio +xcb-sm

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Sat Feb 01 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-11
- better %%rpm_macros_dir handling

* Wed Jan 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.2.0-10
- fix the allow-forcing-llvmpipe patch to patch actual caller of __glXInitialize

* Wed Jan 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.2.0-9
- use software OpenGL (llvmpipe) if the hardware driver doesn't support OpenGL 2

* Tue Jan 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-8
- (re)enable -docs

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-7
- unconditionally enable freetype lcd_filter
- (temp) disable docs (libxcb bootstrap)

* Sun Jan 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-6
- fix %%_qt5_examplesdir macro

* Sat Jan 25 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-5
- -examples subpkg

* Mon Jan 13 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.2.0-4
- fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
- fix QTBUG-35460 (error message for CVE-2013-4549 is misspelled)
- reenable docs on Fedora (accidentally disabled)

* Mon Jan 13 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-3
- move sql build deps into subpkg sections
- macro'ize ibase,tds support (disabled on rhel)

* Thu Jan 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- -devel: qtsql apparently wants all drivers available at buildtime

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Fri Dec 06 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.12.rc1
- qt5-base-devel.x86_64 qt5-base-devel.i686 file conflict qconfig.h (#1036956)

* Thu Dec 05 2013 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-0.11.rc1
- needs a minimum version on sqlite build dependency (#1038617)
- fix build when doc macro not defined

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1
- revert/omit recent egl packaging changes
- -doc install changes-5.* files here (#989149)

* Tue Nov 26 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.8.beta1.20131108_141
- Install changes-5.x.y file (#989149)

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.7.beta1.20131108_141
- enable -doc only on primary archs (allow secondary bootstrap)

* Fri Nov 22 2013 Lubomir Rintel <lkundrak@v3.sk> 5.2.0-0.6.beta1.20131108_141
- Enable EGL support

* Sat Nov 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1.20131108_141
- 2013-11-08_141 snapshot, arm switch qreal double

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.alpha
- disable -docs (for ppc bootstrap mostly)

* Wed Oct 16 2013 Lukáš Tinkl <ltinkl@redhat.com> - 5.2.0-0.2.alpha
- Fixes #1005482 - qtbase FTBFS on ppc/ppc64

* Tue Oct 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-0.1.alpha
- 5.2.0-alpha
- -system-harfbuzz
- rename subpkg -x11 => -gui
- move some gui-related plugins base => -gui
- don't use symlinks in %%_qt5_bindir (more qtchooser-friendly)

* Fri Sep 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 5.1.1-6
- -doc subpkg (not enabled)
- enable %%check

* Mon Sep 23 2013 Dan Horák <dan[at]danny.cz> - 5.1.1-5
- fix big endian builds

* Wed Sep 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-4
- macros.qt5: use newer location, use unexpanded macros

* Sat Sep 07 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-3
- ExcludeArch: ppc64 ppc (#1005482)

* Fri Sep 06 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- BR: pkgconfig(libudev) pkgconfig(xkbcommon) pkgconfig(xcb-xkb)

* Tue Aug 27 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 5.0.2-8
- Perl 5.18 rebuild

* Tue Jul 30 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-7
- enable qtchooser support

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.0.2-6
- Perl 5.18 rebuild

* Wed May 08 2013 Than Ngo <than@redhat.com> - 5.0.2-5
- add poll support, thanks to fweimer@redhat.com (QTBUG-27195)

* Thu Apr 18 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-4
- respin lowmem patch to apply (unconditionally) to gcc-4.7.2 too

* Fri Apr 12 2013 Dan Horák <dan[at]danny.cz> - 5.0.2-3
- rebase the lowmem patch

* Wed Apr 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- more cmake_path love (#929227)

* Wed Apr 10 2013 Rex Dieter <rdieter@fedoraproject.org> - 5.0.2-1
- 5.0.2
- fix cmake config (#929227)

* Tue Apr 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-0.1.rc1
- 5.0.2-rc1

* Sat Mar 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-6
- pull in upstream gcc-4.8.0 buildfix

* Tue Feb 26 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-5
- -static subpkg, Requires: fontconfig-devel,glib2-devel,zlib-devel
- -devel: Requires: pkgconfig(gl)

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-4
- create/own %%{_qt5_plugindir}/iconengines
- -devel: create/own %%{_qt5_archdatadir}/mkspecs/modules
- cleanup .prl

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-3
- +%%_qt5_libexecdir

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-2
- macros.qt5: fix %%_qt5_headerdir, %%_qt5_datadir, %%_qt5_plugindir

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- 5.0.1
- lowmem patch for %%arm, s390

* Wed Jan 30 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-4
- %%build: -system-pcre, BR: pkgconfig(libpcre)
- use -O1 optimization on lowmem (s390) arch

* Thu Jan 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-3
- enable (non-conflicting) qtchooser support

* Wed Jan 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-2
- add qtchooser support (disabled by default)

* Wed Dec 19 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-1
- 5.0 (final)

* Thu Dec 13 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-0.4.rc2
- 5.0-rc2
- initial try at putting non-conflicting binaries in %%_bindir

* Thu Dec 06 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-0.3.rc1
- 5.0-rc1

* Wed Nov 28 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-0.2.beta2
- qtbase --> qt5-qtbase

* Mon Nov 19 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-0.1.beta2
- %%build: -accessibility
- macros.qt5: +%%_qt5_archdatadir +%%_qt5_settingsdir
- pull in a couple more configure-related upstream patches

* Wed Nov 14 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-0.0.beta2
- first try

