Name:		mock-pandoc
Version:	0.0.1
Release:	1%{?dist}
Summary:	Mock pandoc package for habanalabs-rdma-core
License:	GPL-2.0-or-later
Source0:	LICENSE
BuildArch:	noarch
Provides:	pandoc = %{version}

%description
Mock pandoc package to satisfy habanalabs-rdma-core dependency. The
habanalabs package depends on pandoc to build man pages in its postinst
scriplet. Tests have shown that the package installs and works fine without
pandoc.

%prep
cp %{SOURCE0} .

%build

%install

%files
%license LICENSE

%changelog
* Wed Aug 07 2024 Christian Heimes <cheimes@redhat.com> - 0.0.1-1
- Initial package
