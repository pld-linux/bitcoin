# TODO: Readd missing icons/*.destktop deleted from contrib/debian during 0.14.0 -> 0.14.2
# TODO: Consider running as system-wide service (check contrib/init) with own user/group
Summary:	Bitcoin is a peer-to-peer currency
Name:		bitcoin
Version:	0.14.2
Release:	0.1
License:	MIT/X11
Group:		X11/Applications
# Source0:	https://github.com/bitcoin/bitcoin/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://bitcoin.org/bin/bitcoin-core-%{version}/bitcoin-%{version}.tar.gz
# Source0-md5:	4324327fbb2d696b98809b3ddbd40b0c
# https://bitcoin.org/bin/bitcoin-core-0.14.2/bitcoin-0.14.2.tar.gz
URL:		http://www.bitcoin.org
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel
BuildRequires:	db-cxx-devel
BuildRequires:	libtool
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	protobuf-devel
BuildRequires:	qrencode-devel
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
./autogen.sh

%configure \
	--disable-silent-rules \
	--with-miniupnpc \
	--with-qrencode \
	--with-incompatible-bdb \
	--with-boost \
	--with-gui=qt4 \
	--with-qtdbus

%{__make}


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_mandir}/man{1,5},%{_localedir},%{_desktopdir},%{_pixmapsdir},%{_datadir}/kde4/services}

%{__make} install \
		DESTDIR=$RPM_BUILD_ROOT

# TODO: gone during 0.14.0 -> 0.14.2
# cp -p contrib/debian/bitcoin-qt.desktop $RPM_BUILD_ROOT%{_desktopdir}
# cp -p contrib/debian/bitcoin-qt.protocol $RPM_BUILD_ROOT%{_datadir}/kde4/services
# cp -p share/pixmaps/bitcoin{32,64,128,256}.png $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*.txt 
%attr(755,root,root) %{_bindir}/bitcoin-cli
%attr(755,root,root) %{_bindir}/bitcoin-tx
%attr(755,root,root) %{_bindir}/bitcoind
%attr(755,root,root) %ghost %{_libdir}/libbitcoinconsensus.so.0
%attr(755,root,root) %{_libdir}/libbitcoinconsensus.so.*.*
%{_mandir}/man1/bitcoin-cli.1*
%{_mandir}/man1/bitcoin-tx.1*
%{_mandir}/man1/bitcoind.1*

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bitcoin-qt
#%%{_datadir}/kde4/services/bitcoin-qt.protocol
#%%{_desktopdir}/bitcoin-qt.desktop
#%%{_pixmapsdir}/bitcoin*.png
%{_mandir}/man1/bitcoin-qt.1*
