%define pkgname anjuta

%define major 0
%define libname %mklibname %{pkgname} %major
%define libnamedev %mklibname %{pkgname}  -d

%define _requires_exceptions perl.GBF..Make.
Summary:	Integrated development environment for C and C++ (Linux)
Name:		%{pkgname}2
Version:	2.28.1.0
Release:	%mkrel 1
License:	GPLv2+
Group:		Development/Other
URL:		http://anjuta.sourceforge.net/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/anjuta/%{pkgname}-%{version}.tar.bz2
Patch: anjuta-2.27.91.0-format-strings.patch
BuildRequires:	gtk+2-devel >= 2.4.0
BuildRequires:	libORBit2-devel >= 2.6
BuildRequires:	libxml2-devel >= 2.4.23
BuildRequires:	pango-devel >= 1.8
BuildRequires:	gda4.0-devel
BuildRequires:	libgdl-devel >= 2.27.3
BuildRequires:	libxslt-devel
BuildRequires:	unique-devel
BuildRequires:	devhelp-devel >= 0.22
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
BuildRequires:	glade3-devel >= 1:3.6.0
BuildRequires:	imagemagick
Requires:	autogen
Suggests:	libglademm-devel
Suggests:	glade3
Provides:	anjuta = %{version}
Obsoletes:	anjuta < 2
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
%patch -p1 -b .format-strings

%build
%configure2_5x \
    --disable-static \
    --enable-plugin-sourceview

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

%define schemas anjuta-build-basic-autotools-plugin anjuta-cvs-plugin anjuta-document-manager anjuta-editor-scintilla anjuta-editor-sourceview anjuta-language-cpp-java anjuta-message-manager-plugin anjuta-symbol-browser-plugin anjuta-terminal-plugin anjuta-valgrind anjuta

%if %mdkversion < 200900
%post
%update_menus
%post_install_gconf_schemas %{schemas}
%update_icon_cache hicolor
%update_mime_database
%endif

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%preun
%preun_uninstall_gconf_schemas %{schemas}

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%clean_mime_database
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -f %{pkgname}.lang
%defattr(-,root,root)
%{_sysconfdir}/gconf/schemas/*.schemas
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

%files -n %libnamedev
%defattr(-,root,root)
%_libdir/*.so
%_includedir/libanjuta-1.0
%_libdir/pkgconfig/*.pc
