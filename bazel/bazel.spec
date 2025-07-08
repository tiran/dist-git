# Based on Vincent Batts' work
# https://github.com/vbatts/copr-build-bazel/blob/master/bazel.spec

%global bazel_major 6
%global jdk_version 11

Name:           bazel%{bazel_major}
Version:        6.5.0
Release:        1%{?dist}
Summary:        Correct, reproducible, and fast builds for everyone.
License:        Apache License 2.0
URL:            http://bazel.build/
Source0:        https://github.com/bazelbuild/bazel/releases/download/%{version}/bazel-%{version}-dist.zip


# FIXME: Java 11 log.warning generates backtrace
Patch1:         bazel-1.0.0-log-warning.patch

Provides:	bazel = %{version}
Provides:	bazel = %{bazel_major}

BuildRequires:  java-%{jdk_version}-openjdk-devel
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  findutils
BuildRequires:  gcc-c++
BuildRequires:  which
BuildRequires:  unzip
BuildRequires:  zip
BuildRequires:  python3

Requires:         findutils
Requires:         java-%{jdk_version}-openjdk-devel
Requires(post):   alternatives
Requires(postun): alternatives


%define bashcompdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null)
# no debug symbols
%global debug_package %{nil}
# disable strip and compress as this removes the embedded zip file from real bazel binary
%define __os_install_post %{nil}


%description
Correct, reproducible, and fast builds for everyone. Bazel is a tool for automation of
building and testing software.


%prep
%autosetup -p0 -c -n bazel-%{version}
chmod -x AUTHORS CHANGELOG.md README.md LICENSE


%build
export JAVA_HOME="/usr/lib/jvm/java-%{jdk_version}-openjdk"
export EXTRA_BAZEL_ARGS="${EXTRA_BAZEL_ARGS} --python_path=/usr/bin/python3"
%ifarch aarch64
export EXTRA_BAZEL_ARGS="${EXTRA_BAZEL_ARGS} --nokeep_state_after_build --notrack_incremental_state --nokeep_state_after_build"
%endif
%ifarch s390x
# increase heap size to addess s390x build failures
export BAZEL_JAVAC_OPTS="-J-Xmx4g -J-Xms512m"
%endif

# loose epoch from their release date
export SOURCE_DATE_EPOCH="$(date -d $(head -1 CHANGELOG.md | %{__grep} -Eo '\b[[:digit:]]{4}-[[:digit:]]{2}-[[:digit:]]{2}\b' ) +%s)"
export EMBED_LABEL="%{version}"

export TMPDIR=%{_tmppath}
export CC=gcc
export CXX=g++
export EXTRA_BAZEL_ARGS="${EXTRA_BAZEL_ARGS} --sandbox_debug --tool_java_runtime_version=local_jdk --verbose_failures --subcommands --explain=build.log --show_result=2147483647"
./compile.sh

./scripts/generate_bash_completion.sh --bazel=output/bazel --output=output/bazel-complete.bash


%install
%{__mkdir_p} %{buildroot}/%{_bindir}
touch %{buildroot}%{_bindir}/bazel
touch %{buildroot}/%{_bindir}/bazel-real
%{__cp} output/bazel %{buildroot}/%{_bindir}/bazel-%{version}-%{_os}-%{_arch}
# wrapper script has to be in the same directory as real bazel binary
%{__cp} ./scripts/packages/bazel.sh %{buildroot}/%{_bindir}/.bazel-%{bazel_major}
%{__mkdir_p} %{buildroot}/%{bashcompdir}
%{__cp} output/bazel-complete.bash %{buildroot}/%{bashcompdir}/bazel-%{bazel_major}


%post
alternatives --install %{_bindir}/bazel bazel %{_bindir}/.bazel-%{bazel_major} 1 \
    --follower %{_bindir}/bazel-real bazel-real %{_bindir}/bazel-%{version}-%{_os}-%{_arch}


%postun
if [ $1 -eq 0 ] ; then
  alternatives --remove bazel %{_bindir}/bazel-%{bazel_major}
fi


%files
%license LICENSE
%doc AUTHORS CHANGELOG.md README.md
%defattr(-,root,root)
%ghost %{_bindir}/bazel
%ghost %{_bindir}/bazel-real
%attr(0755,root,root) %{_bindir}/.bazel-%{bazel_major}
%attr(0755,root,root) %{_bindir}/bazel-%{version}-%{_os}-%{_arch}
%attr(0755,root,root) %{bashcompdir}/bazel-%{bazel_major}


%changelog
* Tue Jul 08 2025 Christian Heimes <cheimes@redhat.com> - 6.5.0-1
- Build 6.5.0
- Fix building with local JDK
- Use alternatives to support multiple Bazel major versions
- Remove old workarounds for RHEL < 9 and Python 2
- Include LICENSE, AUTHORS, CHANGELOG.md, and README.md
