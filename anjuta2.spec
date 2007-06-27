%define pkgname anjuta

%define major 0
%define libname %mklibname %{pkgname} %major
%define libnamedev %mklibname %{pkgname}  -d

Summary:	Integrated development environment for C and C++ (Linux)
Name:		%{pkgname}2
Version:	2.1.3
Release:	%mkrel 2
License:	GPL
Group:		Development/Other
URL:		http://anjuta.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/anjuta/%{pkgname}-%{version}.tar.bz2
Patch0:		anjuta-2.0.0-alt-packagename.patch
Patch1: 	anjuta-2.0.1-link.patch
Patch2: 	anjuta-2.0.2-fix-compile-with-nls.patch
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
BuildRequires:	perl-XML-Parser
BuildRequires:	libgladeui-devel >= 3.0.0
BuildRequires:	gtk+2-devel >= 2.4.0
BuildRequires:	libORBit2-devel >= 2.6
BuildRequires:	libgnome2-devel >= 2.6
BuildRequires:	libglade2.0-devel >= 2.3.0
BuildRequires:	libgnomeui2-devel >= 2.6.0
BuildRequires:	libgnomeprintui-devel >= 2.4.0
BuildRequires:	gnome-vfs2-devel >= 2.6.0
BuildRequires:	libxml2-devel >= 2.4.23
BuildRequires:	pango-devel >= 1.8
BuildRequires:	libgdl-devel >= 0.5
BuildRequires:	libxslt-devel
BuildRequires:	devhelp-devel >= 0.9
BuildRequires:	libgladeui-devel >= 3.0.0
BuildRequires:	libvte-devel >= 0.9.0
BuildRequires:	libautogen-devel
BuildRequires:	autogen
BuildRequires:	gnome-build-devel >= 0.1.4
BuildRequires:	gtksourceview-devel
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	subversion-devel >= 1.0.2
BuildRequires:	apr-util-devel >= 0.9.4
BuildRequires:	binutils-devel
BuildRequires:	pcre-devel
BuildRequires:	neon-devel >= 0.24.5
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gnome-doc-utils >= 0.4.2
BuildRequires:	apr-devel >= 1.2.2
BuildRequires:	libgd-devel
BuildRequires:	libgraphviz-devel >= 2.2.1
BuildRequires:	scrollkeeper
BuildRequires:  howl-devel
BuildRequires:	glade3-devel
BuildRequires:	ImageMagick
Provides:	anjuta = %{version} gnome-build
Conflicts:	anjuta < 2
BuildRoot:	%{_tmppath}/%{pkgname}-%{version}-buildroot

%description
Anjuta is a versatile IDE for C and C++, written for GTK/GNOME. Features
include project management, application wizards, an onboard interactive
debugger, and a powerful source editor with browsing and syntax
highlighting.

This version of anjuta is the GNOME 2 port of anjuta 1.0, which
was for GNOME 1.x originally. The one written from scratch and
for GNOME 2 from the start has been renamed "Scaffold".

This is an alpha & unstable release and may not be suitable for production use.
However, we encourage to use it and help us with bug reports.
Both stable and development release can be used simultaneously,
but they should be installed in different install prefix (important).

%package -n %{libname}
Summary: Anjuta 2 libraries
Group: System/Libraries

%description -n %{libname}
Anjuta 2 libraries

%package -n %{libnamedev}
Summary: Anjuta 2 devel files
Group: Development/Other
Requires: %libname = %version
Provides: libanjuta-devel
Obsoletes: %mklibname -d %{pkgname} %{major}

%description -n %{libnamedev}
Anjuta 2 devel files 

%prep
%setup -q -n %{pkgname}-%{version}
%{__perl} -pi -e "s|\<%_name\>|%name|g" anjuta.desktop.in.in
%{__perl} -pi -e "s|%_name/|%name/|g" global-tags/Makefile.am plugins/class-gen/Makefile.am
#mv %name. mime/anjuta*
%{__perl} -pi -e "s| %_name\.| %name.|g" mime/Makefile.am
%{__perl} -pi -e "s|^GETTEXT_PACKAGE=%_name$|GETTEXT_PACKAGE=%name|" configure.in
%{__perl} -pi -e 's|update-mime-database .*;|	echo;|' mime/Makefile.am
#%patch0
#%patch1 -p1
%patch2 -p0

%build
%__rm -f missing
NOCONFIGURE=1 ./autogen.sh
%configure2_5x \
    --disable-static \
    --disable-plugin-glade \
    --enable-plugin-valgrind \
    --enable-plugin-scintilla \
    --enable-plugin-sourceview \
    --enable-plugin-class-inheritance \
    --enable-final \
    --enable-optimize \
    --enable-gtk-doc 
make

