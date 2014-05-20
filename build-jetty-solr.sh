#!/bin/sh
solrversion="4.8.1"
jettyversion="8.1.10.v20130312"
log4jextrasversion="1.1"

echo "Cleaning up....."
rm -rf BUILD BUILDROOT tmp || true
mkdir -p BUILD BUILDROOT RPMS SRPMS

echo "Collecting source files....."
if [ ! -f SOURCES/solr-$solrversion.tgz ];
then
    wget "http://archive.apache.org/dist/lucene/solr/$solrversion/solr-$solrversion.tgz" -O SOURCES/solr-$solrversion.tgz
    wget "http://archive.apache.org/dist/lucene/solr/$solrversion/solr-$solrversion.tgz.md5" -O SOURCES/solr-$solrversion.tgz.md5
fi

if [ ! -f SOURCES/jetty-distribution-$jettyversion.tar.gz ];
then
#    wget "http://download.eclipse.org/jetty/$jettyversion/dist/jetty-distribution-$jettyversion.tar.gz" -O SOURCES/jetty-distribution-$jettyversion.tar.gz
    wget "http://archive.eclipse.org/jetty/$jettyversion/dist/jetty-distribution-$jettyversion.tar.gz" -O SOURCES/jetty-distribution-$jettyversion.tar.gz
#    wget "http://download.eclipse.org/jetty/$jettyversion/dist/jetty-distribution-$jettyversion.tar.gz.md5" -O SOURCES/jetty-distribution-$jettyversion.tar.gz.md5
    wget "http://archive.eclipse.org/jetty/$jettyversion/dist/jetty-distribution-$jettyversion.tar.gz.md5" -O SOURCES/jetty-distribution-$jettyversion.tar.gz.md5
fi

if [ ! -f SOURCES/apache-log4j-extras-$log4jextrasversion.tar.gz ];
then
    wget "http://archive.apache.org/dist/logging/log4j/companions/extras/$log4jextrasversion/apache-log4j-extras-$log4jextrasversion.tar.gz" -O SOURCES/apache-log4j-extras-$log4jextrasversion.tar.gz
#    wget "http://www.us.apache.org/dist/logging/log4j/extras/$log4jextrasversion/apache-log4j-extras-$log4jextrasversion-bin.tar.gz" -O SOURCES/apache-log4j-extras-$log4jextrasversion-bin.tar.gz
    wget "http://archive.apache.org/dist/logging/log4j/companions/extras/$log4jextrasversion/apache-log4j-extras-$log4jextrasversion.tar.gz.md5" -O SOURCES/apache-log4j-extras-$log4jextrasversion.tar.gz.md5
#    wget "http://www.us.apache.org/dist/logging/log4j/extras/$log4jextrasversion/apache-log4j-extras-$log4jextrasversion-bin.tar.gz.md5" -O SOURCES/apache-log4j-extras-$log4jextrasversion-bin.tar.gz.md5
fi

echo "Assembling RPM....."
rpmbuild -ba --target=noarch --define="_topdir $PWD" --define="_tmppath $PWD/tmp" --define="sver $solrversion" --define="jver $jettyversion" --define="l4xver $log4jextrasversion" jetty-solr.spec

echo "DONE"
