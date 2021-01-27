%global apiver          20170718
%global zendver         20170718
%global pdover          20170320
%global jsonver         1.6.0
%global _hardened_build 1
%global embed_version   7.2
%global mysql_sock      %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)
%global mysql_config    %{_libdir}/mysql/mysql_config

%undefine _strict_symbol_defs_build
%{!?runselftest: %global runselftest 1}

%{!?_httpd_mmn:         %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}

%global with_argon2     1
%global with_dtrace     1
%global with_libgd      1
%global with_zip        0
%global with_libzip     0
%global with_zts        0
%global with_firebird   0
%global with_imap       0
%global with_freetds    0
%global with_sodium     0
%global with_pspell     0
%global with_lmdb       0
%global upver           7.2.10

Name:          php
Version:       %{upver}%{?rcver:~%{rcver}}
Release:       9
Summary:       PHP scripting language for creating dynamic web sites
License:       PHP and Zend and BSD and MIT and ASL 1.0 and NCSA
URL:           http://www.php.net/
Source0:       http://www.php.net/distributions/php-%{upver}%{?rcver}.tar.xz
Source1:       php.conf
Source2:       php.ini
Source3:       macros.php
Source4:       php-fpm.conf
Source5:       php-fpm-www.conf
Source6:       php-fpm.service
Source7:       php-fpm.logrotate
Source9:       php.modconf
Source10:      php.ztsmodconf
Source12:      php-fpm.wants
Source13:      nginx-fpm.conf
Source14:      nginx-php.conf
Source50:      10-opcache.ini
Source51:      opcache-default.blacklist

Patch0001:     php-7.1.7-httpd.patch
Patch0002:     php-7.2.0-includedir.patch
Patch0003:     php-5.6.3-embed.patch
Patch0004:     php-5.3.0-recode.patch
Patch0005:     php-7.2.0-libdb.patch
Patch0006:     php-7.2.4-dlopen.patch
Patch0007:     php-7.2.3-systzdata-v16.patch
Patch0008:     php-5.4.0-phpize.patch
Patch0009:     php-7.2.3-ldap_r.patch
Patch0010:     php-7.2.4-fixheader.patch
Patch0011:     php-5.6.3-phpinfo.patch
Patch0012:     php-7.2.8-getallheaders.patch
Patch0013:     https://github.com/php/php-src/commit/cd0a37994e3cbf1f0aa1174155d3d662cefe2e7a.patch
Patch0014:     https://github.com/php/php-src/commit/be50a72715c141befe6f34ece660745da894aaf3.patch
Patch0015:     https://github.com/php/php-src/commit/c1729272b17a1fe893d1a54e423d3b71470f3ee8.patch
Patch0016:     php-5.6.3-datetests.patch

Patch6000:     CVE-2019-9021.patch
Patch6001:     CVE-2019-9022.patch
Patch6002:     CVE-2019-9023.patch
Patch6003:     CVE-2019-9024.patch
Patch6004:     CVE-2019-9637.patch
Patch6005:     CVE-2019-9638-CVE-2019-9639.patch
Patch6006:     CVE-2019-9640.patch
Patch6007:     php-CVE-2018-20783.patch
Patch6008:     php-CVE-2019-9641.patch
Patch6009:     CVE-2019-11034.patch
Patch6010:     CVE-2019-11035.patch
Patch6011:     CVE-2019-11036.patch
Patch6012:     CVE-2019-11041.patch
Patch6013:     CVE-2019-11042.patch
Patch6014:     CVE-2019-11043.patch
Patch6015:     CVE-2018-19935.patch
Patch6016:     CVE-2019-11045.patch
Patch6017:     CVE-2019-11046.patch
Patch6018:     CVE-2019-11050.patch
Patch6019:     CVE-2019-11047.patch
#git.php.net/?p=php-src.git;a=patch;h=336d2086a9189006909ae06c7e95902d7d5ff77e
Patch6020:     CVE-2018-19518.patch
#git.php.net/?p=php-src.git;a=patch;h=a15af81b5f0058e020eda0f109f51a3c863f5212
Patch6021:     CVE-2019-6977.patch
Patch6022:     CVE-2020-7064.patch
Patch6023:     CVE-2020-7066.patch
Patch6024:     CVE-2019-11048.patch
Patch6025:     CVE-2020-7068.patch
Patch6026:     CVE-2020-7063.patch
Patch6027:     backport-CVE-2020-7059-Fix-79099-OOB-read.patch
Patch6028:     backport-CVE-2020-7062-Fix-bug-79221.patch
Patch6029:     backport-CVE-2020-7071-Fix-bug-77423.patch

