%define desktop_file_utils_version 0.9

Name: rhythmbox
Summary: Music Management Application
Version: 0.12.8
Release: 1%{?dist}
License: GPLv2+ with exceptions and GFDL
Group: Applications/Multimedia
URL: http://projects.gnome.org/rhythmbox/
Source: http://download.gnome.org/sources/rhythmbox/0.12/%{name}-%{version}.tar.bz2
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: gtk2 >= 2.4.0
Requires: gnome-python2 gnome-python2-gconf gnome-python2-gnomevfs
Requires: gnome-themes
Requires: media-player-info
Requires(post): scrollkeeper
Requires(post): desktop-file-utils >= %{desktop_file_utils_version}
Requires(post): GConf2
Requires(preun): GConf2
Requires(postun): scrollkeeper
Requires(postun): desktop-file-utils >= %{desktop_file_utils_version}
Requires: gstreamer-python
Requires: pywebkitgtk python-mako gnome-python2-gconf

BuildRequires: libgpod-devel
BuildRequires: gnome-media-devel
BuildRequires: gnome-keyring-devel
BuildRequires: brasero-devel
BuildRequires: gstreamer-plugins-base-devel >= 0.10
BuildRequires: gettext, scrollkeeper
BuildRequires: totem-pl-parser-devel >= 2.21.1
BuildRequires: gnome-vfs2-devel >= 2.7.4
BuildRequires: avahi-glib-devel >= 0.6
BuildRequires: libmusicbrainz3-devel
BuildRequires: dbus-devel >= 0.90
BuildRequires: dbus-glib-devel >= 0.70
BuildRequires: libnotify-devel
BuildRequires: gstreamer-devel
BuildRequires: gnome-doc-utils
BuildRequires: python-devel
BuildRequires: pygtk2-devel
BuildRequires: libsoup-devel >= 2.3.0
BuildRequires: hal-devel
BuildRequires: libmtp-devel
BuildRequires: gstreamer-python-devel
BuildRequires: libgudev-devel
BuildRequires: kernel-headers
BuildRequires: perl(XML::Parser) intltool
BuildRequires: libSM-devel


ExcludeArch:    s390 s390x

# https://bugzilla.gnome.org/show_bug.cgi?id=596615
Patch0: 0001-podcast-use-g_file_input_stream_query_info-for-downl.patch
# use a omf category that rarian/yelp recognize
Patch1: rhythmbox-doc-category.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=590400
Patch2: rb-update-radios.patch
# Upstream MTP bug fixes
Patch3: 0002-MTP-Fix-memory-leak.patch
Patch4: 0003-generic-player-don-t-crash-saving-empty-playlists-bu.patch
Patch5: 0004-don-t-crash-when-transferring-files-with-no-extensio.patch
Patch6: 0005-rhythmdb-use-g_ascii_strtod-to-read-the-db-version-b.patch
Patch7: 0006-source-protect-against-repeated-deletion-bug-613526.patch
Patch8: 0007-mtp-ignore-devices-that-don-t-support-any-audio-form.patch
Patch9: 0008-mtp-report-out-of-space-errors-on-track-upload.patch
Patch10: 0009-mtp-add-thread-task-for-folder-creation.patch
Patch11: 0010-mtp-add-folder-path-property-on-the-mtp-device-uploa.patch
Patch12: 0011-mtp-delete-empty-folders-after-deleting-tracks-bug-5.patch

%description
Rhythmbox is an integrated music management application based on the powerful
GStreamer media framework. It has a number of features, including an easy to
use music browser, searching and sorting, comprehensive audio format support
through GStreamer, Internet Radio support, playlists and more.

Rhythmbox is extensible through a plugin system.

%package upnp
Summary: UPNP/DLNA plugin for Rhythmbox
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Requires: python-Coherence
Requires: python-louie python-twisted


%description upnp
This package contains a Rhythmbox plugin to add support for playing media 
from, and sending media to UPnP/DLNA network devices.

%prep
%setup -q

%patch0 -p1 -b .http-head
%patch1 -p1 -b .doc-category
%patch2 -p1 -b .radios
%patch3 -p1 -b .mtp-memleak
%patch4 -p1 -b .empty-pl
%patch5 -p1 -b .no-ext
%patch6 -p1 -b .strtod
%patch7 -p1 -b .src-deletion
%patch8 -p1 -b .mtp-no-audio
%patch9 -p1 -b .oospace
%patch10 -p1 -b .mtp-thread
%patch11 -p1 -b .mtp-folder-prop
%patch12 -p1 -b .mtp-empty-folder

# Use the installed louie, not the one in Coherence
find plugins/coherence/upnp_coherence/ -type f -exec sed -i 's/coherence.extern.louie as louie/louie/' '{}' ';'

%build

# work around a gstreamer bug
/usr/bin/gst-inspect-0.10 --print-all >& /dev/null || :

