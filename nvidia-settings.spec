Name:           nvidia-settings
Version:        340.96
Release:        1%{?dist}
Summary:        Configure the NVIDIA graphics driver
Epoch:          2
License:        GPLv2+
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  %{ix86} x86_64 armv7hl

Source0:        ftp://download.nvidia.com/XFree86/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}-load.desktop
Patch0:         %{name}-256.35-validate.patch
Patch1:         %{name}-340.17-libXNVCtrl-so.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel > 2.4
BuildRequires:  jansson-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
BuildRequires:  m4
BuildRequires:  mesa-libGL-devel

Requires:       nvidia-libXNVCtrl = %{?epoch}:%{version}-%{release}

Obsoletes:      nvidia-settings-desktop < %{?epoch}:%{version}-%{release}

%description
The %{name} utility is a tool for configuring the NVIDIA graphics
driver. It operates by communicating with the NVIDIA X driver, querying and
updating state as appropriate.

This communication is done with the NV-CONTROL X extension.

%package -n nvidia-libXNVCtrl
Summary:        Library providing the NV-CONTROL API
Obsoletes:      libXNVCtrl < %{?epoch}:%{version}-%{release}
Provides:       libXNVCtrl = %{?epoch}:%{version}-%{release}

%description -n nvidia-libXNVCtrl
This library provides the NV-CONTROL API for communicating with
the proprietary NVidia xorg driver. It is required for proper operation of the
%{name} utility.

%package -n nvidia-libXNVCtrl-devel
Summary:        Development files for libXNVCtrl
Requires:       nvidia-libXNVCtrl = %{?epoch}:%{version}-%{release}
Requires:       libX11-devel

%description -n nvidia-libXNVCtrl-devel
This devel package contains libraries and header files for
developing applications that use the NV-CONTROL API.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

find . -name "*.la" -delete
find . -name "*.a" -delete
# rpmlint fixes
find . -name "*.h" -exec chmod 644 {} \;

sed -i -e 's|/usr/local|%{_prefix}|g' utils.mk
sed -i -e 's|-lXxf86vm|-lXxf86vm -ldl -lm|g' Makefile

%build
export CFLAGS="$RPM_OPT_FLAGS"
make %{?_smp_mflags} \
    NV_VERBOSE=1 \
    X_LDFLAGS="-L%{_libdir}" \
    STRIP_CMD="true" \
    NV_USE_BUNDLED_LIBJANSSON=0 \
    XNVCTRL_LIB_STATIC=0

