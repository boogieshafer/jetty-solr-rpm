%define _prefix /opt/solr
%define _logprefix /var/log/solr
%define _javaprefix /usr/lib/jvm
%define _collection_name core01
%define _core02_name core02
%define _core02_enabled false
%define _notify_email youremail@yourdomain.com
%define _solr_gid 8983
%define _solr_uid 8983
# Prevent brp-java-repack-jars from being run.
%define __jar_repack %{nil}

Name:			jetty-solr
Version:		%{sver}
Release:		1log4j%{?dist}
Summary:		Solr
License:		GPL
URL:			http://lucene.apache.org/solr/
Source:			http://www.us.apache.org/dist/lucene/solr/%{version}/solr-%{version}.tgz
Source1:                http://download.eclipse.org/jetty/%{jver}/dist/jetty-distribution-%{jver}.tar.gz
Source2:		slf4j-%{slfver}.tar.gz
Source3:		log4j-%{lver}.tar.gz
Source4:		apache-log4j-extras-%{l4xver}-bin.tar.gz
Source5:		etc.default.jetty-solr
Source6:		jmx.passwd
Source7:		jmx.access
Source8:		java_error.sh
Source9:		java_oom.sh
Source10:		log4j.xml
Patch0:			jetty.xml-remove_requestlog.patch
Patch1:			jetty-requestlog.xml-configure_filenaming.patch
Patch2:			jetty-jmx.xml-enable_rmi_tcp1099.patch
Patch3:			jetty.sh-redirect_init_output.patch
Patch4:			jetty.sh-use_etc_default_jetty-solr.patch 
BuildRoot:		%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
Requires:		java7 => 1:1.7.0
Requires:		mailx

%description
RPM build for Solr using builtin Jetty
https://github.com/boogieshafer/jetty-solr-rpm

