# based on https://src.fedoraproject.org/rpms/sentencepiece
%bcond_without python

Name:		sentencepiece
Version:	0.2.0
Release:	1%{?dist}
Summary:	An unsupervised text tokenizer for Neural Network-based text generation

License:	Apache-2.0
URL:		https://github.com/google/sentencepiece
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	gcc-c++
BuildRequires:	cmake
BuildRequires:	ninja-build
# for tcmalloc
BuildRequires:	gperftools-devel
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:  pkgconfig(protobuf-lite)
%endif

%description
The SentencePiece is an unsupervised text tokenizer for Neural Network-based
text generation.
It is an unsupervised text tokenizer and detokenizer mainly for
Neural Network-based text generation systems where the vocabulary size is
predetermined prior to the neural model training.
SentencePiece implements subword units and unigram language model with the
extension of direct training from raw sentences.
SentencePiece allows us to make a purely end-to-end system that does not
depend on language-specific pre/post-processing.

%package libs
Summary:	Runtime libraries for SentencePiece

%description libs
This package contains the libraries for SentencePiece.

%package tools
Summary:	Tools for SentencePiece
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description tools
This package contains tools for manipulate models for SentencePiece.

%package devel
Summary:	Libraries and header files for SentencePiece
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains header files to develop a software using SentencePiece.

%if %{with python}
%package        -n python3-%{name}
Summary:	Python module for SentencePiece
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
This package contains Python3 module file for SentencePiece.
%endif

%prep
%autosetup

%build
%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release

%cmake_build

%if %{with python}
pushd python
CFLAGS="-I../src" LDFLAGS="-L../%{_vpath_builddir}/src -lsentencepiece" PKG_CONFIG_PATH="../%{_vpath_builddir}" %py3_build
popd
%endif

%install
%cmake_install

rm %{buildroot}%{_libdir}/libsentencepiece*.a

%if %{with python}
pushd python
%py3_install
popd
%endif


%files libs
%doc README.md
%license LICENSE
%{_libdir}/libsentencepiece*.so.0*

%files devel
%{_includedir}/sentencepiece*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/sentencepiece*.pc

%files tools
%{_bindir}/spm*

%if %{with python}
%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-*.egg-info/
%endif


%changelog
* Tue Oct 01 2024 Christian Heimes <cheimes@redhat.com> - 0.2.0-1
- New upstream release 0.2.0
- Build for s390x again

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.99-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.1.99-3
- Rebuilt for Python 3.13

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 23 2023 topazus <topazus@outlook.com> - 0.1.99-1
- update to 0.1.99

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.92-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.1.92-10
- Rebuilt for Python 3.12

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.92-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.92-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.1.92-7
- Rebuilt for Python 3.11

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.92-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.92-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.1.92-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 07 2020 Kentaro Hayashi <kenhys@gmail.com> - 0.1.92-2
- Add missing BuildRequires: python3-setuptools

* Thu Oct 01 2020 Kentaro Hayashi <kenhys@gmail.com> - 0.1.92-1
- New upstream release

* Tue Sep 22 2020 Jeff Law <law@redhat.com> - 0.1.84-6
- Use cmake_in_source_build to fix FTBFS due to recent cmake macro changes

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.84-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.84-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.1.84-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.84-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Kentaro Hayashi <hayashi@clear-code.com> - 0.1.84-1
- New upstream release

* Mon Oct 07 2019 Kentaro Hayashi <hayashi@clear-code.com> - 0.1.83-1
- initial packaging
