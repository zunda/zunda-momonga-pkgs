%global momorel 1

Summary:      platform independent library for scheme
Name:         slib
Version:      3b3
Release:      %{momorel}m%{?dist}
Group:        Development/Languages
BuildArch:    noarch
Packager:     Aubrey Jaffer <agj@alum.mit.edu>

License:      distributable, see individual files for copyright
Vendor:       Aubrey Jaffer <agj @ alum.mit.edu>
Provides:     slib

Requires:     guile

Source0:      http://groups.csail.mit.edu/mac/ftpdir/scm/slib-%{version}.zip
NoSource:     0
URL:          http://people.csail.mit.edu/jaffer/SLIB.html
BuildRoot:    %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

%description
"SLIB" is a portable library for the programming language Scheme.
It provides a platform independent framework for using "packages" of
Scheme procedures and syntax.  As distributed, SLIB contains useful
packages for all Scheme implementations.  Its catalog can be
transparently extended to accomodate packages specific to a site,
implementation, user, or directory.

%prep
%setup -n slib -c -T
cd ..
unzip ${RPM_SOURCE_DIR}/slib-%{version}.zip

%build

%install
rm -rf %{buildroot}
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/slib
cp *.scm *.init *.xyz *.txt ${RPM_BUILD_ROOT}%{_datadir}/slib

# Guile specific
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/guile/site
ln -s %{_datadir}/slib ${RPM_BUILD_ROOT}%{_datadir}/guile/site/slib

%clean
rm -rf %{buildroot}

%post
# Guile specific
guile <<_END > /dev/null
(use-modules (ice-9 slib))
(load "%{_datadir}/slib/mklibcat.scm")
(quit)
_END

%preun
# Guile specific
rm -f %{_datadir}/guile/*/slibcat

%files
%defattr(-, root, root)
%dir %{_datadir}/slib
%{_datadir}/slib/*.scm
%{_datadir}/slib/*.init
%{_datadir}/slib/cie1931.xyz
%{_datadir}/slib/cie1964.xyz
%{_datadir}/slib/nbs-iscc.txt
%{_datadir}/slib/saturate.txt
%{_datadir}/slib/resenecolours.txt
%doc ANNOUNCE README COPYING FAQ ChangeLog
%dir %{_datadir}/guile/site
%{_datadir}/guile/site/slib

%changelog
* Mon Apr  4 2011 zunda <zunda at freeshell.org>
- Modified to build on Momonga 7

* Sun Sep 25 2005 Aubrey Jaffer <agj@alum.mit.edu>
- Updated from RedHat version from Jindrich Novy.

* Fri Jun 22 2005 Aubrey Jaffer  <agj@alum.mit.edu>
- slib.spec (install): Make slib executable.

* Sat Jun 18 2004 Aubrey Jaffer <agj@alum.mit.edu>
- Fixed for RPMbuild version 4.3.1
- Make slib executable.

* Thu Nov 03 2002 Aubrey Jaffer  <agj@alum.mit.edu>
- slib.spec (%post): Improved catalog-building scripts.
- Make clrnamdb.scm.

* Wed Mar 14 2001 Radey Shouman <shouman@ne.mediaone.net>
- Adapted from the spec file of R. J. Meier.

* Mon Jul 12 2000 Dr. Robert J. Meier <robert.meier@computer.org> 0.9.4-1suse
- Packaged for SuSE 6.3

* Sun May 30 2000 Aubrey Jaffer <agj @ alum.mit.edu>
- Updated content
