# TODO: Readd missing icons/*.destktop deleted from contrib/debian during 0.14.0 -> 0.14.2
# TODO: Consider running as system-wide service (check contrib/init) with own user/group
Summary:	Bitcoin is a peer-to-peer currency
Summary(pl.UTF-8):	Bitcoin - waluta peer-to-peer
Name:		bitcoin
Version:	22.0
Release:	2
License:	MIT
Group:		X11/Applications
# Source0:	https://github.com/bitcoin/bitcoin/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://bitcoin.org/bin/bitcoin-core-%{version}/bitcoin-%{version}.tar.gz
# Source0-md5:	f822f7e798fbdc36e8fc18b355ab446d
Patch1:		univalue.patch
URL:		http://www.bitcoin.org/
BuildRequires:	Qt5Core-devel >= 5.0
BuildRequires:	Qt5DBus-devel >= 5.0
BuildRequires:	Qt5Gui-devel >= 5.0
BuildRequires:	Qt5Network-devel >= 5.0
BuildRequires:	Qt5Widgets-devel >= 5.0
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.13
BuildRequires:	boost-devel >= 1.49
BuildRequires:	db-cxx-devel >= 4.8
BuildRequires:	gettext-tools
BuildRequires:	libevent-devel >= 2
# -std=c++11
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2
BuildRequires:	libunivalue-devel >= 1.0.4
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf-devel
BuildRequires:	python3 >= 1:3.5
BuildRequires:	qrencode-devel
BuildRequires:	zeromq-devel >= 4
Requires:	libunivalue >= 1.0.4
Requires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bitcoin is a peer-to-peer currency. Peer-to-peer means that no central
authority issues new money or tracks transactions. These tasks are
managed collectively by the network.

%description -l pl.UTF-8
Bitcoin to waluta peer-to-peer. Oznacza to, że nie ma centralnej
instytucji emitującej nowe pieniądze czy śledzącej transakcje. Zadania
te są zarządzane kolektywnie przez sieć.

%package devel
Summary:	Header file for bitcoinconsensus library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki bitcoinconsensus
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel

%description devel
Header file for bitcoinconsensus library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki bitcoinconsensus.

%package static
Summary:	Static bitcoinconsensus library
Summary(pl.UTF-8):	Statyczna biblioteka bitcoinconsensus
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static bitcoinconsensus library.

%description static -l pl.UTF-8
Statyczna biblioteka bitcoinconsensus.

%package qt
Summary:	Qt-based Bitcoin Wallet
Summary(pl.UTF-8):	Portfel na bitcoiny oparty na Qt
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description qt
Qt-based Bitcoin Wallet.

%description qt -l pl.UTF-8
Portfel na bitcoiny oparty na Qt.

%prep
%setup -q
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I build-aux/m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd src/secp256k1
%{__libtoolize}
%{__aclocal} -I build-aux/m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../..
%configure \
	--disable-silent-rules \
	--with-boost \
	--with-gui=qt4 \
	--with-incompatible-bdb \
	--with-miniupnpc \
	--with-qrencode \
	--with-qtdbus \
	--with-system-univalue

%{__make}


%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_datadir}/kde4/services}

%{__make} install \
		DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbitcoinconsensus.la

# TODO: gone during 0.14.0 -> 0.14.2
# cp -p contrib/debian/bitcoin-qt.desktop $RPM_BUILD_ROOT%{_desktopdir}
# cp -p contrib/debian/bitcoin-qt.protocol $RPM_BUILD_ROOT%{_datadir}/kde4/services
# cp -p share/pixmaps/bitcoin{32,64,128,256}.png $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING doc/*.txt 
%attr(755,root,root) %{_bindir}/bitcoin-cli
%attr(755,root,root) %{_bindir}/bitcoin-tx
%attr(755,root,root) %{_bindir}/bitcoin-util
%attr(755,root,root) %{_bindir}/bitcoin-wallet
%attr(755,root,root) %{_bindir}/bitcoind
%attr(755,root,root) %{_libdir}/libbitcoinconsensus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbitcoinconsensus.so.0
%{_mandir}/man1/bitcoin-cli.1*
%{_mandir}/man1/bitcoin-tx.1*
%{_mandir}/man1/bitcoin-util.1*
%{_mandir}/man1/bitcoin-wallet.1*
%{_mandir}/man1/bitcoind.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbitcoinconsensus.so
%{_includedir}/bitcoinconsensus.h
%{_pkgconfigdir}/libbitcoinconsensus.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libbitcoinconsensus.a

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bitcoin-qt
#%%{_datadir}/kde4/services/bitcoin-qt.protocol
#%%{_desktopdir}/bitcoin-qt.desktop
#%%{_pixmapsdir}/bitcoin*.png
%{_mandir}/man1/bitcoin-qt.1*