%prep
%setup -q -n solr-%{version}
rm -r example/example-DIH
rm -r example/exampledocs
rm -r example/example-schemaless
rm -r example/multicore
rm example/lib/ext/*.jar
rm example/resources/log4j.properties
rm example/scripts/cloud-scripts/zkcli.bat
rm dist/solr-%{version}.war
mkdir -p example/solr/%{_core02_name}
cp -R example/solr/collection1/conf example/solr/%{_core02_name}/conf
mv example/solr/%{_core02_name}/conf/schema.xml example/solr/%{_core02_name}/conf/schema-%{_core02_name}.xml
mv example/solr/%{_core02_name}/conf/solrconfig.xml example/solr/%{_core02_name}/conf/solrconfig-%{_core02_name}.xml
echo "name="%{_core02_name} > example/solr/%{_core02_name}/core.properties.unloaded
echo "schema=schema-"%{_core02_name}".xml" >> example/solr/%{_core02_name}/core.properties.unloaded
echo "config=solrconfig-"%{_core02_name}".xml" >> example/solr/%{_core02_name}/core.properties.unloaded
echo "loadOnStartup="%{_core02_enabled} >> example/solr/%{_core02_name}/core.properties.unloaded
%if "%{_core02_enabled}" == "true"
mv example/solr/%{_core02_name}/core.properties.unloaded example/solr/%{_core02_name}/core.properties
%else
# no need to rename
%endif
%patch0 -p0

%setup -q -D -T -b 1 -n jetty-distribution-%{jver}
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0

%setup -q -D -T -b 2 -n slf4j-%{slfver}

%setup -q -D -T -b 3 -n apache-log4j-%{lver}

%setup -q -D -T -b 4 -n apache-log4j-extras-%{l4xver}

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
mkdir -p "%{buildroot}%{_prefix}/jetty-solr/.java/.systemPrefs"
cp -p $RPM_BUILD_DIR/slf4j-%{slfver}/slf4j-api-%{slfver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/slf4j-%{slfver}/jcl-over-slf4j-%{slfver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/slf4j-%{slfver}/jul-to-slf4j-%{slfver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/slf4j-%{slfver}/slf4j-log4j12-%{slfver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/apache-log4j-%{lver}/log4j-%{lver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
cp -p $RPM_BUILD_DIR/apache-log4j-extras-%{l4xver}/apache-log4j-extras-%{l4xver}.jar "%{buildroot}%{_prefix}/jetty-solr/lib/ext"
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
%__install -D -m0644  "%{SOURCE5}" %{buildroot}/etc/default/jetty-solr
%__install -D -m0600  "%{SOURCE6}" %{buildroot}%{_prefix}/jetty-solr/resources/jmx.passwd
%__install -D -m0644  "%{SOURCE7}" %{buildroot}%{_prefix}/jetty-solr/resources/jmx.access
%__install -D -m0755  "%{SOURCE8}" %{buildroot}%{_prefix}/jetty-solr/etc/java_error.sh
%__install -D -m0755  "%{SOURCE9}" %{buildroot}%{_prefix}/jetty-solr/etc/java_oom.sh
%__install -D -m0644  "%{SOURCE10}" %{buildroot}%{_prefix}/jetty-solr/resources/log4j.xml
%__install -D -m0755  $RPM_BUILD_DIR/jetty-distribution-%{jver}/bin/jetty.sh %{buildroot}/etc/init.d/jetty-solr
%__install -D -m0644  $RPM_BUILD_DIR/jetty-distribution-%{jver}/etc/jetty-requestlog.xml %{buildroot}%{_prefix}/jetty-solr/etc/jetty-requestlog.xml
%__install -D -m0644  $RPM_BUILD_DIR/jetty-distribution-%{jver}/etc/jetty-jmx.xml %{buildroot}%{_prefix}/jetty-solr/etc/jetty-jmx.xml
sed -i "s|JETTY_HOME_REPLACE|%{_prefix}|g" "%{buildroot}/etc/default/jetty-solr"
sed -i "s|JETTY_LOGS_REPLACE|%{_logprefix}|g" "%{buildroot}/etc/default/jetty-solr"
sed -i "s|JAVA_HOME_REPLACE|%{_javaprefix}|g" "%{buildroot}/etc/default/jetty-solr"
sed -i "s|./logs|%{_logprefix}|g" "%{buildroot}%{_prefix}/jetty-solr/etc/jetty-requestlog.xml"
sed -i "s|notify@domain.com|%{_notify_email}|g" "%{buildroot}%{_prefix}/jetty-solr/etc/java_error.sh"
sed -i "s|notify@domain.com|%{_notify_email}|g" "%{buildroot}%{_prefix}/jetty-solr/etc/java_oom.sh"
sed -i "s|./logs|%{_logprefix}|g" "%{buildroot}%{_prefix}/jetty-solr/resources/log4j.xml"

%if "%{_collection_name}" == "collection1"
# no need to rename
%else
sed -i "s|collection1|%{_collection_name}|g" "%{buildroot}%{_prefix}/jetty-solr/solr/%{_collection_name}/core.properties"
%endif

%clean
# rm -rf $RPM_BUILD_ROOT



%files
%defattr(-,solr,solr,-)
%attr(0755,solr,solr) %dir %{_prefix}
%if "%{_logprefix}" == "%{_prefix}/jetty-solr/logs"
# do nothing
%else
%attr(0755,solr,solr) %dir %{_logprefix}
%endif
%{_prefix}/contrib
%{_prefix}/dist
%doc %{_prefix}/docs
%{_prefix}/jetty-solr
%doc %{_prefix}/licenses
%doc %{_prefix}/CHANGES.txt
%doc %{_prefix}/LICENSE.txt
%doc %{_prefix}/LUCENE_CHANGES.txt
%doc %{_prefix}/NOTICE.txt
%doc %{_prefix}/README.txt
%doc %{_prefix}/SYSTEM_REQUIREMENTS.txt
%attr(0755,root,root) /etc/init.d/jetty-solr
%config %attr(0644,root,root) /etc/default/jetty-solr

%pre
mkdir -p %{_prefix}
getent group solr >/dev/null || groupadd -g %{_solr_gid} solr
getent passwd solr >/dev/null || \
    useradd -g %{_solr_gid} -u %{_solr_uid} -d %{_prefix}/jetty-solr -s /bin/bash \
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

* Thu Nov 06 2014 Boogie Shafer <boogieshafer@yahoo.com>
- 4.10.2-1log4j
- update for 4.10.2

* Tue May 20 2014 Boogie Shafer <boogieshafer@yahoo.com>
- 4.8.1-1log4j

* Sat Apr 13 2014 Boogie Shafer <boogieshafer@yahoo.com>
- 4.7.1-1log4j
- remove the dist slf4j and log4j and upgrade to current releases

* Wed Apr 02 2014 Boogie Shafer <boogieshafer@yahoo.com>
- 4.7.1-1
- update for solr 4.7.x
- disable jar repack during rpmbuild process

* Fri Nov 15 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.5.1-4
- add lib4j extras to enable compression on rotation 
- make name of second core more obvious
- clean up log naming
- remove extra solr war file from rpm

* Fri Nov 15 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.5.1-3
- replace log4j.properties with log4j.xml
- fix problem with SOLR GUI logging by sending solr logs to root logger
- create second, disabled core02
- fix URL to archived jetty build

* Thu Nov 14 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.5.1-1
- update for solr 4.5.1 release

* Wed Jul 31 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.4.0-1
- update for solr 4.4.0 release
- remove logback and slf4j updates in favor of bundled log4j

* Thu Jun 20 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.3.1-1
- changed java GC to CMS

* Fri Jun 14 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.3.0-4
- rename /etc/default/jetty to /etc/default/jetty-solr

* Thu May 14 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.3.0-3
- upgrade logback components to 1.0.13 release
- add java option for gc.log rotation

* Wed May 8 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.3.0-2
- remove solr bundled log4j 1.2.16 and slf4j 1.6.6 jars, replace with logback 1.0.12 and slf4j 1.7.5 jars
- fix jetty init script hangs for remote restarts via ssh

* Mon Apr 29 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.2.1-6
- move logging jars to ext dir to match future location in 4.3.x solr releases
- add GC printing options to startup
- add lib dir support for solr/lib area
- add recommeded java options from jetty's start.ini to etc/default/jetty. most commented out for now

* Mon Apr 22 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.2.1-4
- remove logging jars from solr.war
- adjust logback settings

* Fri Apr 19 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.2.1-3
- configure JMX support in jetty

* Thu Apr 18 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.2.1-2
- switch logging to logback

* Wed Apr 17 2013 Boogie Shafer <boogieshafer@yahoo.com>
- 4.2.1-1
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