%install
# Install libXNVCtrl
mkdir -p %{buildroot}%{_libdir}/
mkdir -p %{buildroot}%{_includedir}/NVCtrl
cp -af src/libXNVCtrl/libXNVCtrl.so* %{buildroot}%{_libdir}/
chmod 755 %{buildroot}%{_libdir}/*.so*
cp -af src/libXNVCtrl/*.h %{buildroot}%{_includedir}/NVCtrl/

# Install main program
make install DESTDIR=%{buildroot} INSTALL="install -p" NV_USE_BUNDLED_LIBJANSSON=0

# Install desktop file
mkdir -p %{buildroot}%{_datadir}/{applications,pixmaps}
desktop-file-install --dir %{buildroot}%{_datadir}/applications/ doc/%{name}.desktop
cp doc/%{name}.png %{buildroot}%{_datadir}/pixmaps/
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# Install autostart file to load settings at login
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-load.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-load.desktop

%post -n nvidia-libXNVCtrl -p /sbin/ldconfig

%postun -n nvidia-libXNVCtrl -p /sbin/ldconfig

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/%{name}.*
%{_sysconfdir}/xdg/autostart/%{name}-load.desktop

%files -n nvidia-libXNVCtrl
%doc COPYING
%{_libdir}/libXNVCtrl.so.*

%files -n nvidia-libXNVCtrl-devel
%doc doc/NV-CONTROL-API.txt doc/FRAMELOCK.txt
%{_includedir}/NVCtrl
%{_libdir}/libXNVCtrl.so

%changelog
* Tue Nov 17 2015 Simone Caronni <negativo17@gmail.com> - 2:340.96-1
- Update to 340.96.

* Tue Sep 08 2015 Simone Caronni <negativo17@gmail.com> - 2:340.93-1
- Update to 340.93.

* Wed Jan 28 2015 Simone Caronni <negativo17@gmail.com> - 2:340.76-1
- Update to 340.76.

* Mon Dec 08 2014 Simone Caronni <negativo17@gmail.com> - 2:340.65-1
- Update to 340.65.

* Wed Nov 05 2014 Simone Caronni <negativo17@gmail.com> - 2:340.58-1
- Update to 340.58.

* Wed Oct 01 2014 Simone Caronni <negativo17@gmail.com> - 2:340.46-1
- Update to 340.46.
- Switched to GitHub sources.

* Sun Aug 17 2014 Simone Caronni <negativo17@gmail.com> - 2:340.32-1
- Update to 340.32.

* Tue Jul 08 2014 Simone Caronni <negativo17@gmail.com> - 2:340.24-1
- Update to 340.24.

* Mon Jun 09 2014 Simone Caronni <negativo17@gmail.com> - 2:340.17-1
- Update to 340.17.
- Removed upstreamed patch.

* Tue Jun 03 2014 Simone Caronni <negativo17@gmail.com> - 2:337.25-2
- Fix requirements.

* Mon Jun 02 2014 Simone Caronni <negativo17@gmail.com> - 2:337.25-1
- Update to 337.25.

* Fri May 09 2014 Simone Caronni <negativo17@gmail.com> - 2:337.19-2
- Load settings at login.

* Tue May 06 2014 Simone Caronni <negativo17@gmail.com> - 2:337.19-1
- Update to 337.19.

* Tue Apr 08 2014 Simone Caronni <negativo17@gmail.com> - 2:337.12-1
- Update to 337.12.

* Tue Mar 04 2014 Simone Caronni <negativo17@gmail.com> - 2:334.21-1
- Update to 334.21.

* Wed Feb 19 2014 Simone Caronni <negativo17@gmail.com> - 2:331.49-1
- Update to 331.49.

* Tue Jan 14 2014 Simone Caronni <negativo17@gmail.com> - 2:331.38-1
- Update to 331.38.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-2
- Make libXNVCtrl an external library (adapted from Debian):
    Obsolete (useless) Fedora libXNVCtrl library.
    Make dynamic shared object optional at compile time.
    Version libXVNCtrl library according to driver version.
- Link libraries as needed, removing empty dependencies.
- Do not strip binaries during build, let rpm generate debuginfo files.

* Thu Nov 07 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-1
- Update to 331.20.

* Wed Oct 23 2013 Simone Caronni <negativo17@gmail.com> - 2:331.17-1
- Updated to 331.17.

* Fri Oct 04 2013 Simone Caronni <negativo17@gmail.com> - 2:331.13-1
- Update to 331.13.

* Mon Sep 09 2013 Simone Caronni <negativo17@gmail.com> - 2:325.15-1
- Update to 325.15.

* Wed Aug 07 2013 Simone Caronni <negativo17@gmail.com> - 2:319.49-1
- Updated to 319.49.

* Tue Jul 02 2013 Simone Caronni <negativo17@gmail.com> - 2:319.32-2
- Add armv7hl support.

* Fri Jun 28 2013 Simone Caronni <negativo17@gmail.com> - 1:319.32-1
- Update to 319.32.

* Fri May 24 2013 Simone Caronni <negativo17@gmail.com> - 1:319.23-2
- Add missing m4 build requirement.

* Fri May 24 2013 Simone Caronni <negativo17@gmail.com> - 1:319.23-1
- Update to 319.23.

* Thu May 02 2013 Simone Caronni <negativo17@gmail.com> - 1:319.17-1
- Update to 319.17.
- Switch to ftp://download.nvidia.com/ sources.

* Mon Apr 22 2013 Simone Caronni <negativo17@gmail.com> - 1:319.12-2
- Obsoletes nvidia-settings.desktop.

* Wed Apr 10 2013 Simone Caronni <negativo17@gmail.com> - 1:319.12-1
- Started off from rpmfusion-nonfree packages.
- Updated to 319.12.
- Add libvdpau BuildRequires.
- Simplify spec file; move version to official version; drop 1.0.
- Remove split desktop package; simplify packaging.
