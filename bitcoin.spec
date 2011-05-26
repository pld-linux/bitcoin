Summary:	Bitcoin is a peer-to-peer currency
Name:		bitcoin
Version:	0.3.21
Release:	0.1
License:	MIT/X11
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/bitcoin/%{name}-%{version}-linux.tar.gz
# Source0-md5:	19e530a9b60e3a0987998a87b30d8cdc
Patch0:		%{name}-boost.patch
Patch1:		%{name}-nostatic.patch
URL:		http://www.bitcoin.org
BuildRequires:	boost-devel
BuildRequires:	db-cxx-devel
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	wxGTK2-unicode-devel >= 2.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bitcoin is a peer-to-peer currency. Peer-to-peer means that no central
authority issues new money or tracks transactions. These tasks are
managed collectively by the network.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} -C src -f makefile.unix \
	CXX="%{__cxx}" \
	WXINCLUDEPATHS="$(wx-gtk2-unicode-2.9-config --cxxflags)" \
	WXLIBS="$(wx-gtk2-unicode-2.9-config --libs)" \
	USE_UPNP=1

%{__make} -C src -f makefile.unix \
	CXX="%{__cxx}" \
	WXINCLUDEPATHS="$(wx-gtk2-unicode-2.9-config --cxxflags)" \
	WXLIBS="$(wx-gtk2-unicode-2.9-config --libs)" \
	USE_UPNP=1 \
	bitcoind

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_localedir}}

install src/{bitcoin,bitcoind} $RPM_BUILD_ROOT%{_bindir}

# install locales
for dir in $(find locale/ -mindepth 1 -maxdepth 1 -type d); do
	lang=$(basename $dir)
	
	install -d $RPM_BUILD_ROOT%{_localedir}/$lang/LC_MESSAGES
	install $dir/LC_MESSAGES/bitcoin.mo $RPM_BUILD_ROOT%{_localedir}/$lang/LC_MESSAGES
done

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bitcoin
%attr(755,root,root) %{_bindir}/bitcoind