%configure \
      --with-ipod \
      --with-mdns=avahi \
      --disable-scrollkeeper \
      --with-gnome-keyring

# Remove RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=%{buildroot}
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
rm -f %{buildroot}%{_libdir}/bonobo/*.{a,la}
rm -f %{buildroot}%{_libdir}/bonobo/librb-nautilus-context-menu.so
rm -f %{buildroot}%{_libdir}/rhythmbox/plugins/*.{a,la}
rm -f %{buildroot}%{_libdir}/rhythmbox/plugins/*/*.{a,la}
rm -f %{buildroot}%{_libdir}/librhythmbox-core.{a,la}
rm -f %{buildroot}%{_libdir}/mozilla/plugins/*.{a,la}

%find_lang %name --with-gnome

# Don't package api docs
rm -rf %{buildroot}/%{_datadir}/gtk-doc/

# And don't package vala
rm -f %{buildroot}%{_libdir}/rhythmbox/plugins/libsample-vala.so \
	%{buildroot}%{_libdir}/rhythmbox/plugins/sample-vala.rb-plugin

# Don't include header files for plugins
rm -rf %{buildroot}%{_libdir}/rhythmbox/plugins/*/*.h

# save space by linking identical images in translated docs
helpdir=$RPM_BUILD_ROOT%{_datadir}/gnome/help/%{name}
for f in $helpdir/C/figures/*.png; do
  b="$(basename $f)"
  for d in $helpdir/*; do
    if [ -d "$d" -a "$d" != "$helpdir/C" ]; then
      g="$d/figures/$b"
      if [ -f "$g" ]; then
        if cmp -s $f $g; then
          rm "$g"; ln -s "../../C/figures/$b" "$g"
        fi
      fi
    fi
  done
done


%clean
rm -rf %{buildroot}

%post 
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/rhythmbox.schemas >/dev/null
update-desktop-database -q
scrollkeeper-update -q
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/rhythmbox.schemas > /dev/null || :
fi

%postun
/sbin/ldconfig
update-desktop-database -q
scrollkeeper-update -q
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi


%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING README NEWS
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/rhythmbox.schemas
%{_datadir}/rhythmbox/
%{_datadir}/applications/rhythmbox.desktop
%{_datadir}/dbus-1/services/org.gnome.Rhythmbox.service
%{_datadir}/icons/hicolor/*/places/*.*
%{_datadir}/icons/hicolor/*/apps/rhythmbox.*
%{_libdir}/librhythmbox-core.so*
%{_libdir}/mozilla/plugins/*.so
%dir %{_libdir}/rhythmbox
%dir %{_libdir}/rhythmbox/plugins
%{_libdir}/rhythmbox/plugins/artdisplay/
%{_libdir}/rhythmbox/plugins/audiocd/
%{_libdir}/rhythmbox/plugins/audioscrobbler/
%{_libdir}/rhythmbox/plugins/cd-recorder/
%{_libdir}/rhythmbox/plugins/context/
%{_libdir}/rhythmbox/plugins/daap/
%{_libdir}/rhythmbox/plugins/generic-player/
%{_libdir}/rhythmbox/plugins/ipod/
%{_libdir}/rhythmbox/plugins/iradio/
%{_libdir}/rhythmbox/plugins/jamendo/
%{_libdir}/rhythmbox/plugins/lyrics/
%{_libdir}/rhythmbox/plugins/magnatune/
%{_libdir}/rhythmbox/plugins/mmkeys/
%{_libdir}/rhythmbox/plugins/mtpdevice/
%{_libdir}/rhythmbox/plugins/power-manager/
%{_libdir}/rhythmbox/plugins/python-console/
%{_libdir}/rhythmbox/plugins/rb/
%{_libdir}/rhythmbox/plugins/visualizer/
%{_libdir}/rhythmbox/plugins/fmradio/
%{_libdir}/rhythmbox/plugins/im-status/
%{_libdir}/rhythmbox/plugins/status-icon/
%{_libdir}/rhythmbox/plugins/sendto/
%{_libdir}/rhythmbox/plugins/replaygain/
%{_libexecdir}/rhythmbox-metadata
%{_mandir}/man1/*

%files upnp
%defattr(-, root, root)
%{_libdir}/rhythmbox/plugins/upnp_coherence

%changelog
* Fri Jun 25 2010 Bastien Nocera <bnocera@redhat.com> 0.12.8-1
- Update to 0.12.8 + cherry-pick fixes
Resolves: rhbz#558143

* Tue Jun 01 2010 Bastien Nocera <bnocera@redhat.com> 0.12.6-8
- Update initial radio list
Resolves: rhbz#590400

* Fri May 14 2010 Bastien Nocera <bnocera@redhat.com> 0.12.6-7
- Fix package review bugs

* Mon May  3 2010 Matthias Clasen <mclasen@redhat.com> 0.12.6-6
- Make the manual show up in yelp
Resolves: #588506

* Tue Jan 12 2010 Matthias Clasen <mclasen@redhat.com> 0.12.6-5
- Rebuild

* Wed Jan 06 2010 Bastien Nocera <bnocera@redhat.com> 0.12.6-4
- Add patches from F-12
Related: rhbz#543948

* Thu Dec 17 2009 Bastien Nocera <bnocera@redhat.com> 0.12.6-3
- Remove LIRC plugin
Related: rhbz#543948

* Wed Dec 16 2009 Matthias Clasen <mclasen@redhat.com> - 0.12.6-2
- Don't include header files for plugins

* Sun Nov 22 2009 Bastien Nocera <bnocera@redhat.com> 0.12.6-1
- Update to 0.12.6

* Tue Nov 03 2009 Bastien Nocera <bnocera@redhat.com> 0.12.5-8
- Fix brasero project generation

* Mon Oct 19 2009 Bastien Nocera <bnocera@redhat.com> 0.12.5-7
- Use bicubic volumes in the UI
- Avoid using HEAD to get podcast mime-types

* Tue Oct 13 2009 Bastien Nocera <bnocera@redhat.com> 0.12.5-6
- Fix DAAP plugin linkage

* Wed Oct 07 2009 Bastien Nocera <bnocera@redhat.com> 0.12.5-5
- Remove work-around for brasero bug

* Tue Oct  6 2009 Matthias Clasen <mclasen@redhat.com> 0.12.5-4
- Make burning with brasero actually work, somewhat

* Mon Sep 28 2009 Bastien Nocera <bnocera@redhat.com> 0.12.5-3
- Fix the symbols for the browser plugin being mangled (#525826)

* Mon Sep 28 2009 Richard Hughes  <rhughes@redhat.com> - 0.12.5-2
- Apply a patch from upstream to inhibit gnome-session, rather than
  gnome-power-manager. This fixes a warning on rawhide.

* Fri Sep 18 2009 Bastien Nocera <bnocera@redhat.com> 0.12.5-1
- Update to 0.12.5

* Wed Sep 02 2009 Bastien Nocera <bnocera@redhat.com> 0.12.4-3
- Add upstream patch to use the correct path for mpi files

* Tue Sep 01 2009 Bastien Nocera <bnocera@redhat.com> 0.12.4-2
- Remove obsolete configure flags
- Add libgudev BR
- Add media-player-info requires (note, not built yet)

* Tue Sep 01 2009 Bastien Nocera <bnocera@redhat.com> 0.12.4-1
- Update to 0.12.4

* Sat Aug 22 2009 Matthias Clasen <mclasen@redhat.com> - 0.12.3-5
- Respect the button-images setting better

* Wed Aug 19 2009 Matthias Clasen <mclasen@redhat.com> - 0.12.3-4
- Use the right spinner icon

* Wed Aug 19 2009 Bastien Nocera <bnocera@redhat.com> 0.12.3-3
- Fix audio CD activation (#517685)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 09 2009 Bastien Nocera <bnocera@redhat.com> 0.12.3-1
- Udpate to 0.12.3

* Wed Jul 01 2009 Bastien Nocera <bnocera@redhat.com> 0.12.2.93-1
- Update to 0.12.2.93

* Tue Jun 30 2009 Bastien Nocera <bnocera@redhat.com> 0.12.2.92-1
- Update to 0.12.2.92

* Mon Jun 29 2009 Bastien Nocera <bnocera@redhat.com> 0.12.2.91-1
- Update to 0.12.2.91

* Thu Jun 04 2009 Bastien Nocera <bnocera@redhat.com> 0.12.2-1
- Update to 0.12.2

* Thu May 07 2009 Bastien Nocera <bnocera@redhat.com> 0.12.1-3
- Add patch for sound-juicer changes

* Wed Apr 29 2009 - Matthias Clasen <mclasen@redhat.com> - 0.12.1-2
- Update WKNC urls (#498258)

* Tue Apr 28 2009 - Bastien Nocera <bnocera@redhat.com> - 0.12.1-1
- Update to 0.12.1

* Wed Apr 22 2009 - Bastien Nocera <bnocera@redhat.com> - 0.12.0.92-1
- Update to 0.12.0.92

* Tue Apr 14 2009 - Bastien Nocera <bnocera@redhat.com> - 0.12.0-5
- Fix possible crashers in the libmusicbrainz3 code

* Thu Apr 09 2009 - Bastien Nocera <bnocera@redhat.com> - 0.12.0-4
- Fix iPod detection with the DeviceKit-disks gvfs monitor (#493640)

* Wed Mar 25 2009 - Bastien Nocera <bnocera@redhat.com> - 0.12.0-3
- Fix crasher in the PSP and Nokia plugins

* Tue Mar 24 2009 - Bastien Nocera <bnocera@redhat.com> - 0.12.0-2
- Add patch to use decodebin2 instead of decodebin and fix
  playback problems with chained ogg streams (#446283)

* Thu Mar 19 2009 - Bastien Nocera <bnocera@redhat.com> - 0.12.0-1
- Update to 0.12.0

* Wed Mar 18 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.99.3-1
- Update to 0.11.99.3 pre-release

* Tue Mar 17 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.99.2-1
- Update to 0.11.99.2 pre-release

* Fri Mar 13 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.99.1-1
- Update to 0.11.99.1 pre-release

* Thu Mar 12 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.99-1
- Update to 0.11.99 pre-release

* Mon Mar 09 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-30.r6184
- Update to r6184
- Change default burner plugin to brasero

* Wed Mar 04 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-29.r6176
- Update to r6176
- Drop upstreamed patches

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-28.r6096
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Todd Zullinger <tmz@pobox.com> - 0.11.6-27.r6096
- Rebuild against libgpod-0.7.0

* Thu Feb 19 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-26.r6096
- libmusicbrainz is gone

* Tue Feb 17 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-25.r6096
- Add patch to set the PulseAudio properties

* Fri Feb 13 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-24.r6096
- Use the pulsesink's volume instead of our own one
- Fix crasher when musicbrainz3 doesn't get a match for an audio CD (#481441)

* Tue Jan 20 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-23.r6096
- Fix UPNP plugin for use with external Louie (#480036)

* Mon Jan 19 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.11.6-22.r6096
- Backport patch to fix avahi assertion in DAAP plugin.

* Tue Jan 13 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-21.r6096
- Add more Python deps for the UPNP plugin (#474372)
- Require gstreamer-python-devel, as it's been split from gstreamer-python

* Mon Jan 05 2009 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-20.r6096
- Don't ship our own iradio playlist, the changes are already upstream

* Tue Dec 09 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-19.r6096
- Update to rev 6096
- Fixes some crashers during playback

* Tue Dec 02 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-18-r6086
- Update to rev 6086
- Add libmusicbrainz3 support

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.11.6-17.r6005
- Rebuild for Python 2.6

* Sat Nov 22 2008 Matthias Clasen <mclasen@redhat.com>
- Better URL
- Tweak description

* Thu Oct 30 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-15.r6005
- Update to rev 6005
- Fixes typo in the LIRC config
- Force GConf library location to be a URI on startup

* Mon Oct 27 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-15.r6002
- Update to rev 6002

* Mon Oct 20 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-14.r5988
- Update to rev 5988, add patch to avoid duplicate tracks on iPods

* Wed Oct  8 2008 Matthias Clasen  <mclasen@redhat.com> - 0.11.6-13.r5966
- Save some space

* Fri Oct 03 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-12.r5966
- Update to latest trunk
- Fix license info to match that of upstream

* Wed Oct 01 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-11.r5957
- Update source name

* Wed Oct 01 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-10.r5957
- Update to latest trunk
- Fixes lirc plugin never finishing loading

* Wed Oct 01 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-9.r5956
- Update release version

* Wed Oct 01 2008 - Bastien Nocera <bnocera@redhat.com> 0.11.6-r5956
- Update to latest trunk version, with GIO support and very many
  bug fixes
- Remove obsoleted patches, autotools and xulrunner-devel BRs

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.11.6-8
- fix license tag

* Mon Sep 01 2008 - Bastien Nocera <bnocera@redhat.com> 0.11.6-7
- Add wbur.org to the default playlist (#446791)

* Sat Aug 23 2008 - Linus Walleij <triad@df.lth.se> 0.11.6-6
- Rebuild package to pick up libmtp 0.3.0 deps

* Thu Aug 14 2008 - Bastien Nocera <bnocera@redhat.com> 0.11.6-5
- Add a default LIRC configuration, so it works out-of-the-box

* Tue Aug 12 2008 - Bastien Nocera <bnocera@redhat.com> 0.11.6-4
- Add patch for libmtp 0.3 support (#458388)

* Sat Jul 26 2008 Matthias Clasen  <mclasen@redhat.com> 0.11.6-3
- Use standard icon names in a few places

* Sun Jul 20 2008 Adam Jackson <ajax@redhat.com> 0.11.6-2
- rhythmbox-0.11.5-xfade-buffering.patch: Backport from svn to fix playback
  start when the crossfader is active.

* Mon Jul 14 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.6-1
- Update to 0.11.6
- Remove loads of upstreamed patches

* Mon Jun 16 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-15
- Avoid crash on new iPods (#451547)

* Wed May 14 2008 - Matthias Clasen <mclasen@redhat.com> - 0.11.5-14
- Rebuild again 

* Tue May 13 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-13
- Rebuild

* Wed May 07 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-12
- Prefer Ogg previews for Magnatune

* Thu Apr 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.11.5-11
- Drop big ChangeLog file

* Fri Apr 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-10
- Add patch to use the new Amazon search, the old one was shutdown

* Tue Apr 08 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-9
- Update deadlock fix patch

* Mon Apr 07 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-8
- Add patch to avoid deadlocks when playing music through the cross-fade backend

* Fri Apr 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-7
- Add patch to work-around transfer of some filenames to VFAT iPods (#440668)

* Fri Apr 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-6
- Add patch to fix CDDA autostart from nautilus (#440489)

* Mon Mar 31 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-5
- Force podcast parsing, as we already know it's a Podcast

* Mon Mar 31 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-4
- Add a 24x24 icon so it doesn't look blurry in the panel

* Thu Mar 20 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-3
- Patch from upstream to fix URL encoding, as soup_encode_uri()
  doesn't encode in place anymore, should fix track submission
  with last.fm

* Mon Mar 17 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-2
- Fix possible crasher in playlist activation

* Mon Mar 17 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.5-1
- Update to 0.11.5
- Remove outdated patches

* Thu Mar 13 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.4-13
- Big update of the UPNP plugin, with MediaRenderer support
- Add patch to make the pane window bigger by default (#437066)

* Wed Mar 12 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.4-12
- Remove ExcludeArch for ppc/ppc64

* Tue Mar 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.4-11
- Add patch to save the album artwork onto the iPod (#435952)

* Mon Mar 03 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.4-10
- Add a patch to fix activating audio players with a directory instead
  of a device path (GNOME bug #519737)

* Mon Feb 18 2008 Matthias Clasen <mclasen@redhat.com> - 0.11.4-9
- Fix the media player patch to work

* Thu Feb 14 2008 Matthias Clasen <mclasen@redhat.com> - 0.11.4-8
- Rebuild against new libsoup

* Tue Feb 05 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.4-7
- Update libsoup 2.4 patch again from upstream

* Mon Feb 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.4-6
- Update libsoup 2.4 patch from upstream
- Add patch to fix the media player keys API usage

* Tue Jan 29 2008  Matthias Clasen <mclasen@redhat.com> - 0.11.4-5
- Port to libsoup 2.4

* Fri Jan 18 2008  Matthias Clasen <mclasen@redhat.com> - 0.11.4-4
- Add content-type support

* Thu Jan 17 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.4-3
- Own the plugins dir (#389111)

* Wed Jan 09 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.4-2
- Add patch to make the power manager plugin disablable (#428034)

* Fri Dec 21 2007 Matthias Clasen <mclasen@redhat.com> - 0.11.4-1
- Update to 0.11.4

* Fri Dec 07 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.3-9
- Add patch to fix possible crasher when playing any song (#410991)

* Fri Nov 30 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.3-8
- Update patch for the Podcast parsing to include the browser plugin
  for the iTunes detection

* Fri Nov 30 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.3-7
- Add patch to avoid crashing if no Python plugins are enabled by default
  (#393531)

* Thu Nov 29 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.3-6
- Remove stupid return that caused Podcasts never to be updated
  (see http://bugzilla.gnome.org/show_bug.cgi?id=500325)

* Wed Nov 21 2007 Todd Zullinger <tmz@pobox.com> - 0.11.3-5
- Rebuild against libgpod-0.6.0

* Sat Nov 17 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.3-4
- Better DAAP fix (#382351)

* Wed Nov 14 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.3-3
- Add missing gstreamer-python run-time dependency (#382921)

* Tue Nov 13 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.3-2
- Add upstream patch to implement missing plugins support

* Mon Nov 12 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.3-1
- Update to 0.11.3
- Remove a whole load of upstreamed patches

* Sat Nov 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.11.2-14
- Rebuild against newer libmtp

* Wed Oct 31 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.2-13
- Rebuild for new totem

* Mon Oct 29 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.2-12
- Update patch for #242260, tooltips weren't working
- Add patch to fix problems importing files with spaces in them (#291571)
- Add patch to remove iPod tracks when removed, rather than put them
  in the trash (#330101)
- Add upstream patch to support new playlist parser in Totem, and add
  better Podcast support, as well as iTunes podcast support

* Mon Oct 22 2007  Matthias Clasen <mclasen@redhat.com> - 0.11.2-11
- Rebuild against new dbus-glib

* Thu Oct 11 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.2-10
- Add patch to avoid Rhythmbox escaping the primary text in notifications
  as per the spec (#242260)

* Wed Oct 10 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.2-9
- Add the plugin to handle MTP devices (#264541)

* Tue Oct 09 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.2-8
- Add patch to make the gnome-power-manager plugin work again
  (GNOME #483721)

* Tue Oct 02 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.2-7
- Add upstream patch to make the Upnp media store work (GNOME #482548)

* Thu Sep 20 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.2-6
- Init pygobject threads early (GNOME #469852)

* Tue Aug 24 2007 Todd Zullinger <tmz@pobox.com> - 0.11.2-5
- Rebuild against new libgpod

* Thu Aug 23 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.2-4
- Rebuild with PPC-enabled, now that liboil is "fixed"

* Mon Aug 20 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.2-3
- Own some directories of ours (#246156)

* Mon Aug 20 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.2-2
- Disable PPC for now
- Add the LIRC plugin (#237269)
- Add Coherence UPNP plugin

* Wed Aug 15 2007 Matthias Clasen <mclasen@redhat.com> - 0.11.2-1
- Update to 0.11.2

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 0.11.1-2
- Update the license field
- Use %%find_lang for help files

* Wed Jun 27 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.1-1
- Update to 0.11.1
- Drop obsolete patches
- Work-around a possible buggy GStreamer plugin

* Mon Jun 04 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.0-5
- Add patch to not ignore tags with trailing white spaces

* Tue May 29 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.0-4
- Update totem playlist parser requirements

* Tue May 29 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.0-3
- Use the store resize patch for 0.11.x rather than the one for 0.10.x

* Tue May 29 2007 - Bastien Nocera <bnocera@redhat.com> - 0.11.0-2
- Re-add the store resize patch, as it's not upstream

* Mon May 28 2007 Matthias Clasen <mclasen@redhat.com> - 0.11.0-1
- Update to 0.11.0
- Drop upstreamed patches

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 0.10.0-9
- Rebuild against new totem-plparser

* Tue May 08 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.0-8.fc7
- Add patch to avoid the window resizing when loading the stores
  (#236972)

* Mon Apr 30 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.0-7.fc7
- Add missing gnome-python2-gconf and gnome-python2-gnomevfs deps
  (#238363)

* Fri Apr 20 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.0-6.fc7
- Enable the Magnatune and Jamendo stores by default (#237131)

* Wed Apr 18 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.0-5.fc7
- Set the first time flag on startup, otherwise the iRadio's initial
  playlist is never loaded (Gnoem BZ #431167)

* Wed Apr 11 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.0-4.fc7
- Provide some quality Ogg radios in the default iRadio catalogue
  (#229677)

* Wed Apr 11 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.0-3.fc7
- Add requires for gnome-themes, spotted by Nigel Jones (#235818)

* Wed Apr 04 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.0-2.fc7
- Use multiple CPUs to build, the upstream bug is fixed now

* Wed Apr 04 2007 - Bastien Nocera <bnocera@redhat.com> - 0.10.0-1.fc7
- Update to the stable branch 0.10.0, fixes a large number of crashers
- Add patch for xdg-user-dirs support

* Wed Mar 28 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.8-4.fc7
- Add upstream patch for bug 234216

* Sun Mar 25 2007  Matthias Clasen <mclasen@redhat.com> - 0.9.8-3
- Fix a directory ownership issue (#233911)

* Thu Mar 15 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.8-2.fc7
- Add missing dependency on gnome-python2 for the Python gnome-vfs
 bindings (#232189)

* Wed Feb 21 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.8-1.fc7
- Update to 0.9.8, drop unneeded requirements and patches
- Change iradio default stations location
- Add new rhythmbox-core library

* Wed Jan 31 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.7-11.fc7
- Require automake in the BuildRequires as well, as we need to generate
  plugins/mmkeys/Makefile.in

* Wed Jan 31 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.7-10.fc7
- Require autoconf in the BuildRequires, as it's not in the minimum build
  environment

* Wed Jan 31 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.7-9.fc7
- Exclude s390* from the builds, as there's no gnome-media there

* Wed Jan 31 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.7-8.fc7
- Add patch to make the multimedia keys work with the new control-center
  way of doing things (#197540)

* Mon Jan 22 2007 Alexander Larsson <alexl@redhat.com> - 0.9.7-7.fc7
- Specfile cleanups from Todd Zullinger
- Buildrequire gnome-media-devel for gnome-media-profiles.pc
- Remove explicit libgpod dep
- install missing artwork image (Gnome BZ #387413)

* Tue Jan 16 2007 Alexander Larsson <alexl@redhat.com> - 0.9.7-6.fc7
- rebuild with new libgpod

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.7-5
- Update to 0.9.7

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.9.6-4
- rebuild for python 2.5

* Tue Nov 21 2006 Ray Strode <rstrode@redhat.com> - 0.9.6-3
- drop keybinding patch

* Mon Nov 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.6-2
- Rebuild

* Sun Oct 22 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.6-1
- Update to 0.9.6

* Mon Oct 2 2006 Ray Strode <rstrode@redhat.com> - 0.9.5-6.fc6
- first unfinished, buggy crack at fixing keybindings

* Mon Sep 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.9.5-5
- Enable tag editing

* Wed Sep 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.5-4
- Fix a crash when a radio station is missing  (#206170)

* Thu Sep  7 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.5-3
- Support transparent panels (#205584)

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.9.5-2
- Add BR for dbus-glib-devel 
- Add patch to fix deprecated dbus function

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.9.5-1.1
- rebuild

* Fri Jul  7 2006 Bill Nottingham <notting@redhat.com>
- don't require eel2

* Mon Jun 19 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.5-1
- Update to 0.9.5

* Wed Jun 14 2006 Bill Nottingham <notting@redhat.com> - 0.9.4.1-8
- apply patch from CVS to port to nautilus-cd-burner 2.15.3

* Wed Jun 14 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.4.1-7
- Rebuild

* Fri May 26 2006 Jeremy Katz <katzj@redhat.com> - 0.9.4.1-6
- try to fix building on s390{,x}

* Wed May 24 2006 John (J5) Palmieri <johnp@redhat.com> - 0.9.4.1-5
- Patch to build with latest libnotify

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.4.1-4
- Rebuild

* Sun May 21 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.4.1-3
- Add missing BuildRequires (#129145)

* Mon Apr 25 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.4.1-2
- Update to 0.9.4.1

* Mon Apr 17 2006 Matthias Clasen <mclasen@redhat.com> - 0.9.4-2
- Update to 0.9.4
- Drop upstreamed patches

* Wed Mar 08 2006 Ray Strode <rstrode@redhat.com> - 0.9.3.1-3
- fix icon on notification bubbles (bug 183720)
- patch from CVS to escape bubble markup, found by 
  Bill Nottingham

* Fri Mar 03 2006 Ray Strode <rstrode@redhat.com> - 0.9.3.1-2
- add patch from James "Doc" Livingston to stop a hang
  for new users (bug 183883)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.9.3.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.9.3.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Feb  4 2006 Christopher Aillon <caillon@redhat.com> 0.9.3.1-1
- Update to 0.9.3.1
- Use gstreamer (0.10)

* Wed Feb  1 2006 Christopher Aillon <caillon@redhat.com> 0.9.3-2
- Remove hack for 173869, as its no longer needed.

* Wed Feb  1 2006 Christopher Aillon <caillon@redhat.com> 0.9.3-1
- 0.9.3

* Wed Feb  1 2006 Christopher Aillon <caillon@redhat.com> 0.9.2.cvs20060201-1
- Newer CVS snapshot

* Sun Jan 22 2006 Christopher Aillon <caillon@redhat.com> 0.9.2.cvs20060123-1
- Update to latest CVS
- Add hack to workaround bug #173869

* Thu Jan 19 2006 Christopher Aillon <caillon@redhat.com> 0.9.2-8
- Rebuild, now that gstreamer08-plugins has been fixed

* Thu Jan 19 2006 Ray Strode <rstrode@redhat.com> 0.9.2-7
- bonobo multilib issue (bug 156982)

* Wed Jan 04 2006 John (J5) Palmieri <johnp@redhat.com> 0.9.2-5
- rebuild with ipod support

* Tue Jan 03 2006 Jesse Keating <jkeating@redhat.com> 0.9.2-4
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Matthias Clasen <mclasen@redhat.com>
- rebuild

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com>
- rebuild for new dbus

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com>
- Update to 0.9.2

* Tue Oct 25 2005 Matthias Clasen <mclasen@redhat.com>
- Update to 0.9.1

* Fri Sep 02 2005 Colin Walters <walters@redhat.com> 
- Add configure flags --with-bonobo --with-dbus
- BR nautilus-cd-burner-devel
- New upstream CVS snapshot for testing
- Drop IDL file and ui .xml
- Add dbus service file
- Drop upstreamed rhythmbox-bluecurve.tar.gz
- Drop upstreamed rhythmbox-0.8.8-cell-renderer.patch

* Fri Jun 13 2005 Colin Walters <walters@redhat.com> - 0.8.8-3
- Add Bluecurve-ized icons from Jeff Schroeder (157716)
- Add rhythmbox-0.8.8-cell-renderer.patch to remove use of custom
  cell renderer for playback icon (no longer necessary) and
  changes the rating renderer to work with non-b&w icons

* Mon Mar 14 2005 Colin Walters <walters@redhat.com> - 0.8.8-2
- Rebuild for GCC4

* Tue Oct 05 2004 Colin Walters <walters@redhat.com> - 0.8.8-1
- New upstream version
- Remove librb-nautilus-context-menu.so, killed upstream

* Thu Sep 30 2004 Christopher Aillon <caillon@redhat.com> 0.8.7-2
- PreReq desktop-file-utils >= 0.9

* Sat Sep 29 2004 Colin Walters <walters@redhat.com> - 0.8.7-1
- New upstream version

* Sat Sep 18 2004 Colin Walters <walters@redhat.com> - 0.8.6-2
- Fix postun to use correct syntax, thanks Nils Philippsen

* Sat Sep 18 2004 Colin Walters <walters@redhat.com> - 0.8.6-1
- New upstream version
- Call update-desktop-database in post and postun

* Thu Jun 24 2004 Colin Walters <walters@redhat.com> - 0.8.5-1
- New upstream version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 18 2004 Colin Walters <walters@redhat.com> - 0.8.4-1
- New upstream version
- Remove backported patches
- Gratuitiously bump various BuildRequires versions

* Mon May 10 2004 Colin Walters <walters@redhat.com> - 0.8.3-4
- Remove code to unregister GConf schema for now (Closes: #122532)

* Thu May 07 2004 Colin Walters <walters@redhat.com> - 0.8.3-3
- Apply tiny patch from 0.8 arch to fix GConf key used
  for initial sorting

* Thu May 07 2004 Colin Walters <walters@redhat.com> - 0.8.3-2
- Apply patch from 0.8 arch tree to fix a number of memleaks

* Thu May 02 2004 Colin Walters <walters@redhat.com> - 0.8.3-1
- Update to 0.8.3: fixes showstopper bug with internet radio

* Thu Apr 30 2004 Colin Walters <walters@redhat.com> - 0.8.2-1
- Update to 0.8.2
- Fix Source url
- Add smp_mflags
- Bump BuildRequires on gstreamer to 0.8.1

* Tue Apr 23 2004 Colin Walters <walters@redhat.com> - 0.8.1-2
- Uninstall GConf schemas on removal

* Tue Apr 20 2004 Colin Walters <walters@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Fri Apr 16 2004 Colin Walters <walters@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Fri Apr 02 2004 Colin Walters <walters@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Mon Mar 29 2004 Colin Walters <walters@redhat.com> - 0.7.1-2
- Remove BuildRequires on autoconf and libvorbis-devel

* Mon Mar 29 2004 Colin Walters <walters@redhat.com> - 0.7.1-1
- New major version - I know we are past major version slush, but
  this should have been done two weeks ago along with the GNOME 2.6
  upload.  As upstream author as well, I believe this version is
  good enough for FC2.
- Remove --disable-mp3
- Remove id3, flac variables
- Remove GStreamer major version patch
- Fix typo in description

* Tue Mar 16 2004 Jeremy Katz <katzj@redhat.com> - 0.6.8-2
- rebuild for new gstreamer

* Thu Mar 11 2004 Alex Larsson <alexl@redhat.com> 0.6.8-1
- update to 0.6.8

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar  1 2004 Alexander Larsson <alexl@redhat.com> 0.6.7-1
- update to 0.6.7

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 12 2004 Colin Walters <walters@verbum.org> 0.6.4-1
- New upstream version
- Don't re-run the autotools; upstream incorporates newer versions.
* Tue Oct 28 2003 Jonathan Blandford <jrb@redhat.com> 0.5.4-1
- new version
- remove smp_flags

* Fri Oct 24 2003 Jonathan Blandford <jrb@redhat.com> 0.5.3-5
- remove the initial iradio channels as they all are mp3 based.

* Wed Oct  8 2003 Matthias Saou <matthias@rpmforge.net> 0.5.3-3
- Fix category from Development/Libraries to Applications/Multimedia.
- Use bz2 instead of gz as ftp.gnome.org has both, 300k saved in the src.rpm.
- Fix SCHEMES vs. SCHEMAS in the post scriplet.
- Added gstreamer-plugins-devel, libvorbis-devel, scrollkeeper and gettext deps.
- Removed unnecessary date expansion define.
- Updated description, including mp3 reference removal.
- Added libid3tag and flac optional support for convenient rebuild.
- Removed obsolete omf.make and xmldocs.make (included ones are the same now).

* Mon Sep 22 2003 Jonathan Blandford <jrb@redhat.com> 0.5.3-1
- new version
- use _sysconfdir instead of /etc

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 18 2002 Jonathan Blandford <jrb@redhat.com>
- gave up on other archs for the Beta
- new version
- remove werror and add missing files

* Thu Nov  7 2002 Jeremy Katz <katzj@redhat.com>
- update to newer cvs snap

* Mon Sep 23 2002 Jeremy Katz <katzj@redhat.com>
- update to cvs snap

* Sun Sep 22 2002 Jeremy Katz <katzj@redhat.com>
- use %%(lang)

* Sun Aug 11 2002 Jeremy Katz <katzj@redhat.com>
- fix post to actually install the schema

* Sat Jun 22 2002 Christian F.K. Schaller <Uraeus@linuxrising.org>
- Added gconf file
- Added i18n directory

* Sat Jun 15 2002 Christian F.K. Schaller <Uraeus@linuxrising.org>
- Updated for new rewrite of rhythmbox, thanks to Jeroen

* Mon Mar 18 2002 Jorn Baayen <jorn@nl.linux.org>
- removed bonobo dependency
* Sat Mar 02 2002 Christian Schaller <Uraeus@linuxrising.org>
- created new spec file