%install
rm -rf %{buildroot}
%makeinstall_std
cat global-tags/create_global_tags.sh | sed -e s/'PROGDIR=.'/'PROGDIR=\/usr\/bin'/ > %{buildroot}%{_datadir}/anjuta/scripts/create_global_tags.sh
chmod 755 %{buildroot}%{_datadir}/anjuta/scripts/create_global_tags.sh

# make a link in /usr/share/pixmaps
pushd %buildroot%_datadir/pixmaps
%__ln_s -f %name/anjuta_icon.png %name.png
popd

mv $RPM_BUILD_ROOT%{_datadir}/applications/anjuta.desktop $RPM_BUILD_ROOT%{_datadir}/applications/%name.desktop

# menu
mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
command="%{_bindir}/anjuta" \
title="Anjuta IDE" \
longtitle="Anjuta Integrated Development Environment for C/C++" \
needs="x11" \
icon="%{name}.png" \
section="More Applications/Development/Development Environments" \
startup_notify="yes" \
xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="IDE" \
  --add-category="X-MandrivaLinux-MoreApplications-Development-DevelopmentEnvironments" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


# icons
mkdir -p %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
install -m 644 -D       pixmaps/anjuta_logo.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/anjuta_logo.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/anjuta_logo.png %{buildroot}%{_miconsdir}/%{name}.png

%find_lang %{pkgname} --with-gnome
 
# remove unneeded and conflictive files
rm -f %{buildroot}%{_libdir}/libanjuta*.la \
      %{buildroot}%{_libdir}/libanjuta*.a \
      %{buildroot}%{_datadir}/mime/XMLnamespaces \
      %{buildroot}%{_datadir}/mime/aliases \
      %{buildroot}%{_datadir}/mime/globs \
      %{buildroot}%{_datadir}/mime/magic \
      %{buildroot}%{_datadir}/mime/subclasses
rm -rf %{buildroot}/%{_docdir}

%clean
rm -rf %{buildroot}

%define schemas anjuta-valgrind

%post
cd %{_datadir}/anjuta2
./create_global_tags.sh
%update_menus
%update_scrollkeeper
%post_install_gconf_schemas %{schemas}
%update_icon_cache hicolor
%update_mime_database

%post -n %libname -p /sbin/ldconfig

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%clean_menus
%clean_scrollkeeper
%clean_icon_cache hicolor
%clean_mime_database

%postun -n %libname -p /sbin/ldconfig

%files -f %{pkgname}.lang
%defattr(-,root,root) 
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/*
%{_libdir}/anjuta/*.plugin
%_libdir/anjuta/*.so
%{_datadir}/anjuta/*
%{_datadir}/applications/%name.desktop
%{_datadir}/gtk-doc/html/libanjuta/*
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-x-anjuta.png
%{_datadir}/man/man1/anjuta.1.*
%{_datadir}/man/man1/anjuta_launcher.1.*
%{_datadir}/mime/packages/anjuta.xml
%{_datadir}/pixmaps/%name.png
%{_datadir}/pixmaps/anjuta/*
#%{_datadir}/anjuta/class-templates/*
%{_datadir}/icons/hicolor/48x48/apps/anjuta.png
%{_datadir}/icons/hicolor/scalable/apps/anjuta.svg
%{_datadir}/icons/gnome/scalable/mimetypes/*.svg
%{_datadir}/omf/anjuta-manual/*.omf
%{_menudir}/%{name}
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_libdir}/pkgconfig/libanjuta-1.0.pc
%{_datadir}/gnome/help/anjuta-manual/
%{_datadir}/gnome/help/anjuta-faqs/
%{_localstatedir}/scrollkeeper/*

#%files -n %name-devel
#%{_libdir}/pkgconfig/libanjuta-1.0.pc
#%{_datadir}/%name/indent_test.*
#%{_datadir}/%name/project/gnome/src/
#%{_datadir}/%name/project/terminal/src/
#%{_datadir}/%name//usr/share/anjuta2/project/xlib/src/
#%{_datadir}/%name//usr/share/anjuta2/project/gtk/src/
#%{_datadir}/%name//usr/share/anjuta2/project/xlib-dock/src/
#%{_datadir}/%name//usr/share/anjuta2/project/anjuta-plugin/src/plugin.c
#%{_datadir}/%name//usr/share/anjuta2/project/gnome/src/
#%{_datadir}/%name//usr/share/anjuta2/project/mkfile/src/main.c

%files -n %libname
%defattr(-,root,root)
%_libdir/*.so.*
%_libdir/anjuta/*.so.*

%files -n %libnamedev
%defattr(-,root,root)
%_libdir/*.so
%_includedir/libanjuta-1.0
%_libdir/anjuta/*.*a

