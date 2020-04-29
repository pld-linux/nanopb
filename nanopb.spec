#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Nanopb - Protocol Buffers for Embedded Systems
Summary(pl.UTF-8):	Nanopb - Protocol Buffers dla systemów wbudowanych
Name:		nanopb
Version:	0.4.1
Release:	1
License:	BSD-like
Group:		Libraries
#Source0Download: https://github.com/nanopb/nanopb/releases
Source0:	https://github.com/nanopb/nanopb/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3e40a0b3af23259be4957fde9d4c4a22
URL:		https://jpa.kapsi.fi/nanopb/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	python >= 1:2.7
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

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DBUILD_SHARED_LIBS=ON \
	%{!?with_static_libs:-DBUILD_STATIC_LIBS=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGELOG.txt LICENSE.txt README.md docs/{*.rst,*.css,logo}
%attr(755,root,root) %{_libdir}/libprotobuf-nanopb.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprotobuf-nanopb.so
%{_includedir}/pb*.h
%{_libdir}/cmake/nanopb

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libprotobuf-nanopb.a
%endif
