Summary:	MT-METIS - OpenMP version of METIS' partitioning routines
Summary(pl.UTF-8):	MT-METIS - wykorzystujaca OpenMP wersja procedur dzielących biblioteki METIS
Name:		mt-metis
Version:	0.3
Release:	1
License:	Apache v2.0 (base METIS library), MIT (other components)
Group:		Libraries
#Source0Download: http://glaros.dtc.umn.edu/gkhome/metis/metis/download
Source0:	http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/%{name}-%{version}.tar.gz
# Source0-md5:	b430f097a53435d2ca4cf4587eb45159
Patch0:		%{name}-cmake.patch
Patch1:		%{name}-types.patch
URL:		http://glaros.dtc.umn.edu/gkhome/views/metis
BuildRequires:	cmake >= 2.6
BuildRequires:	gcc >= 6:4.2
BuildRequires:	libgomp-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MT-METIS is an OpenMP version of METIS' partitioning routines.

%description -l pl.UTF-8
MT-METIS to wykorzystująca OpenMP wersja procedur dzielących METIS.

%package devel
Summary:	Header file for MT-METIS library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki MT-METIS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for MT-METIS library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki MT-METIS.

%package static
Summary:	Static MT-METIS library
Summary(pl.UTF-8):	Statyczna biblioteka MT-METIS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MT-METIS library.

%description static -l pl.UTF-8
Statyczna biblioteka MT-METIS.

%prep
%setup -q -n %{name}-0.3.0
%patch -P0 -p1
%patch -P1 -p1

%build
mkdir -p build-shared build-static
cd build-static
%cmake .. \
	-DBOWSTRING_PATH="bowstring" \
	-DDOMLIB_PATH="domlib" \
	-DMETIS_PATH="metis"
%{__make}
cd ../build-shared
%cmake .. \
	-DBOWSTRING_PATH="bowstring" \
	-DDOMLIB_PATH="domlib" \
	-DMETIS_PATH="metis" \
	-DSHARED=ON
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C build-shared install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.txt
%attr(755,root,root) %{_bindir}/mtmetis
%attr(755,root,root) %{_libdir}/libmtmetis.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/mtmetis.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libmtmetis.a
