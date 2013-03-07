%define _prefix /var/lib/solr
%define _logprefix /var/log/solr
%define _javaprefix /usr/lib/jvm

Name:			jetty-solr
Version:		%{ver}
Release:		18%{?dist}
Summary:		Solr
License:		GPL
URL:			http://lucene.apache.org/solr/
Source:			http://apache.mirrors.lucidnetworks.net/lucene/solr/%{version}/solr-%{version}.tgz
Source1:		jetty
Source2:		jetty-solr
Source3:		jetty.xml
BuildRoot:		%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
Requires:		java7 => 1:1.7.0

%description
%{summary}
%prep
%setup -q -n solr-%{version}


%build

%install
rm -rf $RPM_BUILD_ROOT
%__install -d "%{buildroot}%{_prefix}"
cp -p *.txt "%{buildroot}%{_prefix}"
cp -pr contrib "%{buildroot}%{_prefix}"
cp -pr dist "%{buildroot}%{_prefix}"
cp -pr docs "%{buildroot}%{_prefix}"
%__install -d "%{buildroot}%{_prefix}/jetty-solr"
cp -pr example/* "%{buildroot}%{_prefix}/jetty-solr"
cp -pr licenses "%{buildroot}%{_prefix}"
%__install -d "%{buildroot}%{_prefix}"/jetty-solr/solr/collection1/data
%__install -d "%{buildroot}%{_prefix}"/jetty-solr/solr/lib
%__install -d "%{buildroot}"/etc/default
%__install -d "%{buildroot}"/etc/init.d
%__install -d "%{buildroot}%{_logprefix}"
%__install -D -m0644  "%{SOURCE1}" %{buildroot}/etc/default/jetty
%__install -D -m0755  "%{SOURCE2}" %{buildroot}/etc/init.d/jetty-solr
%__install -D -m0644  "%{SOURCE3}" %{buildroot}%{_prefix}/jetty-solr/etc/jetty.xml
sed -i "s|JETTY_HOME_REPLACE|%{_prefix}|g" "%{buildroot}/etc/default/jetty"
sed -i "s|JETTY_LOGS_REPLACE|%{_logprefix}|g" "%{buildroot}/etc/default/jetty"
sed -i "s|JAVA_HOME_REPLACE|%{_javaprefix}|g" "%{buildroot}/etc/default/jetty"
sed -i "s|./logs/solr%u.log|%{_logprefix}/solr-%g.log|g" "%{buildroot}%{_prefix}/jetty-solr/etc/logging.properties"
sed -i "$ a\ \n# keep 5 files \njava.util.logging.FileHandler.count = 5\n \n# append to existing \njava.util.logging.FileHandler.append = true" "%{buildroot}%{_prefix}/jetty-solr/etc/logging.properties"
sed -i "s|./logs|%{_logprefix}|g" "%{buildroot}%{_prefix}/jetty-solr/etc/jetty.xml"

%clean
rm -rf $RPM_BUILD_ROOT



%files
%defattr(-,solr,solr,-)
%attr(0755,solr,solr) %dir %{_prefix}
%attr(0755,solr,solr) %dir %{_logprefix}
%doc
%{_prefix}/contrib
%{_prefix}/dist
%{_prefix}/docs
%{_prefix}/jetty-solr
%{_prefix}/licenses
%{_prefix}/CHANGES.txt
%{_prefix}/LICENSE.txt
%{_prefix}/NOTICE.txt
%{_prefix}/README.txt
%{_prefix}/SYSTEM_REQUIREMENTS.txt
%attr(0755,root,root) /etc/init.d/jetty-solr
%attr(0644,root,root) /etc/default/jetty

%pre
getent group solr >/dev/null || groupadd -r solr
getent passwd solr >/dev/null || \
    useradd -r -g solr -d %{_prefix}/jetty-solr -s /bin/bash \
    -c "Solr User" solr
exit 0

%post
chkconfig --add jetty-solr
echo "Installation complete."

%preun
if [ $1 = 0 ] ; then
   service jetty-solr stop >/dev/null 2>&1 || :
   chkconfig --del jetty-solr
fi

%postun
if [ "$1" -ge "1" ] ; then
   service jetty-solr restart >/dev/null 2>&1 || :
fi

%changelog
* Wed Feb 20 2013 Boogie Shafer <boogieshafer@yahoo.com>
- change path to data directory to place it under collection1
- adjust logging settings for solr

* Tue Feb 12 2013 Boogie Shafer <boogieshafer@yahoo.com>
- edits to configure jetty logging

* Tue Jan 29 2013 Boogie Shafer <boogieshafer@yahoo.com>
- edits for 4.1.0 solr using bundled jetty and zookeeper

* Tue Jan 18 2012 Jean-Francois Roche <jfroche@affinitic.be>
- Initial implementation
