%define pkgname anjuta

%define major 0
%define libname %mklibname %{pkgname} %major
%define libnamedev %mklibname %{pkgname}  -d

Summary:	Integrated development environment for C and C++ (Linux)
Name:		%{pkgname}2
Version:	2.3.2
Release:	%mkrel 1
License:	GPLv2+
Group:		Development/Other
URL:		http://anjuta.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/anjuta/%{pkgname}-%{version}.tar.bz2
Patch0:		anjuta-2.0.0-alt-packagename.patch
Patch1: 	anjuta-2.0.1-link.patch
Patch2: 	anjuta-2.0.2-fix-compile-with-nls.patch
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
BuildRequires:	vte-devel >= 0.9.0
BuildRequires:	autogen-devel
BuildRequires:	autogen
BuildRequires:	gnome-build-devel >= 0.2.0
BuildRequires:	gtksourceview-devel
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	subversion-devel >= 1.0.2
BuildRequires:	apr-util-devel >= 0.9.4
BuildRequires:	binutils-devel
BuildRequires:	pcre-devel
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gnome-doc-utils >= 0.4.2
BuildRequires:	apr-devel >= 1.2.2
BuildRequires:	gd-devel
BuildRequires:	graphviz-devel >= 2.2.1
BuildRequires:	scrollkeeper
BuildRequires:  howl-devel
BuildRequires:	glade3-devel
BuildRequires:	ImageMagick
Requires:	autogen
Suggests:	libglademm-devel
Suggests:	glade3
Provides:	anjuta = %{version}
Conflicts:	anjuta < 2
Conflicts:	%libnamedev < 2.3.1-2
BuildRoot:	%{_tmppath}/%{pkgname}-%{version}-buildroot

%description
Anjuta DevStudio is a versatile Integrated Development Environment (IDE)
on GNOME Desktop Environment and features a number of advanced
programming facilities. These include project management, application and
class wizards, an on-board interactive debugger, powerful source editor,
syntax highlighting, intellisense autocompletions, symbol navigation,
version controls, integrated GUI designing and other tools.

Anjuta 2.x is the next generation Anjuta development studio with extensible
plugin architecture. The new architecture allows writing independent
plugins that could interact with existing plugins. Most of the older
features have been already ported to the new architecture and are working.

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
Conflicts: %name < 2.3.1-2
Obsoletes: %mklibname -d %{pkgname} %{major}

%description -n %{libnamedev}
Anjuta 2 devel files

%prep
%setup -q -n %{pkgname}-%{version}
%{__perl} -pi -e "s|\<%_name\>|%name|g" anjuta.desktop.in.in
%{__perl} -pi -e "s|%_name/|%name/|g" global-tags/Makefile.am plugins/class-gen/Makefile.am
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
    --enaable-plugin-glade \
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

mv $RPM_BUILD_ROOT%{_datadir}/applications/anjuta.desktop $RPM_BUILD_ROOT%{_datadir}/applications/%name.desktop

desktop-file-install --vendor="" \
  --remove-key='Encoding' \
  --add-category="IDE" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# icons
mkdir -p %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
install -m 644 -D       pixmaps/anjuta_logo.png %{buildroot}%{_liconsdir}/%{pkgname}.png
convert -geometry 32x32 pixmaps/anjuta_logo.png %{buildroot}%{_iconsdir}/%{pkgname}.png
convert -geometry 16x16 pixmaps/anjuta_logo.png %{buildroot}%{_miconsdir}/%{pkgname}.png

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
%update_menus
%post_install_gconf_schemas %{schemas}
%update_icon_cache hicolor
%update_mime_database

%post -n %libname -p /sbin/ldconfig

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%clean_menus
%clean_icon_cache hicolor
%clean_mime_database

%postun -n %libname -p /sbin/ldconfig

%files -f %{pkgname}.lang
%defattr(-,root,root)
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/*
%{_libdir}/glade3/modules/*
%{_libdir}/anjuta
%{_datadir}/anjuta
%{_datadir}/glade3/catalogs/*.xml
%{_datadir}/applications/%name.desktop
%{_datadir}/gtk-doc/html/libanjuta*
%{_datadir}/icons/gnome/*/mimetypes/*
%{_mandir}/man1/anjuta.1.*
%{_mandir}/man1/anjuta_launcher.1.*
%{_datadir}/mime/packages/anjuta.xml
%{_datadir}/pixmaps/anjuta
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/omf/anjuta-manual/*.omf
%{_liconsdir}/%{pkgname}.png
%{_iconsdir}/%{pkgname}.png
%{_miconsdir}/%{pkgname}.png
%{_datadir}/gnome/help/anjuta-manual/
%{_datadir}/gnome/help/anjuta-faqs/


%files -n %libname
%defattr(-,root,root)
%_libdir/*.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root)
%_libdir/*.so
%_includedir/libanjuta-1.0
%_libdir/pkgconfig/*.pc
