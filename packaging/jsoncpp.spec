%global jsondir json

Name:       jsoncpp
Version:    1.6.5
Release:        0
Summary:    JSON library implemented in C++
Group:      System Environment/Libraries
License:    Public Domain or MIT
URL:        https://github.com/open-source-parsers/jsoncpp
Source0:    https://github.com/open-source-parsers/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        baselibs.conf
Source1001:     jsoncpp.manifest

BuildRequires:  doxygen cmake
BuildRequires:  python
#BuildRequires:  graphviz

%description
%{name} is an implementation of a JSON (http://json.org) reader and writer in
C++. JSON (JavaScript Object Notation) is a lightweight data-interchange format.
It is easy for humans to read and write. It is easy for machines to parse and
generate.


%package devel
Summary:    Development headers and library for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development headers and library for %{name}.


%package doc
Summary:    Documentation for %{name}
Group:      Documentation
BuildArch:  noarch

%description doc
This package contains the documentation for %{name}


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .



%build
%cmake -DBUILD_STATIC_LIBS=OFF .
make %{?_smp_mflags}
# Build the doc
python doxybuild.py --doxygen %{_bindir}/doxygen

#%check
# Tests are run automatically in the build section
# ctest -V %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}/html
for f in AUTHORS LICENSE NEWS.txt README.md ; do
    install -p -m 0644 $f $RPM_BUILD_ROOT%{_docdir}/%{name}
done
install -p -m 0644 dist/doxygen/*/*.{html,png} $RPM_BUILD_ROOT%{_docdir}/%{name}/html

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_docdir}/%{name}/
%exclude %{_docdir}/%{name}/html
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_includedir}/%{jsondir}/
%{_libdir}/pkgconfig/jsoncpp.pc

%files doc
%{_docdir}/%{name}/