BuildRequires: bzip2-devel, curl-devel >= 7.9, httpd-devel >= 2.0.46-1, pam-devel, httpd-filesystem, nginx-filesystem
BuildRequires: libstdc++-devel, openssl-devel, sqlite-devel >= 3.6.0, zlib-devel, smtpdaemon, libedit-devel
BuildRequires: pcre-devel >= 6.6, bzip2, perl-interpreter, autoconf, automake, gcc, gcc-c++, libtool, libtool-ltdl-devel
%if %{with_libzip}
BuildRequires: libzip-devel >= 0.11
%endif
%if %{with_dtrace}
BuildRequires: systemtap-sdt-devel
%endif
%if %{with_argon2}
BuildRequires: libargon2-devel
%endif
%if %{with_zts}
Provides: php-zts = %{version}-%{release}, php-zts%{?_isa} = %{version}-%{release}
%endif

Requires: httpd-mmn = %{_httpd_mmn}, php-common%{?_isa} = %{version}-%{release}, php-cli%{?_isa} = %{version}-%{release}
Provides: mod_php = %{version}-%{release}, php(httpd)
#Recommends: php-fpm%{?_isa} = %{version}-%{release}
Requires(pre): httpd-filesystem

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.
The php package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

%package cli
Summary:  Command-line interface for PHP
License:  PHP and Zend and BSD and MIT and ASL 1.0 and NCSA and PostgreSQL
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}, php-cgi%{?_isa} = %{version}-%{release}, php-pcntl, php-pcntl%{?_isa}
Provides: php-readline, php-readline%{?_isa}

%description cli
The php-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php, and the CGI interface.

%package dbg
Summary:  The interactive PHP debugger
Requires: php-common%{?_isa} = %{version}-%{release}

%description dbg
The php-dbg package contains the interactive PHP debugger.

%package fpm
Summary:       PHP FastCGI Process Manager
BuildRequires: libacl-devel
Requires:      php-common%{?_isa} = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
BuildRequires: systemd-devel
%{?systemd_requires}
Requires(pre): httpd-filesystem
Requires:      httpd-filesystem >= 2.4.10, nginx-filesystem
Provides:      php(httpd)

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.

%package  common
Summary:   Common files for PHP
License:   PHP and BSD
Provides:  php(api) = %{apiver}-%{__isa_bits}, php(zend-abi) = %{zendver}-%{__isa_bits}
Provides:  php(language) = %{version}, php(language)%{?_isa} = %{version}, php-bz2, php-bz2%{?_isa}
Provides:  php-calendar, php-calendar%{?_isa}, php-core = %{version}, php-core%{?_isa} = %{version}
Provides:  php-ctype, php-ctype%{?_isa}, php-curl, php-curl%{?_isa}, php-date, php-date%{?_isa}
Provides:  bundled(timelib), php-exif, php-exif%{?_isa}, php-fileinfo, php-fileinfo%{?_isa}, bundled(libmagic) = 5.29
Provides:  php-filter, php-filter%{?_isa}, php-ftp, php-ftp%{?_isa}, php-gettext, php-gettext%{?_isa}
Provides:  php-hash, php-hash%{?_isa}, php-mhash = %{version}, php-mhash%{?_isa} = %{version}, php-zlib, php-zlib%{?_isa}
Provides:  php-iconv, php-iconv%{?_isa}, php-libxml, php-libxml%{?_isa}, php-openssl, php-openssl%{?_isa}
Provides:  php-phar, php-phar%{?_isa}, php-pcre, php-pcre%{?_isa}, php-reflection, php-reflection%{?_isa}
Provides:  php-session, php-session%{?_isa}, php-sockets, php-sockets%{?_isa}, php-spl, php-spl%{?_isa}
Provides:  php-standard = %{version}, php-standard%{?_isa} = %{version}, php-tokenizer, php-tokenizer%{?_isa}
%if %{with_zip}
Provides:  php-zip, php-zip%{?_isa}
Obsoletes: php-pecl-zip < 1.11
%endif

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Summary:   Files needed for building PHP extensions
Requires:  php-cli%{?_isa} = %{version}-%{release}, autoconf, automake, gcc, gcc-c++, libtool, pcre-devel%{?_isa}
Obsoletes: php-pecl-json-devel  < %{jsonver}, php-pecl-jsonc-devel < %{jsonver}
%if %{with_zts}
Provides:  php-zts-devel = %{version}-%{release}, php-zts-devel%{?_isa} = %{version}-%{release}
%endif

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package opcache
Summary:   The Zend OPcache
License:   PHP
Requires:  php-common%{?_isa} = %{version}-%{release}
Provides:  php-pecl-zendopcache = %{version}, php-pecl-zendopcache%{?_isa} = %{version}, php-pecl(opcache) = %{version}
Provides:  php-pecl(opcache)%{?_isa} = %{version}

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.

