%define _prefix /opt/solr
%define _logprefix /var/log/solr
%define _javaprefix /usr/lib/jvm
%define _collection_name collection1
%define _notify_email youremail@yourdomain.com

Name:			jetty-solr
Version:		%{sver}
Release:		3%{?dist}
Summary:		Solr
License:		GPL
URL:			http://lucene.apache.org/solr/
Source:			http://www.us.apache.org/dist/lucene/solr/%{version}/solr-%{version}.tgz
Source1:                http://download.eclipse.org/jetty/%{jver}/dist/jetty-distribution-%{jver}.tar.gz
Source2:                http://www.slf4j.org/dist/slf4j-%{slfver}.tar.gz
Source3:                http://logback.qos.ch/dist/logback-%{lver}.tar.gz
Source4:		etc.default.jetty
Source5:		logback.xml
Source6:		logback-access.xml
Source7:		jmx.passwd
Source8:		jmx.access
Source9:		java_error.sh
Source10:		java_oom.sh
Patch0:			jetty.xml-remove_requestlog_log4j.patch
Patch1:			solr.xml-add_lib_dir.patch
Patch2:			jetty-requestlog.xml-configure_logback.patch
Patch3:			jetty-jmx.xml-enable_rmi_tcp1099.patch
Patch4:			jetty.sh-redirect_init_output.patch
Patch5:			jetty.sh-config-init.patch
BuildRoot:		%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
Requires:		java7 => 1:1.7.0
Requires:		mailx

%description
%{summary}
%prep
%setup -q -n solr-%{version}
%patch0 -p0
%patch1 -p0
%setup -q -D -T -b 1 -n jetty-distribution-%{jver}
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%setup -q -D -T -b 2 -n slf4j-%{slfver}
%setup -q -D -T -b 3 -n logback-%{lver}

%build

