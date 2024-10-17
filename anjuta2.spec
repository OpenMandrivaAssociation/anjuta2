%define pkgname anjuta

%define major 0
%define libname %mklibname %{pkgname} %major
%define libnamedev %mklibname %{pkgname}  -d

%define _requires_exceptions perl.GBF..Make.
Summary:	Integrated development environment for C and C++ (Linux)
Name:		%{pkgname}2
Version:	2.32.1.1
Release:	%mkrel 4
License:	GPLv2+
Group:		Development/Other
URL:		https://anjuta.sourceforge.net/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/anjuta/%{pkgname}-%{version}.tar.bz2
Patch0: anjuta-2.31.6.0-format-strings.patch
Patch1: anjuta-2.29.4.0-fix-linking.patch
Patch2: 04_vala_0_12.patch
BuildRequires:	gtk+2-devel >= 2.4.0
BuildRequires:	libORBit2-devel >= 2.6
BuildRequires:	libxml2-devel >= 2.4.23
BuildRequires:	pango-devel >= 1.8
BuildRequires:	gda4.0-devel
BuildRequires:	libgdl-devel >= 2.27.3
BuildRequires:	libxslt-devel
BuildRequires:	unique-devel
BuildRequires:	devhelp-devel >= 2.31.6
BuildRequires:	vte-devel >= 0.9.0
BuildRequires:	autogen-devel
BuildRequires:	autogen
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
BuildRequires:	graphviz-devel >= 2.22
BuildRequires:	scrollkeeper
BuildRequires:  howl-devel
BuildRequires:	glade3-devel >= 1:3.7.1
BuildRequires:	vala-devel >= 0.9.4
BuildRequires:	GConf2
#gw https://bugzilla.gnome.org/show_bug.cgi?id=628397
#BuildRequires:	gobject-introspection-devel
BuildRequires:	glib2-devel >= 2.25.15
BuildRequires:	imagemagick
Requires:	autogen
Suggests:	libglademm-devel
Suggests:	glade3
Provides:	anjuta = %{version}
Obsoletes:	anjuta < 2
Conflicts:	%libnamedev < %version
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
Provides: libanjuta-devel = %version-%release
Conflicts: %name < 2.3.1-2
Obsoletes: %mklibname -d %{pkgname} %{major}

%description -n %{libnamedev}
Anjuta 2 devel files

%prep
%setup -q -n %{pkgname}-%{version}
%autopatch -p1
autoreconf -fi

%build
%configure2_5x --disable-schemas-install \
    --disable-static \
    --disable-vala \
    --enable-plugin-sourceview \
    --enable-introspection=no
%make

%install
rm -rf %{buildroot} *.lang
%makeinstall_std

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
%find_lang anjuta-build-tutorial --with-gnome
cat anjuta-build-tutorial.lang >> anjuta.lang

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

%define schemas anjuta-build-basic-autotools-plugin anjuta-cvs-plugin anjuta-document-manager anjuta-editor-sourceview anjuta-language-cpp-java anjuta-message-manager-plugin anjuta-terminal-plugin anjuta-debug-manager anjuta-symbol-db file-manager preferences python-plugin-properties

%preun
%preun_uninstall_gconf_schemas %{schemas}

%files -f %{pkgname}.lang
%defattr(-,root,root)
%{_sysconfdir}/gconf/schemas/anjuta-build-basic-autotools-plugin.schemas
%{_sysconfdir}/gconf/schemas/anjuta-cvs-plugin.schemas
%{_sysconfdir}/gconf/schemas/anjuta-document-manager.schemas
%{_sysconfdir}/gconf/schemas/anjuta-debug-manager.schemas
%{_sysconfdir}/gconf/schemas/anjuta-editor-sourceview.schemas
%{_sysconfdir}/gconf/schemas/anjuta-language-cpp-java.schemas
%{_sysconfdir}/gconf/schemas/anjuta-message-manager-plugin.schemas
%{_sysconfdir}/gconf/schemas/anjuta-symbol-db.schemas
%{_sysconfdir}/gconf/schemas/anjuta-terminal-plugin.schemas
%{_sysconfdir}/gconf/schemas/file-manager.schemas
%{_sysconfdir}/gconf/schemas/preferences.schemas
%{_sysconfdir}/gconf/schemas/python-plugin-properties.schemas
%{_bindir}/*
%{_libdir}/glade3/modules/*
%{_libdir}/anjuta
%{_datadir}/anjuta
%{_datadir}/glade3/catalogs/*.xml
%{_datadir}/applications/*.desktop
%{_datadir}/gtk-doc/html/libanjuta*
%{_datadir}/icons/gnome/*/mimetypes/*
%{_mandir}/man1/anjuta.1*
%{_mandir}/man1/anjuta-launcher.1*
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
#%_libdir/girepository-1.0/Anjuta-1.0.typelib
#%_libdir/girepository-1.0/IAnjuta-1.0.typelib

%files -n %libnamedev
%defattr(-,root,root)
%_libdir/*.so
%_includedir/libanjuta-1.0
%_libdir/pkgconfig/*.pc
#%_datadir/gir-1.0/Anjuta-1.0.gir
#%_datadir/gir-1.0/IAnjuta-1.0.gir
