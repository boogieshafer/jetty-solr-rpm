#!/bin/sh
solrversion="4.10.3"
jettyversion="8.1.10.v20130312"
slf4jversion="1.7.10"
log4jversion="1.2.17"
log4jextrasversion="1.2.17"

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
    wget "http://archive.eclipse.org/jetty/$jettyversion/dist/jetty-distribution-$jettyversion.tar.gz" -O SOURCES/jetty-distribution-$jettyversion.tar.gz
    wget "http://archive.eclipse.org/jetty/$jettyversion/dist/jetty-distribution-$jettyversion.tar.gz.md5" -O SOURCES/jetty-distribution-$jettyversion.tar.gz.md5
fi

if [ ! -f SOURCES/slf4j-$slf4jversion.tar.gz ];
then
    wget "http://www.slf4j.org/dist/slf4j-$slf4jversion.tar.gz" -O SOURCES/slf4j-$slf4jversion.tar.gz
fi

if [ ! -f SOURCES/log4j-$log4jversion.tar.gz ];
then
    wget "http://archive.apache.org/dist/logging/log4j/$log4jversion/log4j-$log4jversion.tar.gz" -O SOURCES/log4j-$log4jversion.tar.gz
    wget "http://archive.apache.org/dist/logging/log4j/$log4jversion/log4j-$log4jversion.tar.gz.md5" -O SOURCES/log4j-$log4jversion.tar.gz.md5
fi

if [ ! -f SOURCES/apache-log4j-extras-$log4jextrasversion-bin.tar.gz ];
then
    wget "http://archive.apache.org/dist/logging/log4j/extras/$log4jextrasversion/apache-log4j-extras-$log4jextrasversion-bin.tar.gz" -O SOURCES/apache-log4j-extras-$log4jextrasversion-bin.tar.gz
    wget "http://archive.apache.org/dist/logging/log4j/extras/$log4jextrasversion/apache-log4j-extras-$log4jextrasversion-bin.tar.gz.md5" -O SOURCES/apache-log4j-extras-$log4jextrasversion-bin.tar.gz.md5
fi

echo "Assembling RPM....."
rpmbuild -ba --target=noarch --define="_topdir $PWD" --define="_tmppath $PWD/tmp" --define="sver $solrversion" --define="jver $jettyversion" --define="slfver $slf4jversion" --define="lver $log4jversion" --define="l4xver $log4jextrasversion" jetty-solr.spec

echo "DONE"
