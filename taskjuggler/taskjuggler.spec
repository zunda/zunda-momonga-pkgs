%global momorel 2
Summary: Project management software
Name: taskjuggler
Version: 2.4.3
Release: %{momorel}m%{?dist}
Group: Applications/Productivity
License: GPL
URL: http://www.taskjuggler.org

Source0: http://www.taskjuggler.org/download/taskjuggler-%{version}.tar.bz2
NoSource: 0

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: qt-devel docbook-utils tetex
BuildRequires: kdelibs3-devel arts-devel libart_lgpl-devel libidn-devel
BuildRequires: libutempter-devel libacl-devel
Requires: qt
Requires: kdelibs3

%description
TaskJuggler is a project management tool for Linux and UNIX-like
operating systems. Its new approach to project planning and tracking is
far superior to the commonly used Gantt chart editing tools. It has
already been successfully used in many projects and scales easily to
projects with hundreds of resources and thousands of tasks.

TaskJuggler is an Open Source tools for serious project managers. It
covers the complete spectrum of project management tasks from the first
idea to the completion of the project. It assists you during project
scoping, resource assignment, cost and revenue planing, risk and
communication management.

TaskJuggler provides an optimizing scheduler that computes your project
time lines and resource assignments based on the project outline and
the constrains that you have provided. The build-in resource balancer
and consistency checker offload you from having to worry about
irrelevant details and ring the alarm if the project gets out of hand.
Its flexible "as many details as necessary"-approach allows you to
still plan your project as you go, making it also ideal for new
management strategies such as Extreme Programming and Agile Project
Management.

If you are about to build a skyscraper or just want to put together
your colleague's shift plan for the next month, TaskJuggler is the
right tool for you. If you just want to draw nice looking Gantt charts
to impress your boss or your investors, TaskJuggler might not be right
for you. It takes some effort to master its power, but it will become a
companion you don't want to miss anymore.

Authors:
--------
    Chris Schlaeger <cs@kde.org>,
    Klaas Freitag <freitag@suse.de>
    Lukas Tinkl <lukas.tinkl@suse.cz>

%prep
%setup -q

%build
%define __libtoolize :
autoconf
%configure \
  --with-qt-dir=/usr/lib/qt-3.3.7 \
  --with-ical-support=no \
  --with-extra-includes=/usr/include/kde \
  --with-extra-libraries=/usr/lib/kde3
