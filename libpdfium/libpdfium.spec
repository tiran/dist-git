# for pypdfium2-4.30.0
%global pdfium_build 6462

%bcond_without ctypesgen
%global ctypesgen_commit ebd495b1733b60132151154d6358fd1eb336a36a

# https://pdfium.googlesource.com/pdfium/+/refs/heads/chromium/6462

%global pdfium_commit 7b7c83fba6d0af8d8847ee606569c35880512995
%global pdfium_commitdate 20240502
%global pdfium_shortcommit %(c=%{pdfium_commit}; echo ${c:0:8})

# git ls-remote --sort -version:refname --tags https://chromium.googlesource.com/chromium/src '*.*.6462.0'
# ...        refs/tags/126.0.6462.0
%global pdfium_major 126
%global pdfium_minor 0
%global pdfium_patch 0


%if 0%{?fedora} || 0%{?rhel} >= 10
%bcond_without openjpeg2
%else
# RHEL 9.4 has OpenJPEG2 2.4
%bcond_with openjpeg2
%endif

Name:           libpdfium
Version:        %{pdfium_build}^%{pdfium_commitdate}git%{pdfium_shortcommit}
Release:        3%{?dist}
Summary:        Library for PDF rendering, inspection, manipulation and creation

License:        Apache 2.0
URL:            https://pdfium.googlesource.com/pdfium
Source0:        libpdfium-%{pdfium_build}.tar.gz
Source1:        args.gn
Source2:        passflags-BUILD.gn
Source3:        https://github.com/pypdfium2-team/ctypesgen/archive/%{ctypesgen_commit}.tar.gz#/ctypesgen-%{ctypesgen_commit}.tar.gz

# patches to use public headers, export public names, and to build libpdfium.so
# https://github.com/bblanchon/pdfium-binaries/tree/chromium/6721/patches
Patch1:         public_headers.patch
Patch2:         shared_library.patch

BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  pkgconfig
BuildRequires:  redhat-rpm-config
BuildRequires:  libatomic

BuildRequires:  gn
BuildRequires:  ninja-build
%if %{with ctypesgen}
BuildRequires:  python3
%endif

# de-vendored dependencies
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libjpeg)
%if %{with openjpeg2}
BuildRequires:  pkgconfig(libopenjp2) >= 2.5
%endif
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(zlib)

# https://sourceforge.net/projects/agg/ 2.3 + security patches
Provides:       bundled(agg) = 2.3
%if %{without openjpeg2}
# OpenJPEG2 2.5.0 + security fixes
Provides:       bundled(openjpeg2) = 2.5.0
%endif
Provides:       bundled(abseil-cpp)
Provides:       %{name}(build) = %{pdfium_build}
Provides:       %{name}(version) = %{pdfium_major}.%{pdfium_minor}.%{pdfium_build}.%{pdfium_patch}


%description
Library for PDF rendering, inspection, manipulation and creation

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if %{with ctypesgen}
%package        ctypesgen
Summary:        ctypes bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}(ctypesgen) = %{ctypesgen_commit}

%description    ctypesgen
The %{name}-ctypesgen package contains ctypes bindings for %{name}. The
bindings were generated with https://github.com/pypdfium2-team/ctypesgen from
commit %{ctypesgen_commit}.
%endif


%prep
%autosetup -p1 -b 0 -n libpdfium-%{pdfium_build}
%if %{with ctypesgen}
%setup -T -D -q -a 3 -n libpdfium-%{pdfium_build}
%endif

# build configuration
install -D -m=644 %{SOURCE1} out/args.gn
%if %{with openjpeg2}
echo "use_system_libopenjpeg2 = true" >> out/args.gn
%else
echo "use_system_libopenjpeg2 = false" >> out/args.gn
%endif

# custom flavor of GCC toolchain that passes CFLAGS, CXXFLAGS, etc.
install -D -m=644 %{SOURCE2} build/toolchain/linux/passflags/BUILD.gn

# generate Ninja files with build flags
%set_build_flags
# build system does not define macro for some dependencies
export CPPFLAGS="-DUSE_SYSTEM_LCMS2=1 $CPPFLAGS"
gn gen out


%build
%ninja_build -C out pdfium

%if %{with ctypesgen}
# pypdfium2 ctypesgen bindings
# https://github.com/pypdfium2-team/pypdfium2/blob/4.30.0/autorelease/bindings.py
# https://github.com/pypdfium2-team/pypdfium2/blob/4.30.0/setupsrc/pypdfium2_setup/packaging_base.py

mkdir -p out/ctypesgen

PYTHONPATH=ctypesgen-%{ctypesgen_commit}/src python3 -m ctypesgen \
    -l pdfium \
    --no-load-library \
    --no-macro-guards \
    -D PDF_ENABLE_V8 PDF_ENABLE_XFA PDF_USE_SKIA \
    --symbol-rules 'if_needed=\w+_$|\w+_t$|_\w+' \
    --headers ./public/fpdf*.h \
    -o out/ctypesgen/bindings.py

# remove 'public/' prefix from comments
sed -i 's,public/,,g' out/ctypesgen/bindings.py

cat > "out/ctypesgen/version.json" << EOF
{
  "major": %{pdfium_major},
  "minor": %{pdfium_minor},
  "build": %{pdfium_build},
  "patch": %{pdfium_patch},
  "n_commits": 0,
  "hash": "%{pdfium_commit}",
  "origin": "system",
  "flags": []
}
EOF

%endif


%install
mkdir -p %{buildroot}%{_libdir}
cp out/libpdfium.so %{buildroot}%{_libdir}

mkdir -p %{buildroot}%{_includedir}
cp public/*.h %{buildroot}%{_includedir}

%if %{with ctypesgen}
mkdir -p %{buildroot}%_datarootdir/%{name}/ctypesgen/
cp out/ctypesgen/* %{buildroot}%_datarootdir/%{name}/ctypesgen/
%endif

%files
%license LICENSE
%doc AUTHORS out/args.gn
# PDFium build system does not include a soname
# pypdfium2 needs "libpdfium.so"
%{_libdir}/*.so

%files devel
%doc README.md
%{_includedir}/*

%if %{with ctypesgen}
%files ctypesgen
%_datarootdir/%{name}/ctypesgen/
%endif

%changelog
* Tue Oct 22 2024 Christian Heimes <cheimes@redhat.com> - 6462^20240502git7b7c83fb-3
- Build ctypes bindings with ctypesgen

* Mon Sep 30 2024 Christian Heimes <cheimes@redhat.com> - 6462^20240502git7b7c83fb-2
- use OpenJPEG2 on Fedora and EL10

* Fri Sep 27 2024 Christian Heimes <cheimes@redhat.com> - 6462^20240502git7b7c83fb-1
- Build tag 6462 for pypdfium2-4.30.0
