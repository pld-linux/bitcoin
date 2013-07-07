Summary:	Bitcoin is a peer-to-peer currency
Name:		bitcoin
Version:	0.8.3
Release:	2
License:	MIT/X11
Group:		X11/Applications
Source0:	https://github.com/bitcoin/bitcoin/archive/v%{version}.tar.gz
# Source0-md5:	18184d3284044a615cb36eb617eebd95
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
Requires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bitcoin is a peer-to-peer currency. Peer-to-peer means that no central
authority issues new money or tracks transactions. These tasks are
managed collectively by the network.

%package qt
Summary:	Qt-based Bitcoin Wallet
Group:		X11/Applications

%description qt
Qt-based Bitcoin Wallet.

%prep
%setup -q

%build
qmake-qt4 \
	USE_UPNP=1 \
	USE_DBUS=1 \
	USE_QRCODE=1

%{__make}

%{__make} -C src -f makefile.unix \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} %{rpmcxxflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{_mandir}/man{1,5},%{_localedir},%{_desktopdir},%{_pixmapsdir},%{_datadir}/kde4/services}

install src/bitcoind $RPM_BUILD_ROOT%{_bindir}
install bitcoin-qt $RPM_BUILD_ROOT%{_bindir}
install contrib/debian/bitcoin-qt.desktop $RPM_BUILD_ROOT%{_desktopdir}
install contrib/debian/bitcoin-qt.protocol $RPM_BUILD_ROOT%{_datadir}/kde4/services
install share/pixmaps/bitcoin{32,64,128,256}.png $RPM_BUILD_ROOT%{_pixmapsdir}

install contrib/debian/manpages/bitcoind.1 $RPM_BUILD_ROOT%{_mandir}/man1
install contrib/debian/manpages/bitcoin.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.txt contrib/debian/examples/bitcoin.conf
%attr(755,root,root) %{_bindir}/bitcoind
%{_mandir}/man1/bitcoind.1*
%{_mandir}/man5/bitcoin.conf.5*

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bitcoin-qt
%{_datadir}/kde4/services/bitcoin-qt.protocol
%{_desktopdir}/bitcoin-qt.desktop
%{_pixmapsdir}/bitcoin*.png
