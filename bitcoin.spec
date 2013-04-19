Summary:	Bitcoin is a peer-to-peer currency
Name:		bitcoin
Version:	0.8.1
Release:	1
License:	MIT/X11
Group:		X11/Applications
Source0:	https://github.com/bitcoin/bitcoin/archive/v%{version}.tar.gz
# Source0-md5:	d767f23fa7a2ce0143f738b30deb32e0
URL:		http://www.bitcoin.org
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	boost-devel
BuildRequires:	db-cxx-devel
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	qrencode-devel
BuildRequires:	qt4-qmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bitcoin is a peer-to-peer currency. Peer-to-peer means that no central
authority issues new money or tracks transactions. These tasks are
managed collectively by the network.

%prep
%setup -q

%build
qmake-qt4 \
	USE_UPNP=1 \
	USE_DBUS=1 \
	USE_QRCODE=1

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_localedir},%{_desktopdir},%{_pixmapsdir},%{_datadir}/kde4/services}

install bitcoin-qt $RPM_BUILD_ROOT%{_bindir}
install contrib/debian/bitcoin-qt.desktop $RPM_BUILD_ROOT%{_desktopdir}
install contrib/debian/bitcoin-qt.protocol $RPM_BUILD_ROOT%{_datadir}/kde4/services
install share/pixmaps/bitcoin{32,80}.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.txt
%attr(755,root,root) %{_bindir}/bitcoin-qt
%{_datadir}/kde4/services/bitcoin-qt.protocol
%{_desktopdir}/bitcoin-qt.desktop
%{_pixmapsdir}/bitcoin*.xpm