pushd docs; make; popd
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
%make DESTDIR=%{buildroot} transform='s,x,x,' install

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL README TODO taskjuggler.lsm
%{_bindir}/taskjuggler
%{_bindir}/TaskJugglerUI
%{_libdir}/libtaskjuggler*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%doc /usr/share/doc/packages/taskjuggler
%doc /usr/share/doc/HTML/*/taskjuggler/*
%config /usr/share/applications/kde/taskjuggler.desktop
%config /usr/share/apps/katepart/syntax/taskjuggler.xml
%config /usr/share/apps/taskjuggler/
%config /usr/share/config/taskjugglerrc
%config /usr/share/icons/*/*/*/*
%config /usr/share/mimelnk/application/*

%changelog
* Thu Aug 20 2009 - zunda at freeshell.org
- (2.4.3-2m)
- Modified for Momonga 6
  - added empty defnition on __liboolize
  - added options to configure - --with-ical-support=no,
    --with-extra-includes=/usr/include/kde, and
    --with-extra-libraries=/usr/lib/kde3
  - removed dependencies to kdepim and kdelibs
  - added dependency to kdelibs3
  - disabled parallel build in doc
* Wed Aug 19 2009 - zunda at freeshell.org
- (2.4.3-1m)
- Updated
* Fri Feb 20 2009 - zunda at freeshell.org
- (2.4.1-7m)
- Added dependency to kdelibs and kdepim
* Tue Dec  2 2008 - zunda at freeshell.org
- (2.4.1-5m)
- Added dependency to qt instead of qt3 for Momonga 4
* Tue Dec  2 2008 - zunda at freeshell.org
- (2.4.1-4m)
- Updated list of files
* Tue Dec  2 2008 - zunda at freeshell.org
- (2.4.1-3m)
- rpmbuild completes (with some files left unpackaged) on Momonga 4
* Fri Nov 14 2008 - zunda at freeshell.org
- (2.4.1-2m)
- Modified to include documentations
- Documentations including examples are in /usr/share/doc/packages/taskjuggler.
  Is there a more appropirate path?
- docbook-to-man needed to create man pages
* Mon Nov 10 2008 - zunda at freeshell.org
- Update to version 2.4.1
- Modified to build on Momonga 5 without KDE
* Fri Jul 22 2007 - cs@kde.org
- Update to version 2.4.0
* Mon Jan 01 2007 - cs@kde.org
- Update to version 2.3.1
* Tue Aug 08 2006 - dmueller@suse.de
- fix build
* Wed Jun 21 2006 - dmueller@suse.de
- Remove self-provides taskjuggler-kde (#186079)
* Tue Jun 20 2006 - stbinner@suse.de
- fix build for older distributions
* Wed Jun 14 2006 - dmueller@suse.de
- build parallel
* Wed Feb 15 2006 - stbinner@suse.de
- remove "Software" from GenericName in .desktop file
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Dec 05 2005 - stbinner@suse.de
- Update to version 2.2.0
* Wed Nov 23 2005 - stbinner@suse.de
- Update to version 2.2.0_beta2.
* Sun Nov 06 2005 - cs@suse.de
- Update to version 2.2.0_beta1.
- Cleaned up the spec file. The Perl stuff is no longer needed.
* Thu Oct 13 2005 - stbinner@suse.de
- remove extra qualification for gcc 4.1 compilation
* Tue Oct 11 2005 - stbinner@suse.de
- obviously libkcal/calendarlocal.h is considered internal by
  kdepim developers and so they didn't care api stability
* Mon Aug 29 2005 - adrian@suse.de
- do hide old GUI frontend (#113553)
* Sat Aug 27 2005 - cs@suse.de
- Fixed several critical packaging issues [#113553].
* Mon Aug 15 2005 - cs@suse.de
- Fixed crash with late or missing 'project' section [#104627]
- Enabled test suite again.
- There are no more .cvsignore files, so no need to remove them.
* Sun Aug 14 2005 - cs@suse.de
- Fixed crash in GUI. [#104582]
* Mon Aug 08 2005 - freitag@suse.de
- removed wrong tarball and added the correct one, removed patch
  again
* Mon Aug 08 2005 - freitag@suse.de
- update to rev. 2.1.1
* Mon Aug 01 2005 - freitag@suse.de
- update to rev. 2.1.1 release candidate
* Wed May 25 2005 - freitag@suse.de
- fix the failing test for the Scheduler. Note: I have no solution to
  this but simply removed the testcase completely! TODO!
* Sun May 22 2005 - aj@suse.de
- Fix another gcc4 build problem.
* Tue Apr 19 2005 - ro@suse.de
- build with gcc-4
* Tue Mar 22 2005 - freitag@suse.de
- added fix diff to fix a problem with pathnames [#74224]
* Mon Mar 07 2005 - ro@suse.de
- fixed changelog
* Sun Mar 06 2005 - aj@suse.de
- Fix spec file to include directories.
* Sat Mar 05 2005 - ltinkl@suse.cz
- major update to version 2.1
* Thu Feb 17 2005 - adrian@suse.de
- menu entry moved to xdg dir
* Tue Jan 25 2005 - freitag@suse.de
- update to CVS version as of 2005-01-24
  Brings working version of Chris' graphical taskjuggler tool to the
  preview.
* Mon Nov 22 2004 - ltinkl@suse.cz
- update to CVS version as of 2004-11-22
* Thu Sep 30 2004 - joe@suse.de
- fixed specfile to not create a second icon entry in the KDE menu;
  commenting out the %%suse_update_desktop_file entry was not enough
* Wed Sep 29 2004 - joe@suse.de
- updated to latest version from cvs
- now features latest version of ktjview2
- improved KDE integration (icons, mimetypes)
* Mon Sep 13 2004 - adrian@suse.de
- fix menu entry
* Fri Jul 23 2004 - joe@suse.de
- fixed 64bit and KDE directory issues
* Wed Jul 21 2004 - freitag@suse.de
- update to cvs version that contains the new kde viewer
* Sun Apr 25 2004 - adrian@suse.de
- add qt and kde lib dirs to configure
  (auto-lib suffix detection does not work in this special setup)
* Wed Apr 21 2004 - coolo@suse.de
- build without unsermake
* Thu Mar 18 2004 - freitag@suse.de
- added proper mimetype registration for ktjview
* Tue Mar 09 2004 - freitag@suse.de
- update to version 2.0.1 which contains bugfixes, more flexible
  xml reports, vacations in Html reports.
  Fixes for building on FreeBSD
* Thu Mar 04 2004 - freitag@suse.de
- added a patch for tjx2gantt to work again with MethodMaker perl
  module. MethodMaker had a interface change in the new version
  used from 9.1 on. Added a condition on the patch.
* Thu Nov 27 2003 - freitag@suse.de
- update to version 2.0
* Fri Nov 14 2003 - freitag@suse.de
- update to new snapshot 2003-11-13
* Thu Nov 13 2003 - adrian@suse.de
- add Requires to used qt version
* Mon Nov 10 2003 - freitag@suse.de
- update to CVS version Nov. 2003
* Mon Sep 08 2003 - freitag@suse.de
- update to 1.9.2
* Thu Aug 21 2003 - freitag@suse.de
- updated to another pre2 version
* Wed Aug 06 2003 - freitag@suse.de
- reactivated TestSuite again, works now
* Wed Jul 30 2003 - freitag@suse.de
- on the way to 2.0 another step
* Tue Jul 01 2003 - freitag@suse.de
- added some fixes to build on +kde
* Fri Jun 27 2003 - freitag@suse.de
- update to version 1.9.0
* Tue Jun 17 2003 - coolo@suse.de
- fix build
* Wed May 21 2003 - ro@suse.de
- removed .cvsignore files
- remove unpackaged files
* Tue May 06 2003 - freitag@suse.de
- added a patch older_gcc to fix problems on older versions of
  SuSE Linux with older compilers. This patch can be removed again
  in new versions of taskjuggler
* Tue Mar 11 2003 - freitag@suse.de
- update to 1.4.2 that repairs still some encoding issues, html and
  xml report problems. It brings improved syntax error messages in
  macro use, shows milestones and has a new task attribute.
* Tue Feb 25 2003 - freitag@suse.de
- miniatur changes to the manual and added a index.html to the doc
  directory in order to give the link back to susehelp
* Mon Feb 24 2003 - freitag@suse.de
- update to version 1.4.1 - bugfixes in Localisation issues
  (Bugzilla #23309), speed improvements etc.
* Wed Dec 18 2002 - freitag@suse.de
- fixed a bug in installation that broke building on platforms.
* Wed Dec 18 2002 - freitag@suse.de
- update to version 1.4
* Wed Dec 11 2002 - freitag@suse.de
- removed documentation creation and added the docs as tarfile.
  splitted into different packages for taskjuggler,
  taskjuggler-pstools and taskjuggler-kde
  updated to pre 1.4 version
* Mon Nov 11 2002 - ro@suse.de
- changed neededforbuild <sp> to <opensp>
* Fri Jun 28 2002 - uli@suse.de
- fixed for lib64 archs
* Tue Jun 18 2002 - freitag@suse.de
- replaced acinclude due to problems on some platforms.
* Tue Jun 18 2002 - freitag@suse.de
- update to version 1.2:
  * added a simple KDE viewer for xml output
  * improved html output
  * improved xml output
  * bugfixes
* Fri Jun 14 2002 - freitag@suse.de
- update to version 1.1
* Wed May 22 2002 - coolo@suse.de
- fix path to qt3
* Sun Apr 14 2002 - coolo@suse.de
- fix for gcc 3.1
* Fri Mar 15 2002 - freitag@suse.de
- fixed a nasty bug with vacation, update to version 1.01 for that
* Tue Feb 26 2002 - freitag@suse.de
- update to 1.0.0
  Fixed bug with included files when tjp file is not in working dir
* Fri Feb 22 2002 - freitag@suse.de
- update to 0.9.4 to have proper documentation, correct xml export
  and more bug fixes.
* Thu Feb 07 2002 - freitag@suse.de
- update to version 0.9.1 which brings performance improvements and
  fixes some minor bugs.
* Thu Jan 17 2002 - freitag@suse.de
- first version of taskjugger.
