#
# Conditional build:
%bcond_without	opt		# build opt

Summary:	Zarith: arbitrary-precision integers
Name:		zarith
Version:	1.2.1
Release:	1
License:	GPL
Group:		Applications/Math
Source0:	http://forge.ocamlcore.org/frs/download.php/1199/%{name}-%{version}.tgz
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
%setup -q

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
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{name}
mv $OCAMLFIND_DESTDIR/%{name}/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{name}
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{name}/META
directory="+%{name}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner
%dir %{_libdir}/ocaml/%{name}
%{_libdir}/ocaml/%{name}/*.cmxs
%{_libdir}/ocaml/site-lib/%{name}

%files devel
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/ocaml/%{name}/*.cm[axi]
%{_libdir}/ocaml/%{name}/*.mli
%{_libdir}/ocaml/%{name}/*.h
%if %{with opt}
%{_libdir}/ocaml/%{name}/*.[ao]
%{_libdir}/ocaml/%{name}/*.cmxa
%endif
