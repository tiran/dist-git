Name:           json-schema-validator
Version:        2.3.0
Release:        1%{?dist}
Summary:        JSON schema validator for JSON for Modern C++

License:        MIT
URL:            https://github.com/pboettch/json-schema-validator
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:	ninja-build
BuildRequires:  json-devel


%description
This is a C++ library for validating JSON documents based on a JSON Schema
which itself should validate with draft-7 of JSON Schema Validation.

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       json-devel

%description devel
%{name} development files


%prep
%autosetup -p1


%build
%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DJSON_VALIDATOR_BUILD_TESTS:BOOL=on \

%cmake_build


%check
%ctest


%install
%cmake_install

# remove test examples
rm %{buildroot}%{_bindir}/format-json-schema
rm %{buildroot}%{_bindir}/json-schema-validate
rm %{buildroot}%{_bindir}/readme-json-schema


%files
%license LICENSE
%doc README.md
%{_libdir}/libnlohmann_json_schema_validator.so.2
%{_libdir}/libnlohmann_json_schema_validator.so.%{version}


%files devel
%{_includedir}/nlohmann/json-schema.hpp
%{_libdir}/libnlohmann_json_schema_validator.so
%{_libdir}/cmake/nlohmann_json_schema_validator


%changelog
* Mon Sep 30 2024 Christian Heimes <cheimes@redhat.com> - 2.3.0-1
- initial build of 2.3.0