%if %{with_imap}
%package imap
Summary:       A module for PHP applications that use IMAP
License:       PHP
Requires:      php-common%{?_isa} = %{version}-%{release}
BuildRequires: krb5-devel, openssl-devel, libc-client-devel

%description imap
The php-imap module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail
messages on mail servers. PHP is an HTML-embedded scripting language.
%endif

%package ldap
Summary:       A module for PHP applications that use LDAP
License:       PHP
Requires:      php-common%{?_isa} = %{version}-%{release}
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%package pdo
Summary:  A database access abstraction module for PHP applications
License:  PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-pdo-abi  = %{pdover}-%{__isa_bits}, php(pdo-abi) = %{pdover}-%{__isa_bits}, php-sqlite3, php-sqlite3%{?_isa}
Provides: php-pdo_sqlite, php-pdo_sqlite%{?_isa}

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.

%package mysqlnd
Summary:  A module for PHP applications that use MySQL databases
License:  PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database, php-mysqli = %{version}-%{release}, php-mysqli%{?_isa} = %{version}-%{release},php-pdo_mysql
Provides: php-pdo_mysql%{?_isa}

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.
This package use the MySQL Native Driver

%package pgsql
Summary:       A PostgreSQL database module for PHP
License:       PHP
Requires:      php-pdo%{?_isa} = %{version}-%{release}
Provides:      php_database, php-pdo_pgsql, php-pdo_pgsql%{?_isa}
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

%description pgsql
The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary:  Modules for PHP script using system process interfaces
License:  PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-posix, php-posix%{?_isa}, php-shmop, php-shmop%{?_isa}, php-sysvsem, php-sysvsem%{?_isa}
Provides: php-sysvshm, php-sysvshm%{?_isa}, php-sysvmsg, php-sysvmsg%{?_isa}

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Summary:       A module for PHP applications that use ODBC databases
License:       PHP
Requires:      php-pdo%{?_isa} = %{version}-%{release}
Provides:      php_database, php-pdo_odbc, php-pdo_odbc%{?_isa}
BuildRequires: unixODBC-devel

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Summary:       A module for PHP applications that use the SOAP protocol
License:       PHP
Requires:      php-common%{?_isa} = %{version}-%{release}
BuildRequires: libxml2-devel

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%if %{with_firebird}
%package interbase
Summary:        A module for PHP applications that use Interbase/Firebird databases
License:        PHP
BuildRequires:  firebird-devel
Requires:       php-pdo%{?_isa} = %{version}-%{release}
Provides:       php_database, php-firebird, php-firebird%{?_isa}, php-pdo_firebird, php-pdo_firebird%{?_isa}

%description interbase
The php-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.
InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise.
Firebird is a commercially independent project of C and C++ programmers,
technical advisors and supporters developing and enhancing a multi-platform
relational database management system based on the source code released by
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.
%endif