%install
rm -rf $RPM_BUILD_ROOT
%__install -d "%{buildroot}%{_prefix}"
cp -p $RPM_BUILD_DIR/solr-%{version}/*.txt "%{buildroot}%{_prefix}"
cp -pr $RPM_BUILD_DIR/solr-%{version}/contrib "%{buildroot}%{_prefix}"
cp -pr $RPM_BUILD_DIR/solr-%{version}/dist "%{buildroot}%{_prefix}"
cp -pr $RPM_BUILD_DIR/solr-%{version}/docs "%{buildroot}%{_prefix}"
cp -pr $RPM_BUILD_DIR/solr-%{version}/licenses "%{buildroot}%{_prefix}"
%__install -d "%{buildroot}%{_prefix}/jetty-solr"
cp -pr $RPM_BUILD_DIR/solr-%{version}/example/* "%{buildroot}%{_prefix}/jetty-solr"
rm %{buildroot}%{_prefix}/jetty-solr/lib/ext/*.jar
cp -p $RPM_BUILD_DIR/slf4j-%{slfver}/slf4j-api-%{slfver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/slf4j-%{slfver}/jcl-over-slf4j-%{slfver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/slf4j-%{slfver}/jul-to-slf4j-%{slfver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/slf4j-%{slfver}/log4j-over-slf4j-%{slfver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/logback-%{lver}/logback-core-%{lver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/logback-%{lver}/logback-classic-%{lver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/logback-%{lver}/logback-access-%{lver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
%if "%{_collection_name}" == "collection1"
# no need to rename
%else
mv "%{buildroot}%{_prefix}/jetty-solr/solr/collection1" "%{buildroot}%{_prefix}/jetty-solr/solr/%{_collection_name}"
%endif
%__install -d "%{buildroot}%{_prefix}"/jetty-solr/solr/"%{_collection_name}"/data
%__install -d "%{buildroot}%{_prefix}"/jetty-solr/solr/lib
%__install -d "%{buildroot}"/etc/default
%__install -d "%{buildroot}"/etc/init.d
%__install -d "%{buildroot}%{_logprefix}"
%__install -D -m0644  "%{SOURCE4}" %{buildroot}/etc/default/jetty-solr
%__install -D -m0644  "%{SOURCE5}" %{buildroot}%{_prefix}/jetty-solr/resources/logback.xml
%__install -D -m0644  "%{SOURCE6}" %{buildroot}%{_prefix}/jetty-solr/resources/logback-access.xml
%__install -D -m0600  "%{SOURCE7}" %{buildroot}%{_prefix}/jetty-solr/resources/jmx.passwd
%__install -D -m0644  "%{SOURCE8}" %{buildroot}%{_prefix}/jetty-solr/resources/jmx.access
%__install -D -m0755  "%{SOURCE9}" %{buildroot}%{_prefix}/jetty-solr/etc/java_error.sh
%__install -D -m0755  "%{SOURCE10}" %{buildroot}%{_prefix}/jetty-solr/etc/java_oom.sh
%__install -D -m0755  $RPM_BUILD_DIR/jetty-distribution-%{jver}/bin/jetty.sh %{buildroot}/etc/init.d/jetty-solr
%__install -D -m0644  $RPM_BUILD_DIR/jetty-distribution-%{jver}/etc/jetty-requestlog.xml %{buildroot}%{_prefix}/jetty-solr/etc/jetty-requestlog.xml
%__install -D -m0644  $RPM_BUILD_DIR/jetty-distribution-%{jver}/etc/jetty-jmx.xml %{buildroot}%{_prefix}/jetty-solr/etc/jetty-jmx.xml
sed -i "s|JETTY_HOME_REPLACE|%{_prefix}|g" "%{buildroot}/etc/default/jetty-solr"
sed -i "s|JETTY_LOGS_REPLACE|%{_logprefix}|g" "%{buildroot}/etc/default/jetty-solr"
sed -i "s|JAVA_HOME_REPLACE|%{_javaprefix}|g" "%{buildroot}/etc/default/jetty-solr"
sed -i "s|./logs|%{_logprefix}|g" "%{buildroot}%{_prefix}/jetty-solr/etc/jetty-requestlog.xml"
sed -i "s|./logs|%{_logprefix}|g" "%{buildroot}%{_prefix}/jetty-solr/resources/logback.xml"
sed -i "s|./logs|%{_logprefix}|g" "%{buildroot}%{_prefix}/jetty-solr/resources/logback-access.xml"
sed -i "s|notify@domain.com|%{_notify_email}|g" "%{buildroot}%{_prefix}/jetty-solr/etc/java_error.sh"
sed -i "s|notify@domain.com|%{_notify_email}|g" "%{buildroot}%{_prefix}/jetty-solr/etc/java_oom.sh"
rm "%{buildroot}%{_prefix}/jetty-solr/etc/logging.properties"
rm "%{buildroot}%{_prefix}/jetty-solr/resources/log4j.properties"

%if "%{_collection_name}" == "collection1"
# no need to rename
%else
sed -i "s|collection1|%{_collection_name}|g" "%{buildroot}/etc/default/jetty-solr"
sed -i "s|collection1|%{_collection_name}|g" "%{buildroot}%{_prefix}/jetty-solr/solr/solr.xml"
%endif

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
%attr(0644,root,root) /etc/default/jetty-solr

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
* Thu May 9 2013 Scott Rossillo <scott@rossillo.net>
- Renamed /etc/default/jetty to /etc/default/jetty-solr

* Wed May 8 2013 Boogie Shafer <boogieshafer@yahoo.com>
- v4.3.0-2 tag
- remove solr bundled log4j 1.2.16 and slf4j 1.6.6 jars, replace with logback 1.0.12 and slf4j 1.7.5 jars
- fix jetty init script hangs for remote restarts via ssh

* Mon Apr 29 2013 Boogie Shafer <boogieshafer@yahoo.com>
- v4.2.1-6 tag
- move logging jars to ext dir to match future location in 4.3.x solr releases
- add GC printing options to startup
- add lib dir support for solr/lib area
- add recommeded java options from jetty's start.ini to etc/default/jetty. most commented out for now

* Mon Apr 22 2013 Boogie Shafer <boogieshafer@yahoo.com>
- v4.2.1-4 tag
- remove logging jars from solr.war
- adjust logback settings

* Fri Apr 19 2013 Boogie Shafer <boogieshafer@yahoo.com>
- v4.2.1-3 tag
- configure JMX support in jetty

* Thu Apr 18 2013 Boogie Shafer <boogieshafer@yahoo.com>
- v4.2.1-2 tag
- switch logging to logback

* Wed Apr 17 2013 Boogie Shafer <boogieshafer@yahoo.com>
- v4.2.1-1 tag
- make collection name configurable
- build using 4.2.1 solr binary release
- change default installation location to /opt/solr
- pull jetty init script and logging configs from jetty 8.x distribution

* Mon Mar 25 2013 Boogie Shafer <boogieshafer@yahoo.com>
- adjust version for 4.2.0 

* Wed Feb 20 2013 Boogie Shafer <boogieshafer@yahoo.com>
- change path to data directory to place it under collection1
- adjust logging settings for solr

* Tue Feb 12 2013 Boogie Shafer <boogieshafer@yahoo.com>
- edits to configure jetty logging

* Tue Jan 29 2013 Boogie Shafer <boogieshafer@yahoo.com>
- edits for 4.1.0 solr using bundled jetty and zookeeper

* Tue Jan 18 2012 Jean-Francois Roche <jfroche@affinitic.be>
- Initial implementation
