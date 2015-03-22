Summary:	shadow tool suite
Name:		shadow
Version:	4.2.1
Release:	6
License:	GPL v2 and BSD
Group:		Applications/System
Source0:	http://pkg-shadow.alioth.debian.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	2bfafe7d4962682d31b5eba65dba4fc8
Source1:	login.defs
Source2:	useradd
Source3:	common.pamd
Source4:	passwd.pamd
Source5:	lastlog.tmpfiles
URL:		http://pkg-shadow.alioth.debian.org/
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	pam-devel
BuildRequires:	pkg-config
Obsoletes:	pwdutils
Provides:	pwdutils = 3.2.20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The shadow-utils package includes the necessary programs for
converting UNIX password files to the shadow password format, plus
programs for managing user and group accounts.

%prep
%setup -q

%build
%configure \
	--disable-shadowgrp	\
	--disable-shared	\
	--with-group-name-max-length=32	\
	--with-libpam		\
	--with-sha-crypt	\
	--without-audit		\
	--without-libcrack	\
	--without-nscd 		\
	--without-selinux
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/login.defs
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/default/useradd

touch $RPM_BUILD_ROOT%{_sysconfdir}/shadow

%{__rm} $RPM_BUILD_ROOT%{_bindir}/{chfn,chsh,faillog,login,sg,su}
%{__rm} $RPM_BUILD_ROOT%{_sbindir}/{chgpasswd,grpconv,groupmems,logoutd,nologin,vipw,vigr}
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/*/man{1,3,5,8}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{chfn,chsh,groups,login,newgrp,su}*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/getspnam*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man5/{faillog,gshadow,passwd,shadow,suauth}*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man8/{chgpasswd,faillog,groupmems,grpconv,grpunconv,logoutd,nologin,vigr,vipw}*

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{newgrp,sg}
%{__rm} $RPM_BUILD_ROOT/etc/pam.d/*

for pamd in chage chpasswd groupadd groupdel groupmod useradd userdel usermod;
do
	install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/$pamd
done
for pamd in newusers passwd;
do
	install %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/$pamd
done

install -D %{SOURCE5} $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/lastlog.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/shadow ]; then
    %{_sbindir}/pwconv
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(4755,root,root) %{_bindir}/chage
%attr(4755,root,root) %{_bindir}/expiry
%attr(4755,root,root) %{_bindir}/gpasswd
%attr(4755,root,root) %{_bindir}/newgidmap
%attr(4755,root,root) %{_bindir}/newuidmap
%attr(4755,root,root) %{_bindir}/passwd
%attr(4755,root,root) %{_bindir}/sg
%attr(755,root,root) %{_bindir}/groups

%attr(755,root,root) %{_bindir}/lastlog
%{_prefix}/lib/tmpfiles.d/lastlog.conf

%attr(755,root,root) %{_sbindir}/chpasswd
%attr(755,root,root) %{_sbindir}/groupadd
%attr(755,root,root) %{_sbindir}/groupdel
%attr(755,root,root) %{_sbindir}/groupmod
%attr(755,root,root) %{_sbindir}/grpck
%attr(755,root,root) %{_sbindir}/grpunconv
%attr(755,root,root) %{_sbindir}/newusers
%attr(755,root,root) %{_sbindir}/pwck
%attr(755,root,root) %{_sbindir}/pwconv
%attr(755,root,root) %{_sbindir}/pwunconv
%attr(755,root,root) %{_sbindir}/useradd
%attr(755,root,root) %{_sbindir}/userdel
%attr(755,root,root) %{_sbindir}/usermod

%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %ghost %{_sysconfdir}/shadow
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default/useradd
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/login.defs
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/chage
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/chpasswd
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/groupadd
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/groupdel
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/groupmod
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/newusers
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/passwd
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/useradd
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/userdel
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/usermod

%{_mandir}/man1/chage.1*
%{_mandir}/man1/expiry.1*
%{_mandir}/man1/gpasswd.1*
%{_mandir}/man1/newgidmap.1.*
%{_mandir}/man1/newuidmap.1.*
%{_mandir}/man1/passwd.1*
%{_mandir}/man1/sg.1*
%{_mandir}/man3/shadow.3*
%{_mandir}/man5/login.defs.5*
%{_mandir}/man5/subgid.5.*
%{_mandir}/man5/subuid.5.*
%{_mandir}/man8/chpasswd.8*
%{_mandir}/man8/groupadd.8*
%{_mandir}/man8/groupdel.8*
%{_mandir}/man8/groupmod.8*
%{_mandir}/man8/grpck.8*
%{_mandir}/man8/lastlog.8*
%{_mandir}/man8/newusers.8*
%{_mandir}/man8/pwck.8*
%{_mandir}/man8/pwconv.8*
%{_mandir}/man8/pwunconv.8*
%{_mandir}/man8/useradd.8*
%{_mandir}/man8/userdel.8*
%{_mandir}/man8/usermod.8*