%package snmp
Summary:       A module for PHP applications that query SNMP-managed devices
License:       PHP
Requires:      php-common%{?_isa} = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary:       A module for PHP applications which use XML
License:       PHP
Requires:      php-common%{?_isa} = %{version}-%{release}
Provides:      php-dom, php-dom%{?_isa}, php-domxml, php-domxml%{?_isa}, php-simplexml, php-simplexml%{?_isa}
Provides:      php-wddx, php-wddx%{?_isa}, php-xmlreader, php-xmlreader%{?_isa}, php-xmlwriter, php-xmlwriter%{?_isa}
Provides:      php-xsl, php-xsl%{?_isa}
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary:  A module for PHP applications which use the XML-RPC protocol
License:  PHP and BSD
Requires: php-xml%{?_isa} = %{version}-%{release}

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary:       A module for PHP applications which need multi-byte string handling
License:       PHP and LGPLv2 and OpenLDAP
BuildRequires: oniguruma-devel
Provides:      bundled(libmbfl) = 1.3.2
Requires:      php-common%{?_isa} = %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
%if %{with_libgd}
License: PHP
%else
License: PHP and BSD
%endif
Requires: php-common%{?_isa} = %{version}-%{release}
%if %{with_libgd}
BuildRequires: gd-devel >= 2.1.0
%else
BuildRequires: libjpeg-devel, libpng-devel, freetype-devel, libXpm-devel, libwebp-devel
Provides: bundled(gd) = 2.0.35
%endif

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
License: PHP and LGPLv2+
Requires: php-common%{?_isa} = %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package gmp
Summary: A module for PHP applications for using the GNU MP library
License: PHP
BuildRequires: gmp-devel
Requires: php-common%{?_isa} = %{version}-%{release}

%description gmp
These functions allow you to work with arbitrary-length integers
using the GNU MP library.

%package dba
Summary: A database abstraction layer module for PHP applications
License: PHP
BuildRequires: libdb-devel, tokyocabinet-devel
%if %{with_lmdb}
BuildRequires: lmdb-devel
%endif
Requires: php-common%{?_isa} = %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libtidy-devel

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%if %{with_freetds}
%package pdo-dblib
Summary: PDO driver Microsoft SQL Server and Sybase databases
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
BuildRequires: freetds-devel
Provides: php-pdo_dblib, php-pdo_dblib%{?_isa}

%description pdo-dblib
The php-pdo-dblib package contains a dynamic shared object
that implements the PHP Data Objects (PDO) interface to enable access from
PHP to Microsoft SQL Server and Sybase databases through the FreeTDS libary.
%endif

%package embedded
Summary: PHP library for embedding in applications
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-embedded-devel = %{version}-%{release}, php-embedded-devel%{?_isa} = %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%if %{with_pspell}
%package pspell
Summary: A module for PHP applications for using pspell interfaces
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.
%endif

%package recode
Summary: A module for PHP applications for using the recode library
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: recode-devel

%description recode
The php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libicu-devel >= 4.0

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Enchant spelling extension for PHP applications
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4

%description enchant
The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.

%package json
Summary:   JavaScript Object Notation extension for PHP
License:   PHP
Requires:  php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-json          < %{jsonver}
Obsoletes: php-pecl-jsonc         < %{jsonver}
Provides:  php-pecl(json) = %{jsonver}, php-pecl(json)%{?_isa} = %{jsonver}, php-pecl-json = %{jsonver}
Provides:  php-pecl-json%{?_isa}  = %{jsonver}

%description json
The php-json package provides an extension that will add
support for JavaScript Object Notation (JSON) to PHP.

%if %{with_sodium}
%package sodium
Summary: Wrapper for the Sodium cryptographic library
License: PHP
BuildRequires:  pkgconfig(libsodium) >= 1.0.9

Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-libsodium2 < 3
Provides:  php-pecl(libsodium) = %{version}, php-pecl(libsodium)%{?_isa} = %{version}

%description sodium
The php-sodium package provides a simple,
low-level PHP extension for the libsodium cryptographic library.
%endif

%package help
Summary: help

%description help
help

%prep
%autosetup -n php-%{upver}%{?rcver} -p1

cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
%if ! %{with_libgd}
cp ext/gd/libgd/README libgd_README
cp ext/gd/libgd/COPYING libgd_COPYING
%endif
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING
cp ext/date/lib/LICENSE.rst timelib_LICENSE

mkdir build-cgi build-apache build-embedded \
%if %{with_zts}
    build-zts build-ztscli \
%endif
    build-fpm

rm ext/date/tests/timezone_location_get.phpt
rm ext/date/tests/timezone_version_get.phpt
rm ext/date/tests/timezone_version_get_basic1.phpt
rm ext/sockets/tests/mcast_ipv?_recv.phpt
rm Zend/tests/bug54268.phpt
rm Zend/tests/bug68412.phpt

pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{upver}%{?rcver}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{upver}%{?rcver}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the %{jsonver} macro and rebuild.
   exit 1
fi

rm -f TSRM/tsrm_win32.h TSRM/tsrm_config.w32.h Zend/zend_config.w32.h ext/mysqlnd/config-win.h \
      ext/standard/winver.h main/win32_internal_function_disabled.h main/win95nt.h

find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

cp %{SOURCE50} 10-opcache.ini

%ifarch x86_64
sed -e '/opcache.huge_code_pages/s/0/1/' -i 10-opcache.ini
%endif

%build
export SOURCE_DATE_EPOCH=$(date +%s -r NEWS)

cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4

libtoolize --force --copy
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

touch configure.ac
./buildconf --force

CFLAGS=$(echo $RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign | sed 's/-mstackrealign//')
export CFLAGS

EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

build() {
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend

ln -sf ../configure
%configure \
    --cache-file=../config.cache --with-libdir=%{_lib} --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d --disable-debug --with-pic --disable-rpath \
    --without-pear --with-exec-dir=%{_bindir} --with-freetype-dir=%{_prefix} --with-png-dir=%{_prefix} \
    --with-xpm-dir=%{_prefix} --without-gdbm --with-jpeg-dir=%{_prefix} --with-openssl --with-system-ciphers \
    --with-pcre-regex=%{_prefix} --with-zlib --with-layout=GNU --with-kerberos --with-libxml-dir=%{_prefix} \
    --with-system-tzdata --with-mhash \
%if %{with_argon2}
    --with-password-argon2 \
%endif
%if %{with_dtrace}
    --enable-dtrace \
%endif
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

pushd build-cgi

build --libdir=%{_libdir}/php --enable-pcntl --enable-opcache --enable-opcache-file --enable-phpdbg \
%if %{with_imap}
      --with-imap=shared --with-imap-ssl \
%endif
      --enable-mbstring=shared --with-onig=%{_prefix} --enable-mbregex \
%if %{with_libgd}
      --with-gd=shared,%{_prefix} \
%else
      --with-gd=shared \
%endif
      --with-gmp=shared --enable-calendar=shared --enable-bcmath=shared --with-bz2=shared --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} --with-tcadb=%{_prefix} \
%if %{with_lmdb}
      --with-lmdb=%{_prefix} \
%endif
      --enable-exif=shared --enable-ftp=shared --with-gettext=shared --with-iconv=shared --enable-sockets=shared \
      --enable-tokenizer=shared --with-xmlrpc=shared --with-ldap=shared --with-ldap-sasl --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd --with-mysql-sock=%{mysql_sock} \
%if %{with_firebird}
      --with-interbase=shared --with-pdo-firebird=shared \
%endif
      --enable-dom=shared --with-pgsql=shared --enable-simplexml=shared --enable-xml=shared --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} --enable-soap=shared --with-xsl=shared,%{_prefix} --enable-xmlreader=shared \
      --enable-xmlwriter=shared --with-curl=shared,%{_prefix} --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} --with-pdo-mysql=shared,mysqlnd --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
%if %{with_freetds}
      --with-pdo-dblib=shared,%{_prefix} \
%endif
      --with-sqlite3=shared,%{_prefix} --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%if %{with_libzip}
      --with-libzip \
%endif
%endif
      --without-readline --with-libedit \
%if %{with_pspell}
      --with-pspell=shared \
%endif
      --enable-phar=shared --with-tidy=shared,%{_prefix} --enable-sysvmsg=shared --enable-sysvshm=shared \
      --enable-sysvsem=shared --enable-shmop=shared --enable-posix=shared --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
%if %{with_sodium}
      --with-sodium=shared \
%else
      --without-sodium \
%endif
      --enable-intl=shared --with-icu-dir=%{_prefix} --with-enchant=shared,%{_prefix} --with-recode=shared,%{_prefix}
popd

without_shared="--without-gd --disable-dom --disable-dba --without-unixODBC --disable-opcache --disable-json \
      --disable-xmlreader --disable-xmlwriter --without-sodium --without-sqlite3 --disable-phar --disable-fileinfo \
      --without-pspell --disable-wddx --without-curl --disable-posix --disable-xml --disable-simplexml --disable-exif \
      --without-gettext --without-iconv --disable-ftp --without-bz2 --disable-ctype --disable-shmop --disable-sockets \
      --disable-tokenizer --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

