#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	zarith
Summary:	Zarith: arbitrary-precision integers
Name:		ocaml-zarith
Version:	1.2.1
Release:	3
License:	GPL
Group:		Applications/Math
Source0:	http://forge.ocamlcore.org/frs/download.php/1199/%{module}-%{version}.tgz
# Source0-md5:	b507aaf2469103bb9e54291ff8def5c7
URL:		http://forge.ocamlcore.org/projects/zarith
BuildRequires:	bash
BuildRequires:	gmp-devel
BuildRequires:	ocaml >= 3.09.0
BuildRequires:	camlp5 >= 5.01
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Zarith library implements arithmetic and logical operations over
arbitrary-precision integers. It uses GMP to efficiently implement
arithmetic over big integers. Small integers are represented as Caml
unboxed integers, for speed and space economy.

%package devel
Summary:	Zarith library development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
zarith library.

%prep
%setup -q -n %{module}-%{version}

%build
CFLAGS="%{rpmcflags}" \
./configure \
	-installdir $RPM_BUILD_ROOT/%{_libdir}/ocaml \
	-gmp

%{__make} VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
mv $OCAMLFIND_DESTDIR/%{module}/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META
directory="+%{module}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner
%dir %{_libdir}/ocaml/%{module}
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.cmxs
%endif
%{_libdir}/ocaml/site-lib/%{module}

%files devel
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/ocaml/%{module}/*.cm[axi]
%{_libdir}/ocaml/%{module}/*.mli
%{_libdir}/ocaml/%{module}/*.h
%{_libdir}/ocaml/%{module}/libzarith.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/zarith.a
%{_libdir}/ocaml/%{module}/*.cmxa
%endif
