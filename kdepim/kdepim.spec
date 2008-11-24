%global momorel 1
%global artsver 1.5.8
%global artsrel 1m
%global qtver 3.3.7
%global kdever 3.5.8
%global kdelibsrel 1m
%global kdebaserel 1m
%global qtdir %{_libdir}/qt3
%global kdedir /usr
%global ftpdirver %{kdever}
%global sourcedir stable/%{ftpdirver}/src
%ifarch ppc64
%global enable_final 0
%else
%global enable_final 1
%endif
%global enable_gcc_check_and_hidden_visibility 0
%global md5sum_src0 a1ffff553f1d6739c7791891028b176b

Name: kdepim
Summary: Personal Information Management (PIM) for KDE
Version: %{kdever}
Release: %{momorel}m%{?dist}
Group: Applications/Productivity
License: GPL
URL: http://pim.kde.org/
%NoSource 0 ftp://ftp.kde.org/pub/kde/%{sourcedir}/%{name}-%{version}.tar.bz2 %{md5sum_src0}
Source1: cr48-app-kandy.png
Source2: cr32-app-kandy.png
Source3: cr16-app-kandy.png
Patch0: kdepim-3.4.0-kandy-icons.patch

# upstream patches
# no patch to be applied

BuildRoot: %{_tmppath}/%{name}-%{version}-root
Obsoletes: korganizer1x, kpilot
Requires: kdebase3 >= %{kdever}-%{kdebaserel}
Requires: gnupg2
BuildPreReq: qt-devel >= %{qtver}
BuildPreReq: arts-devel >= %{artsver}-%{artsrel}
BuildPreReq: kdelibs-devel >= %{kdever}-%{kdelibsrel}
BuildPreReq: kdebase3 >= %{kdever}-%{kdebaserel}
BuildPreReq: autoconf >= 2.56-3m 
BuildPreReq: bison
BuildPreREq: cyrus-sasl-devel
BuildPreReq: flex
BuildPreReq: gnokii-devel
BuildPrereq: gnupg
BuildPrereq: gnupg2
BuildPreReq: gpgme-devel >= 1.1.2-2m
BuildPreReq: libXScrnSaver-devel
BuildPreReq: libXpm-devel
BuildPreReq: libart_lgpl-devel
BuildPreReq: libmal-devel >= 0.44-2m
BuildPreReq: libopensync-devel
BuildPreReq: libpng-devel >= 1.2.5
BuildPreReq: perl 
BuildPreReq: pilot-link-devel >= 0.12.1-2m
BuildPreReq: python-devel

%description
kdepim is a collection of Personal Information Management (PIM) tools for
the K Desktop Enviromnent (KDE).
kdepim contains the following applications:

  kaddressbook: The KDE addressbook application.
  kandy: sync phone book entries between your cell phone and computer
  kmail: the KDE mail client
  kmailcvt: tool for importing mail related data from other programs
  knode: news client
  korganizer: a calendar-of-events and todo-list manager
  kpilot: synchronizing data with a Palm(tm) or compatible PDA
  kalarm: gui for setting up personal alarm messages, emails and commands
  kalarmd: alarm monitoring daemon, shared by korganizer and kalarm
  karm: Time tracker.
  knotes: Post-It notes on the desktop

and  

  kontact: a unified interface that draws KDE's email, calendaring, address book, notes and other PIM features together into a familiar configuration.


%prep
%setup -q

%patch0 -p1 -b .kandy-icons

# upstream patches
# no patch to be applied

# icons
cp -f %{SOURCE1} %{SOURCE2} %{SOURCE3} kandy/src

make -f admin/Makefile.common cvs

%build
%ifarch ppc64
%global optflags %(echo %{optflags} -mminimal-toc)
%endif

export QTDIR=%{qtdir} KDEDIR=%{kdedir} QTLIB=%{qtdir}/lib

export CFLAGS="%{optflags} -D_GNU_SOURCE -DNDEBUG -UDEBUG -I%{_includedir}/libmal" \
export CXXFLAGS="%{optflags} -DNDEBUG -UDEBUG -DQT_THREAD_SUPPORT -I%{_includedir}/libmal"