pushd build-apache
build --with-apxs2=%{_httpd_apxs} --libdir=%{_libdir}/php --without-mysqli --disable-pdo \
      ${without_shared}
popd

pushd build-fpm
build --enable-fpm --with-fpm-acl --with-fpm-systemd --libdir=%{_libdir}/php --without-mysqli --disable-pdo \
      ${without_shared}
popd

pushd build-embedded
build --enable-embed --without-mysqli --disable-pdo \
      ${without_shared}
popd

%if %{with_zts}
pushd build-ztscli

EXTENSION_DIR=%{_libdir}/php-zts/modules
build --includedir=%{_includedir}/php-zts --libdir=%{_libdir}/php-zts --enable-maintainer-zts --program-prefix=zts- \
      --disable-cgi --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d --enable-pcntl --enable-opcache \
      --enable-opcache-file \
%if %{with_imap}
      --with-imap=shared --with-imap-ssl \
%endif
      --enable-mbstring=shared --with-onig=%{_prefix} --enable-mbregex \
%if %{with_libgd}
      --with-gd=shared,%{_prefix} \
%else
      --with-gd=shared \
%endif
      --with-gmp=shared --enable-calendar=shared --enable-bcmath=shared --with-bz2=shared --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} --with-tcadb=%{_prefix} \
%if %{with_lmdb}
      --with-lmdb=%{_prefix} \
%endif
      --with-gettext=shared --with-iconv=shared --enable-sockets=shared --enable-tokenizer=shared --enable-exif=shared \
      --enable-ftp=shared --with-xmlrpc=shared --with-ldap=shared --with-ldap-sasl --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd --with-mysql-sock=%{mysql_sock} --enable-mysqlnd-threading \
%if %{with_firebird}
      --with-interbase=shared --with-pdo-firebird=shared \
%endif
      --enable-dom=shared --with-pgsql=shared --enable-simplexml=shared --enable-xml=shared --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} --enable-soap=shared --with-xsl=shared,%{_prefix} --enable-xmlreader=shared \
      --enable-xmlwriter=shared --with-curl=shared,%{_prefix} --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} --with-pdo-mysql=shared,mysqlnd --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
%if %{with_freetds}
      --with-pdo-dblib=shared,%{_prefix} \
%endif
      --with-sqlite3=shared,%{_prefix} --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%if %{with_libzip}
      --with-libzip \
%endif
%endif
      --without-readline --with-libedit \
%if %{with_pspell}
      --with-pspell=shared \
%endif
      --enable-phar=shared --with-tidy=shared,%{_prefix} --enable-sysvmsg=shared --enable-sysvshm=shared \
      --enable-sysvsem=shared --enable-shmop=shared --enable-posix=shared --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
%if %{with_sodium}
      --with-sodium=shared \
%else
      --without-sodium \
%endif
      --enable-intl=shared --with-icu-dir=%{_prefix} --with-enchant=shared,%{_prefix} --with-recode=shared,%{_prefix}
popd

pushd build-zts
build --with-apxs2=%{_httpd_apxs} --includedir=%{_includedir}/php-zts --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d --without-mysqli --disable-pdo \
      ${without_shared}
popd
%endif

%check
%if %runselftest
cd build-apache

export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
export SKIP_IO_CAPTURE_TESTS=1
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      cat "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
%if %{with_zts}
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

make -C build-embedded install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT

make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -m 644 php.gif $RPM_BUILD_ROOT%{_httpd_contentdir}/icons/php.gif
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/php
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}

%if %{with_zts}
install -m 755 build-zts/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp7-zts.so
%endif

install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%if %{with_zts}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%endif
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%if %{with_zts}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php
install -m 755 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/peclxml
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/session
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{_sharedstatedir}/php/opcache
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/pecl
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/tests/pecl
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
install -m 755 -d $RPM_BUILD_ROOT/run/php-fpm
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf.default .
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/php-fpm.service.d
install -Dm 644 %{SOURCE6}  $RPM_BUILD_ROOT%{_unitdir}/php-fpm.service
install -Dm 644 %{SOURCE12} $RPM_BUILD_ROOT%{_unitdir}/httpd.service.d/php-fpm.conf
install -Dm 644 %{SOURCE12} $RPM_BUILD_ROOT%{_unitdir}/nginx.service.d/php-fpm.conf
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm
install -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
install -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/php.conf

