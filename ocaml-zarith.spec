#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	zarith
Summary:	Zarith: arbitrary-precision integers
Summary(pl.UTF-8):	Zarith - liczby całkowite dowolnej precyzji
Name:		ocaml-zarith
Version:	1.12
Release:	5
License:	LGPL v2 with linking exception
Group:		Applications/Math
#Source0Download: https://github.com/ocaml/Zarith/releases
Source0:	https://github.com/ocaml/Zarith/archive/release-%{version}/Zarith-%{version}.tar.gz
# Source0-md5:	bf368f3d9e20b6b446d54681afc05a04
URL:		http://github.com/ocaml/Zarith
BuildRequires:	bash
BuildRequires:	gmp-devel
BuildRequires:	ocaml >= 1:4.04
BuildRequires:	ocaml-findlib
BuildRequires:	perl-base
%requires_eq	ocaml-runtime
# does not work on x32 because sizeof(intnat) != sizeof(mp_limb_t) (4 != 8)
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Zarith library implements arithmetic and logical operations over
arbitrary-precision integers. It uses GMP to efficiently implement
arithmetic over big integers. Small integers are represented as Caml
unboxed integers, for speed and space economy.

%description -l pl.UTF-8
Biblioteka Zarith implementuje operacje arytmetyczne i logiczne na
liczbach całkowitych dowolnej precyzji. Wykorzystuje gmp do wydajnej
arytmetyki na dużych liczbach całkowitych. Małe liczby całkowite są
reprezentowane jako nieograniczone liczby całkowite Camla, aby zyskać
na szybkości i rozmiarze.

%package devel
Summary:	Zarith library development files
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Zarith
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
Zarith library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne do tworzenia programów w OCamlu
przy użyciu biblioteki Zarith.

%prep
%setup -q -n Zarith-release-%{version}

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
./configure \
	-installdir $RPM_BUILD_ROOT%{_libdir}/ocaml \
	-gmp

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/

# not required with system package manager
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.so.owner

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes LICENSE README.md
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllzarith.so
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/META
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/%{module}/zarith.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/%{module}/*.cm[axi]
%{_libdir}/ocaml/%{module}/*.mli
%{_libdir}/ocaml/%{module}/*.cmti
%{_libdir}/ocaml/%{module}/libzarith.a
%{_libdir}/ocaml/%{module}/zarith.h
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/zarith.a
%{_libdir}/ocaml/%{module}/zarith.cmxa
%endif
