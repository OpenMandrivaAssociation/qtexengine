%define major 1
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Name: qtexengine
Version: 0.2
Release: 2
Summary: Library enabling Qt based applications to easily export graphics to TeX
License: GPLv3
Group: System/Libraries
URL: http://soft.proindependent.com/qtexengine/
Source0: http://download.berlios.de/qtiplot/QTeXEngine-%{version}-opensource.zip
# Fixes the build and install of QTeXEngine
Patch0: QTeXEngine-svn1552-path.patch
# Fixes between 0.2 and svn1552 checkout
Patch1: QTeXEngine-svn1552.patch
BuildRequires: qt4-devel doxygen

%description
QTeXEngine is a library enabling Qt based applications to easily export
graphics created using the QPainter class to TeX. It is built on top of
QPaintEngine and uses the TikZ/Pgf graphic systems for TeX.

%package -n %libname
Summary: Libraries for %{name}
Group: System/Libraries

%description -n %libname
This package contains library files of %{name}.

%package -n %develname
Summary: Development files for %{name}
Group: Development/KDE and Qt
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %develname
This package contains library, header file and documentation
for developing applications that use %{name}.

%prep
%setup -q -n QTeXEngine
%patch0 -p1
%patch1 -p1

rm -rf {example,test}/.svn

# Remove exec permission
find -type f -exec chmod 0644 {} ";"

%build
export PATH=%{_qt4_bindir}:$PATH
pushd src
%{qmake_qt4} CONFIG+=" QTeXEngineDll" LIBDIR=%{_libdir}
popd
%make -C src

pushd doc
doxygen Doxyfile
# Fix the time stamp
for file in html/*; do
 touch -r Doxyfile $file
done
popd

%install
rm -fr %buildroot
make install INSTALL="install -p" INSTALL_ROOT=%{buildroot} -C src

%clean
rm -rf %{buildroot}

%files -n %libname
%defattr(-,root,root,-)
%doc *.txt
%{_libdir}/libQTeXEngine.so.%{major}*

%files -n %develname
%defattr(-,root,root,-)
%doc doc/html example
%{_includedir}/QTeXEngine.h
%{_libdir}/libQTeXEngine.so


%changelog
* Fri Oct 15 2010 Funda Wang <fwang@mandriva.org> 0.2-1mdv2011.0
+ Revision: 585745
- import qtexengine