for mod in pgsql odbc ldap snmp xmlrpc \
%if %{with_imap}
    imap \
%endif
    json \
    mysqlnd mysqli pdo_mysql \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    simplexml bz2 calendar ctype exif ftp gettext gmp iconv \
    sockets tokenizer opcache \
    pdo pdo_pgsql pdo_odbc pdo_sqlite \
%if %{with_zip}
    zip \
%endif
%if %{with_firebird}
    interbase pdo_firebird \
%endif
    sqlite3 \
    enchant phar fileinfo intl \
    tidy \
%if %{with_freetds}
    pdo_dblib \
%endif
%if %{with_pspell}
    pspell \
%endif
    curl wddx \
%if %{with_sodium}
    sodium \
%endif
    posix shmop sysvshm sysvsem sysvmsg recode xml \
    ; do
    case $mod in
      opcache)
        ini=10-${mod}.ini;;
      pdo_*|mysqli|wddx|xmlreader|xmlrpc)
        ini=30-${mod}.ini;;
      *)
        ini=20-${mod}.ini;;
    esac
    if [ -f ${ini} ]; then
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini}
%if %{with_zts}
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini}
%endif
    else
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}
EOF
%if %{with_zts}
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}
EOF
%endif
    fi
    cat > files.${mod} <<EOF
%{_libdir}/php/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php.d/${ini}
%if %{with_zts}
%{_libdir}/php-zts/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php-zts.d/${ini}
%endif
EOF
done

cat files.dom files.xsl files.xml{reader,writer} files.wddx \
    files.simplexml >> files.xml

cat files.mysqli \
    files.pdo_mysql \
    >> files.mysqlnd

cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
%if %{with_firebird}
cat files.pdo_firebird >> files.interbase
%endif

cat files.shmop files.sysv* files.posix > files.process
cat files.pdo_sqlite >> files.pdo
cat files.sqlite3 >> files.pdo
cat files.curl files.phar files.fileinfo \
    files.exif files.gettext files.iconv files.calendar \
    files.ftp files.bz2 files.ctype files.sockets \
    files.tokenizer > files.common
%if %{with_zip}
cat files.zip >> files.common
%endif

install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with_zts}
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/opcache-default.blacklist
sed -e '/blacklist_filename/s/php.d/php-zts.d/' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/10-opcache.ini
%endif

sed -e "s/@PHP_APIVER@/%{apiver}-%{__isa_bits}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}-%{__isa_bits}/" \
    -e "s/@PHP_PDOVER@/%{pdover}-%{__isa_bits}/" \
    -e "s/@PHP_VERSION@/%{upver}/" \
%if ! %{with_zts}
    -e "/zts/d" \
%endif
    < %{SOURCE3} > macros.php
install -m 644 -D macros.php \
           $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.php

rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp7.la

rm -f README.{Zeus,QNX,CVS-RULES}

%post fpm
%systemd_post php-fpm.service

%preun fpm
%systemd_preun php-fpm.service

%transfiletriggerin fpm -- %{_sysconfdir}/php-fpm.d %{_sysconfdir}/php.d
systemctl try-restart php-fpm.service >/dev/null 2>&1 || :

%files
%{_httpd_moddir}/libphp7.so
%if %{with_zts}
%{_httpd_moddir}/libphp7-zts.so
%endif
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/session
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/wsdlcache
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/opcache
%config(noreplace) %{_httpd_confdir}/php.conf
%config(noreplace) %{_httpd_modconfdir}/15-php.conf
%{_httpd_contentdir}/icons/php.gif

%files common -f files.common
%license LICENSE TSRM_LICENSE
%license libmagic_LICENSE
%license phar_LICENSE
%license timelib_LICENSE
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%if %{with_zts}
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php-zts
%dir %{_libdir}/php-zts/modules
%endif
%dir %{_sharedstatedir}/php
%dir %{_sharedstatedir}/php/peclxml
%dir %{_datadir}/php
%dir %{_docdir}/pecl
%dir %{_datadir}/tests
%dir %{_datadir}/tests/pecl

