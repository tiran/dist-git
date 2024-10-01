# based on https://src.fedoraproject.org/rpms/fasttext

%global commitversion 0.9.2
%global commit c86fcd1a9626a0b13c25cf055db82ddf97917865
%global commitdate 20241001
%global shortcommit %(c=%{commit}; echo ${c:0:8})

Name:     fasttext
Version:  %{commitversion}^%{commitdate}git%{shortcommit}
Release:  1%{?dist}
Summary:  Efficient learning of word representations and sentence classification

License:  MIT
# fork of https://github.com/facebookresearch/fastText
URL:      https://github.com/PeterStaar-IBM/fastText
Source0:  https://github.com/PeterStaar-IBM/fastText/archive/%{commit}.tar.gz#/fastText-%{commitversion}-%{shortcommit}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
Requires:	%{name}-libs = %{version}-%{release}

%description
The fastText is a library for efficient learning of
word representations and sentence classification.


%package libs
Summary:	Runtime libraries for fastText

%description libs
This package contains the libraries for fastText.


%package tools
Summary:	Tools for fastText
Requires:	%{name}-libs = %{version}-%{release}

%description tools
This package contains tools for manipulate models for fastText.


%package devel
Summary:	Libraries and header files for fastText
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains header files to develop a software using fastText.


%prep
%autosetup -p1 -n fastText-%{commit}


%build
%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS:BOOL=ON

%cmake_build


%check
%ctest


%install
%cmake_install
# don't ship static libs
rm %{buildroot}%{_libdir}/libfasttext*.a


%files 
%{_bindir}/fasttext


%files libs
%license LICENSE
%doc README.md
%{_libdir}/libfasttext.so.0


%files devel
%{_includedir}/fasttext/
%{_libdir}/libfasttext.so
%{_libdir}/pkgconfig/fasttext.pc


%changelog
* Tue Oct 01 2024 Christian Heimes <cheimes@redhat.com> - 0.9.2^20241001gitc86fcd1a-1
- initial build