./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir} \
	--with-qt-libraries=%{qtdir}/lib \
	--with-xinerama \
	--with-mal \
	--with-gpg=%{_bindir}/gpg \
	--with-gpgsm=%{_bindir}/gpgsm \
	--with-sasl \
	--disable-debug \
%if %{enable_final}
	--enable-final \
%endif
	--enable-new-ldflags \
%if %{enable_gcc_check_and_hidden_visibility}
	--enable-gcc-hidden-visibility \
%endif
	--disable-warnings \
	--disable-rpath

make %{?_smp_mflags} MAL_LIB=-lmal

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# Make symlinks relative
(
  mkdir -p %{buildroot}%{_docdir}/HTML/en/common
  cd %{buildroot}%{_docdir}/HTML/en
  for i in *; do
    [ -d $i -a -L $i/common ] && cd $i && ln -nfs ../common . && cd ..
  done
)

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc MAINTAINERS README*
%{_bindir}/*
%{_libdir}/kconf_update_bin/korn-3-4-config_change
%{_libdir}/kde3/plugins/designer/*.la
%{_libdir}/kde3/plugins/designer/*.so
%{_libdir}/kde3/*.la
%{_libdir}/kde3/*.so
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.??*
%{_datadir}/applications/kde/*.desktop
%{_datadir}/applnk/.hidden/*.desktop
%{_datadir}/applnk/Applications
%{_datadir}/applnk/Utilities/*.desktop
%{_datadir}/apps/akregator
%{_datadir}/apps/kaddressbook
%{_datadir}/apps/kalarm
%{_datadir}/apps/kandy
%{_datadir}/apps/karm
%{_datadir}/apps/karmpart
%{_datadir}/apps/kconf_update/*
%{_datadir}/apps/kdepim
%{_datadir}/apps/kdepimwidgets
%{_datadir}/apps/kgantt
%{_datadir}/apps/kitchensync
%{_datadir}/apps/kleopatra
%{_datadir}/apps/kmail
%{_datadir}/apps/kmailcvt
%{_datadir}/apps/knode
%{_datadir}/apps/knotes
%{_datadir}/apps/kontact
%{_datadir}/apps/kontactsummary
%{_datadir}/apps/korgac
%{_datadir}/apps/korganizer
%{_datadir}/apps/kpilot
%{_datadir}/apps/ktnef
%{_datadir}/apps/kwatchgnupg
%{_datadir}/apps/libical
%{_datadir}/apps/libkdepim
%{_datadir}/apps/libkholidays
%{_datadir}/apps/libkleopatra
%{_datadir}/autostart/*.desktop
%{_datadir}/config/*rc
%{_datadir}/config.kcfg/*.kcfg
%{_datadir}/doc/HTML/en/akregator
%{_datadir}/doc/HTML/en/kaddressbook
%{_datadir}/doc/HTML/en/kalarm
%{_datadir}/doc/HTML/en/kandy
%{_datadir}/doc/HTML/en/karm
%{_datadir}/doc/HTML/en/kleopatra
%{_datadir}/doc/HTML/en/kmail
%{_datadir}/doc/HTML/en/knode
%{_datadir}/doc/HTML/en/knotes
%{_datadir}/doc/HTML/en/konsolekalendar
%{_datadir}/doc/HTML/en/kontact
%{_datadir}/doc/HTML/en/korganizer
%{_datadir}/doc/HTML/en/korn
%{_datadir}/doc/HTML/en/kpilot
%{_datadir}/doc/HTML/en/ktnef
%{_datadir}/doc/HTML/en/kwatchgnupg
%{_datadir}/icons/*/*/*/*.png
%{_datadir}/icons/*/*/*/*.svgz
%{_datadir}/mimelnk/application/*.desktop
%{_datadir}/services/kaddressbook
%{_datadir}/services/kded/networkstatus.desktop
%{_datadir}/services/kontact
%{_datadir}/services/korganizer
%{_datadir}/services/kresources/kabc/*.desktop
%{_datadir}/services/kresources/kcal
%{_datadir}/services/kresources/knotes
%{_datadir}/services/kresources/*.desktop
%{_datadir}/services/*.desktop
%{_datadir}/services/*.protocol
%{_datadir}/servicetypes/*.desktop

%{_includedir}/akregator
%{_includedir}/calendar
%{_includedir}/gpgme++
%{_includedir}/index
%{_includedir}/kabc/*.h
%{_includedir}/kaddressbook
%{_includedir}/kdepim
%{_includedir}/kgantt
%{_includedir}/kleo
%{_includedir}/kmail
%{_includedir}/kontact
%{_includedir}/korganizer
%{_includedir}/kpilot
%{_includedir}/ksieve
%{_includedir}/ktnef
%{_includedir}/libemailfunctions
%{_includedir}/libkcal
%{_includedir}/mimelib
%{_includedir}/qgpgme
%{_includedir}/*.h
%{_libdir}/*.so.?

%changelog
* Mon Nov 24 2008 zunda <zunda at freeshell.org>
- Copied from http://svn.momonga-linux.org/svn/pkgs/branches/STABLE_4/pkgs/kdepim/ r.29112

* Wed Oct 17 2007 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.8-1m)
- update to KDE 3.5.8

* Thu Jul 12 2007 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.7-3m)
- add Requires: gnupg2

* Sun May 27 2007 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.7-2m)
- enable new kitchensync

* Sat May 26 2007 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.7-1m)
- update to KDE 3.5.7
- delete patch1
- adjust %%files section

* Mon Feb 12 2007 Nishio Futoshi <futoshi@momonga-linux.org>
- (3.5.6-3m)
- rebuild against kdeligs etc.

* Sun Feb  4 2007 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.6-2m)
- rebuild against pilot-link-0.12.1 for support kpilot

* Mon Jan 29 2007 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.6-1m)
- update to KDE 3.5.6
- delete unused upstream patches

* Sat Jan 13 2007 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.5-11m)
- import upstream patch to fix following problem 
  #139941, Fix invalid MapQuest URL

* Sat Jan 13 2007 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.5-10m)
- import upstream patch to fix following problem
  #139370, postpone alarm: incorrent items for date chooser

* Fri Jan 12 2007 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.5-9m)
- import upstream patch to fix following problem
  #123350, Kontact crashes if you click "OK" before completing "Resourse Selection"

* Thu Jan 11 2007 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.5-8m)
- import upstream patch to fix following problem
  #113100, Incorrect mime headers in attachment of files with russian names

* Sun Dec 24 2006 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.5-7m)
- import upstream patch to fix following problem
  #131597, reoccuring todos not written to journal when completed

* Thu Dec 21 2006 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.5-6m)
- import upstream patch to fix following problem
  #136954, Reminders from outlook invites are set to unknown in exchange resources

* Wed Dec 20 2006 Yohsuke Ooi <meke@momonga-linux.org>
- (3.5.5-5m)
- suppport PPC64 architecture
-- unuse --enable-final
-- add optflags : -mminimal-toc

* Sat Dec 16 2006 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.5-4m)
- import upstream patch to fix following problem
  #101696, korganizer crash at startup for a particular std.ics file

* Tue Nov 14 2006 TABUCHI Takaaki <tab@momonga-linux.org>
- (3.5.5-3m)
- rebuild against gnupg2-2.0.0-1m

* Mon Nov 13 2006 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.5-2m)
- rebuild against gnokii-0.6.14-1m
- add BuildPreReq: gnokii-devel
- import upstream patch to fix following problem
  #134423, rename of distribution list fails, list becomes unusable

* Fri Oct 27 2006 NARITA Koichi <pulsar@momonga-linux.org>
- (3.5.5-1m)
- update to KDE 3.5.5
- remove merged upstream patches

* Wed Sep 13 2006 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.4-4m)
- import 4 upstream patches from Fedora Core devel
 +* Mon Sep 04 2006 Than Ngo <than@redhat.com> 6:3.5.4-3
 +- apply upstream patches
 +   fix kde#116607, crash in slotCheckQueuedFolders() on application exit
 +* Tue Aug 15 2006 Than Ngo <than@redhat.com> 6:3.5.4-2
 +- apply patch to fix crash when right clicking in an encapsulated email message, kde#131067
 +* Thu Aug 10 2006 Than Ngo <than@redhat.com> 6:3.5.4-1
 +- apply upstream patches,
 +   - Kmail crashes on startup, kde#132008
 +   - Cannot send to addresses containing an ampersand (&), kde#117882

* Sat Sep  9 2006 Nishio Futoshi <futoshi@momonga-linux.org>
- (3.5.4-3m)
- rebuild against arts-1.5.4-2m kdelibs-3.5.4-3m kdebase-3.5.4-11m

* Fri Aug 18 2006 Nishio Futoshi <futoshi@momonga-linix.org>
- (3.5.4-2m)
- rebuild against kdelibs-3.5.4-2m
- rebuild against kdebase-3.5.4-6m

* Wed Aug  2 2006 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.4-1m)
- update to KDE 3.5.4
- remove merged upstream patches

* Wed Jul 12 2006 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.3-3m)
- import 1 upstream patch from Fedora Core devel
 +* Thu Jul 06 2006 Than Ngo <than@redhat.com> 6:3.5.3-4
 +- apply upstream patches,
 +   fix bugs: 110487, 118112, 119112, 121384, 127210, 130303
- modify options of cofigure for crypto/certificate manager support

* Sat Jul  1 2006 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.3-2m)
- import 4 upstream patches from Fedora Core devel
 +* Tue Jun 27 2006 Than Ngo <than@redhat.com> 6:3.5.3-3
 +- apply upstream patches

* Wed May 31 2006 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.3-1m)
- update to KDE 3.5.3

* Wed Mar 29 2006 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.2-1m)
- update to KDE 3.5.2

* Wed Feb  1 2006 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.1-1m)
- update to KDE 3.5.1

* Sat Jan 28 2006 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.0-2m)
- add --enable-new-ldflags to configure
- disable_gcc_check_and_hidden_visibility 1

* Wed Nov 30 2005 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.0-1m)
- update to KDE 3.5

* Mon Nov 28 2005 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.0-0.1.2m)
- revise %%files section
- disable hidden visibility

* Sat Nov 12 2005 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.5.0-0.1.1m)
- update to KDE 3.5 RC1
- remove kandy-lockdev.patch

* Thu Oct 13 2005 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.4.3-1m)
- update to KDE 3.4.3
- remove kdepim-3.4.2-uic.patch
- remove kdepim-3.4.2-kmail-partNode-109003.patch
- remove kdepim-3.4.2-kpilot.patch

* Fri Sep 23 2005 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.4.2-3m)
- import kdepim-3.4.2-uic.patch from Fedora Core devel
 +* Wed Sep 21 2005 Than Ngo <than@redhat.com> 6:3.4.2-4
 +- fix uic build problem

* Wed Sep 14 2005 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.4.2-2m)
- add --disable-rpath to configure
- import two patches from Fedore Core devel
 - kdepim-3.4.2-kpilot.patch
  +* Mon Aug 15 2005 Than Ngo <than@redhat.com> 6:3.4.2-2
  +- apply patch to fix kpilot crash
 - kdepim-3.4.2-kmail-partNode-109003.patch
  +* Tue Aug 02 2005 Than Ngo <than@redhat.com> 6:3.4.2-1
  +- apply patch to fix kmail bug, kde#109003
- BuildPreReq: bison, flex

* Thu Jul 28 2005 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.4.2-1m)
- update to KDE 3.4.2
- remove nokdelibsuff.patch

* Tue Jun 28 2005 Yohsuke Ooi <meke@momonga-linux.org>
- (3.4.1-2m)
- fixed build error gcc4. import FC patch.
-   kdepim-3.4.0-gcc4.patch
-   admin-visibility.patch

* Wed Jun  1 2005 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.4.1-1m)
- update to KDE 3.4.1

* Fri Apr 15 2005 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.4.0-3m)
- modify %%files section
- BuildPreReq: gnupg, gnupg2, gpgme-devel

* Tue Mar 29 2005 Toru Hoshina <t@momonga-linux.org>
- (3.4.0-2m)
- kdelibsuff doesn't need to be applied with {_libdir}/qt3/lib.

* Mon Mar 28 2005 Ichiro Nakai <ichiro@n.email.ne.jp>
- (3.4.0-1m)
- update to KDE 3.4.0
- import kdepim-3.4.0-kandy-lockdev.patch from Fedora Core
- import kandy icons and kandy-icons.patch from Fedora Core
 +* Wed Mar 23 2005 Than Ngo <than@redhat.com> 6:3.4.0-4
 +- add lockdev support patch in kandy from Peter Rockai #84143
 +- add missing kandy icons #141165
- BuildPreReq: kdebase, libart_lgpl-devel

* Wed Mar  9 2005 Toru Hoshina <t@momonga-linux.org>
- (3.3.2-3m)
- rebuild against libtermcap-2.0.8-38m.

* Wed Feb  2 2005 Dai OKUYAMA <dai@ouchi.nahi.to>
- (3.3.2-2m)
- enable x86_64.

* Mon Dec 13 2004 Masayuki SANO <nosanosa@momonga-linux.org>
- (3.3.2-1m)
- update to KDE 3.3.2
 
* Mon Oct 18 2004 Masayuki SANO <nosanosa@momonga-linux.org>
- (3.3.1-1m)
- update to KDE 3.3.1
 
* Mon Sep 27 2004 Hiroyuki Koga <kuma@momonga-linux.org>
- (3.3.0-2m)
- rebuild against kdelibs-3.3.0-3m (libstdc++-3.4.1)

* Fri Sep 24 2004 Masayuki SANO <nosanosa@momonga-linux.org>
- (3.3.0-1m)
- KDE 3.3.0

* Thu Jun 17 2004 Masayuki SANO <nosanosa@momonga-linux.org>
- (3.2.3-1m)
- KDE 3.2.3
- Bugfix Release
 
* Sat Apr 24 2004 Masayuki SANO <nosanosa@momonga-linux.org>
- (3.2.3-1m)
- KDE 3.2.3

* Sat Mar 13 2004 Masayuki SANO <nosanosa@momonga-linux.org>
- (3.2.1-1m)
- KDE 3.2.1 Release

* Sat Feb 14 2004 Masayuki SANO <nosanosa@momonga-linux.org>
- (3.2.0-1m)
- KDE 3.2.0
- HOT FIX for kmail (http://dot.kde.org/1075969434/)
- modified %%files

* Thu Jan 15 2004 YAMAZAKI Makoto <zaki@zakky.org>
- (3.1.5-1m)
- update to 3.1.5

* Wed Dec 31 2003 kourin <kourin@fh.freeserve.ne.jp>
- (3.1.4-3m)
- rebuild against for qt-3.2.3

* Sat Nov 8 2003 kourin <kourin@fh.freeserve.ne.jp>
- (3.1.4-2m)
- rebuild against for qt-3.2.3

* Thu Sep 25 2003 kourin <kourin@fh.freeserve.ne.jp>
- (3.1.4-1m)
- update to 3.1.4

* Thu Aug 14 2003 YAMAZAKI Makoto <uomaster@nifty.com>
- (3.1.3-1m)
- update to 3.1.3

* Tue Jul  8 2003 YAMAZAKI Makoto <uomaster@nifty.com>
- (3.1.2-3m)
- add -fno-stack-protector if gcc is 3.3

* Sun Jun 15 2003 YAMAZAKI Makoto <uomaster@nifty.com>
- (3.1.2-2m)
- remove --disable-warnings from configure

* Mon May 26 2003 YAMAZAKI Makoto <uomaster@nifty.com>
- (3.1.2-1m)
- update to 3.1.2
   changes are:
     korganizer: Exchange plugin supports secure WebDAV.
     korganizer: Fix timezone handling when timezone names are Unicode strings.
- remove kdepim-3.1.1-korganizer-pref-timezone-fix.patch
- add kdepim-3.1.2-miscfix.patch
- add BuildPreReq: libmal-devel and add -I%{_includedir}/libmal to CXXFLAGS
- revive kalarm

* Thu Apr 10 2003 Shingo Akagaki <dora@kitty.dnsalias.org>
- (3.1.1-4m)
- remove requires: qt-Xt
                                                                                
* Thu Apr  3 2003 YAMAZAKI Makoto <uomaster@nifty.com>
- (3.1.1-3m)
- correct timezone string in pref dialog(kdepim-3.1.1-korganizer-pref-timezone-fix.patch)
   See: [Kdeveloper:02753]

* Sun Mar 23 2003 Shingo Akagaki <dora@kitty.dnsalias.org>
- (3.1.1-2m)
- rebuild against for XFree86-4.3.0

* Fri Mar 21 2003 YAMAZAKI Makoto <uomaster@nifty.com>
- (3.1.1-1m)
- update to 3.1.1
    KOrganizer bug fixes: 
      Use correct default duration for events crossing a day boundary (#53477).
      Correctly save category colors (#54913).
      Don't show todos more than once in what's next view.
      Include todos in print output of month view (#53291).
      Don't restrict maximum size of search dialog (#54912).
      Make cancel button of template selection dialog work (#54852).
      Don't break sorting when changing todos by context menu (#53680).
      Update views on changes of todos directly in the todo list (#43162).
      Save state of statusbar (#55380).
    knotes: Escape "&" in note titles
 
* Wed Mar 12 2003 TABUCHI Takaaki <tab@momonga-linux.org>
- (3.1-2m)
- add URL

* Sun Feb  2 2003 Shigeru Yamazaki <muradaikan@momonga-linux.org>
- (3.1-1m)
- version up.

* Sun Jan 12 2003 Tadataka Yoshikawa <yosshy@momonga-linux.org>
- (3.0.5a-1m)
- ver up.
- remove subpackage "kalarm" because it make failed.

* Wed Dec 11 2002 YAMAZAKI Makoto <uomaster@nifty.com>
- (3.0.4-3m)
- use autoconf-2.53

* Sat Oct 12 2002 Kazuhiko <kazuhiko@fdiary.net>
- (3.0.4-2m)
- revise %files (remove kpilot related directories)

* Fri Oct 11 2002 Tadataka Yoshikawa <yosshy@momonga-linux.org>
- (3.0.4-1m)
- ver up.

* Mon Aug 19 2002 Tadataka Yoshikawa <yosshy@momonga-linux.org>
- (3.0.3-1m)
- ver up.
- remove Patch1.

* Wed Jul 24 2002 Tadataka Yoshikawa <yosshy@momonga-linux.org>
- (3.0.2-3m)
- 3.0.2-2m is spec file fix miss. sorry.

* Wed Jul 24 2002 Tadataka Yoshikawa <yosshy@momonga-linux.org>
- (3.0.2-2m)
- add qt-3.0.5 build patch.

* Wed Jul 17 2002 Tadataka Yoshikawa <yosshy@momonga-linux.org>
- (3.0.2-2m)
- rebuild against qt-3.0.5.

* Sun Jul 14 2002 Tadataka Yoshikawa <yosshy@momonga-linux.org>
- (3.0.2-1m)
- ver up.

* Sun Jun  9 2002 Tadataka Yoshikawa <yosshy@kondara.org>
- (3.0.1-2k)
- ver up.

* Fri Apr  5 2002 Tsutomu Yasuda <tom@kondara.org>
- (3.0.0-2k)
  update to 3.0 release.

* Thu Mar 21 2002 Toru Hoshina <t@kondara.org>
- (3.0.0-0.0003002k)
- based on 3.0rc3.

* Tue Nov 27 2001 Toru Hoshina <t@kondara.org>
- (2.2.2-2k)
- version up.

* Thu Nov  8 2001 Toru Hoshina <t@kondara.org>
- (2.2.1-10k)
- nigirisugi.
- revised spec file.

* Tue Oct 30 2001 MATSUDA, Daiki <dyky@df-usa.com>
- (2.2.1-8k)
- add pilot-link-devel to BuildPreReq tag
- revised spec file.

* Tue Oct 16 2001 Toru Hoshina <t@kondara.org>
- (2.2.1-4k)
- rebuild against libpng 1.2.0.

* Thu Oct  4 2001 Toru Hoshina <t@kondara.org>
- (2.2.1-2k)
- version up.

* Wed Aug 22 2001 Toru Hoshina <toru@df-usa.com>
- (2.2.0-2k)
- stable release.

* Sat Aug 11 2001 Toru Hoshina <toru@df-usa.com>
- (2.2.0-0.0003002k)
- based on 2.2beta1.

* Fri Jun  1 2001 Toru Hoshina <toru@df-usa.com>
- (2.2.0-0.0002002k)
- based on 2.2alpha2.

* Sat May 12 2001 Toru Hoshina <toru@df-usa.com>
- (2.2.0-0.0001002k)

* Fri Mar 30 2001 Tsutomu Yasuda <tom@digitalfactory.co.jp>
- (2.1.1-3k)

* Thu Mar 22 2001 Toru Hoshina <toru@df-usa.com>
- (2.1-2k)

* Fri Mar 16 2001 MATSUDA, Daiki <dyky@df-usa.com>
- (2.0.1-14k)
- rebuild against QT-2.3.0.

* Sat Jan 13 2001 Kenichi Matsubara <m@kondara.org>
- [2.0.1-12k]
- backport 2.0.1-13k(Jirai).

* Fri Jan 05 2001 Kenichi Matsubara <m@kondara.org>
- [2.0.1-10k]
- backport 2.0.1-11k(Jirai).

* Fri Jan 05 2001 Kenichi Matsubara <m@kondara.org>
- [2.0.1-11k]
- rebuild against.

* Wed Dec 20 2000 Kenichi Matsubara <m@kondara.org>
- [2.0.1-9k]
- update patch.
- (kdepim-2.0.1-korganizer-i18n-20001205.diff).

* Thu Dec 14 2000 Kenichi Matsubara <m@kondara.org>
- [2.0.1-7k]
- rebuild against qt-2.2.3.

* Mon Dec 11 2000 Kenichi Matsubara <m@kondara.org>
- [2.0.1-5k]
- change GIF Support switch tag.
- (Vendor to Option)

* Fri Dec 08 2000 Kenichi Matsubara <m@kondara.org>
- [2.0.1-3k]
- update to 2.0.1.

* Tue Nov 21 2000 Kenichi Matsubara <m@kondara.org>
- [2.0-4k]
- rebuild against new environment glibc-2.2 egcs++

* Fri Nov 17 2000 Toru Hoshina <toru@df-usa.com>
- [2.0-3k]
- rebuild against qt 2.2.2.

* Sat Nov 04 2000 Kenichi Matsubara <m@kondara.org>
- [2.0-1k]
- add kdepim-2.0-korganizer-i18n-20001101.diff
- add GIF Support switch.
- release.

* Fri Oct 20 2000 Kenichi Matsubara <m@kondara.org>
- [2.0rc2-0.2k]
- modified Rrequires,BuildPrereq.
- add %%define qtver.

* Thu Oct 12 2000 Kenichi Matsubara <m@kondara.org>
- [2.0rc2-0.1k]
- update 2.0rc2.

* Tue Oct 10 2000 Kenichi Matsubara <m@kondara.org>
- rebuild against Qt-2.2.1.

* Mon Sep 25 2000 Kenichi Matsubara <m@kondara.org>
- update 1.94.

* Tue Aug 08 2000 Toru Hoshina <t@kondara.org>
- rebuild against gcc-2.96-0.6k.

* Sun Jul 30 2000 Toru Hoshina <t@kondara.org>
- rebuild against glibc 2.1.91, gcc 2.96.

* Sat Jun 24 2000 Kenichi Matsubara <m@kondara.org>
- Initial release for Kondara MNU/Linux.