%files cli
%{_bindir}/php
%if %{with_zts}
%{_bindir}/zts-php
%endif
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
%{_bindir}/phpize

%files dbg
%{_bindir}/phpdbg
%if %{with_zts}
%{_bindir}/zts-phpdbg
%endif

%files fpm
%license fpm_LICENSE
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/session
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/wsdlcache
%attr(0770,root,apache) %dir %{_sharedstatedir}/php/opcache
%config(noreplace) %{_httpd_confdir}/php.conf
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%config(noreplace) %{_sysconfdir}/nginx/conf.d/php-fpm.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/php.conf
%{_unitdir}/php-fpm.service
%{_unitdir}/httpd.service.d/php-fpm.conf
%{_unitdir}/nginx.service.d/php-fpm.conf
%{_sbindir}/php-fpm
%dir %{_sysconfdir}/systemd/system/php-fpm.service.d
%dir %{_sysconfdir}/php-fpm.d
%attr(770,apache,root) %dir %{_localstatedir}/log/php-fpm
%dir %ghost /run/php-fpm
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html

%files devel
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%if %{with_zts}
%{_bindir}/zts-php-config
%{_bindir}/zts-phpize
%{_includedir}/php-zts
%{_libdir}/php-zts/build
%endif
%{_rpmconfigdir}/macros.d/macros.php

%files embedded
%{_libdir}/libphp7.so
%{_libdir}/libphp7-%{embed_version}.so

%files pgsql -f files.pgsql
%files odbc -f files.odbc
%if %{with_imap}
%files imap -f files.imap
%endif
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%license libmbfl_LICENSE
%license ucgendat_LICENSE
%files gd -f files.gd
%if ! %{with_libgd}
%license libgd_README
%license libgd_COPYING
%endif
%files soap -f files.soap
%files bcmath -f files.bcmath
%license libbcmath_COPYING
%files gmp -f files.gmp
%files dba -f files.dba
%files pdo -f files.pdo
%files tidy -f files.tidy
%if %{with_freetds}
%files pdo-dblib -f files.pdo_dblib
%endif
%if %{with_pspell}
%files pspell -f files.pspell
%endif
%files intl -f files.intl
%files process -f files.process
%files recode -f files.recode
%if %{with_firebird}
%files interbase -f files.interbase
%endif
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd
%files opcache -f files.opcache
%config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with_zts}
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%endif
%files json -f files.json
%if %{with_sodium}
%files sodium -f files.sodium
%endif

%files help
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS NEWS README* sapi/cgi/README* sapi/cli/README sapi/phpdbg/{README.md,CREDITS}
%doc php-fpm.conf.default www.conf.default php.ini-* 
%{_mandir}/*


%changelog
* Wed Jan 20 2021 Hugel <gengqihu1@huawei.com> - 7.2.10-9
- Fix CVE-2020-7062 CVE-2020-7071

* Fri Jan 15 2021 panxiaohe <panxiaohe@huawei.com> - 7.2.10-8
- Fix CVE-2020-7059

* Thu Dec 17 2020 wangchen <wangchen137@huawei.com> - 7.2.10-7
- Fix CVE-2020-7063

* Mon Sep 21 2020 shaoqiang kang <kangshaoqiang1@huawei.com> - 7.2.10-6
- Fix CVE-2020-7068

* Tue Jul 21 2020 wangyue <wangyue92@huawei.com> - 7.2.10-5
- Type:cves
- ID:CVE-2019-11048
- SUG:restart
- DESC:fix CVE-2019-11048

* Fri Apr 24 2020 openEuler Buildteam <buildteam@openeuler.org> - 7.2.10-4
- Type:cves
- ID:CVE-2020-7064 CVE-2020-7066
- SUG:restart
- DESC:fix CVE-2020-7064 CVE-2020-7066

* Mon Mar 16 2020 shijian <shijian16@huawei.com> - 7.2.10-3
- Type:cves
- ID:CVE-2018-19518 CVE-2019-6977
- SUG:restart
- DESC:fix CVE-2018-19518 CVE-2019-6977

* Thu Mar 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 7.2.10-2
- Add CVE patches

* Fri Feb 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 7.2.10-1
- Package init
