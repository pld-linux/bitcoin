Summary:	Bitcoin is a peer-to-peer currency
Name:		bitcoin
Version:	0.3.21
Release:	0.1
License:	MIT/X11
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/bitcoin/%{name}-%{version}-linux.tar.gz
# Source0-md5:	19e530a9b60e3a0987998a87b30d8cdc
URL:		http://www.bitcoin.org
BuildRequires:	boost-devel
BuildRequires:	miniupnpc-devel
BuildRequires:	openssl-devel
BuildRequires:	wxGTK2-unicode-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bitcoin is a peer-to-peer currency. Peer-to-peer means that no central
authority issues new money or tracks transactions. These tasks are
managed collectively by the network.

%prep
%setup -q

%build
%{__make} -C src -f makefile.unix \
	CXX="%{__cxx}" \
	WXINCLUDEPATHS="$(wx-gtk2-unicode-config --cxxflags)" \
	WXLIBS="$(wx-gtk2-unicode-config --libs)" \
	USE_UPNP=1 \

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
