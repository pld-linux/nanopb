#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	Nanopb - Protocol Buffers for Embedded Systems
Summary(pl.UTF-8):	Nanopb - Protocol Buffers dla systemów wbudowanych
Name:		nanopb
Version:	0.4.9.1
Release:	1
License:	BSD-like
Group:		Libraries
#Source0Download: https://github.com/nanopb/nanopb/tags
Source0:	https://github.com/nanopb/nanopb/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a974c454f4cb245b3552f3fea233a3fa
Patch0:		%{name}-config.patch
URL:		https://jpa.kapsi.fi/nanopb/
BuildRequires:	cmake >= 3.14.0
%{?with_apidocs:BuildRequires:	pandoc}
BuildRequires:	protobuf
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-modules >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nanopb is a small code-size Protocol Buffers implementation in ANSI C.
It is especially suitable for use in microcontrollers, but fits any
memory restricted system.

%description -l pl.UTF-8
Nanopb to mała pod względem rozmiaru kodu implementacja Protocol
Buffers w ANSI C. Jest przydatna szczególnie dla mikrokontrolerów, ale
nadaje się dla każdego systemu o ograniczonej pamięci.

%package devel
Summary:	Header files for Nanopb library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Nanopb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python3
Requires:	python3-modules
Requires:	python3-protobuf

%description devel
Header files for Nanopb library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Nanopb.

%package static
Summary:	Static Nanopb library
Summary(pl.UTF-8):	Statyczna biblioteka Nanopb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Nanopb library.

%description static -l pl.UTF-8
Statyczna biblioteka Nanopb.

%package apidocs
Summary:	API documentation for Nanopb library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Nanopb
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Nanopb library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Nanopb.

%prep
%setup -q
%patch -P0 -p1

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	extra/script_wrappers/nanopb_generator.py.in \
	generator/nanopb_generator \
	generator/nanopb_generator.py \
	generator/protoc-gen-nanopb

%build
install -d build
cd build
%cmake .. \
	-DBUILD_SHARED_LIBS=ON \
	%{!?with_static_libs:-DBUILD_STATIC_LIBS=OFF}

%{__make}
cd ..

%if %{with apidocs}
%{__make} -C docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}/{nanopb,proto}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}/{nanopb,proto}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGELOG.txt LICENSE.txt README.md
%attr(755,root,root) %{_libdir}/libprotobuf-nanopb.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nanopb_generator
%attr(755,root,root) %{_bindir}/nanopb_generator.py
%attr(755,root,root) %{_bindir}/protoc-gen-nanopb
%attr(755,root,root) %{_libdir}/libprotobuf-nanopb.so
%{_includedir}/nanopb
%{py3_sitescriptdir}/nanopb
%{_libdir}/cmake/nanopb

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libprotobuf-nanopb.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/{logo,*.css,*.html,*.svg}
%endif
