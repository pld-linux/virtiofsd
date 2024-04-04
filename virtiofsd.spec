Summary:	virtio-fs vhost-user device daemon
Summary(pl.UTF-8):	Demon urządzeń vhost-user virtio-fs
Name:		virtiofsd
Version:	1.10.1
Release:	1
License:	Apache v2.0 and BSD
Group:		Daemons
#Source0Download: https://gitlab.com/virtio-fs/virtiofsd/-/releases
Source0:	https://gitlab.com/virtio-fs/virtiofsd/-/archive/v%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	d6008962f8cca1998d04dd033d686ad2
Source1:	%{name}-vendor-v%{version}.tar.xz
# Source1-md5:	a63d6dd1d1f755893b31fbbf545b9636
Patch0:		%{name}-x86.patch
URL:		https://gitlab.com/virtio-fs/virtiofsd
BuildRequires:	cargo
BuildRequires:	libcap-ng-devel
BuildRequires:	libseccomp-devel
BuildRequires:	rust
Requires:	qemu-common >= 8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
virtio-fs vhost-user device daemon written in Rust.

%description -l pl.UTF-8
Demon urządzeń vhost-user virtio-fs, napisany w języku Rust.

%prep
%setup -q -n %{name}-v%{version}-3988b7304ceb2fdb4eed2c8bf8682e6ea19c4ecc -a1
%patch0 -p1

%{__sed} -i -e 's,/usr/libexec/,%{_libexecdir}/,' 50-virtiofsd.json

# Use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build \
	--frozen

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libexecdir},%{_datadir}/qemu/vhost-user}

export CARGO_HOME="$(pwd)/.cargo"

%cargo_install \
	--frozen \
	--path . \
	--root $RPM_BUILD_ROOT%{_prefix}

%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates.toml
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates2.json

%{__mv} $RPM_BUILD_ROOT%{_bindir}/virtiofsd $RPM_BUILD_ROOT%{_libexecdir}
cp -p 50-virtiofsd.json $RPM_BUILD_ROOT%{_datadir}/qemu/vhost-user

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE-BSD-3-Clause README.md doc/xattr-mapping.md
%attr(755,root,root) %{_libexecdir}/virtiofsd
%{_datadir}/qemu/vhost-user/50-virtiofsd.json
