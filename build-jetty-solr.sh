#!/bin/sh
solrversion="5.3.1"
jettyversion="9.2.11.v20150529"
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

if [ ! -f SOURCES/apache-log4j-extras-$log4jextrasversion-bin.tar.gz ];
then
    wget "http://archive.apache.org/dist/logging/log4j/extras/$log4jextrasversion/apache-log4j-extras-$log4jextrasversion-bin.tar.gz" -O SOURCES/apache-log4j-extras-$log4jextrasversion-bin.tar.gz
    wget "http://archive.apache.org/dist/logging/log4j/extras/$log4jextrasversion/apache-log4j-extras-$log4jextrasversion-bin.tar.gz.md5" -O SOURCES/apache-log4j-extras-$log4jextrasversion-bin.tar.gz.md5
fi

echo "Assembling RPM....."
rpmbuild -ba --target=x86_64 --define="_topdir $PWD" --define="_tmppath $PWD/tmp" --define="sver $solrversion" --define="jver $jettyversion" --define="l4xver $log4jextrasversion" jetty-solr.spec

echo "DONE"
