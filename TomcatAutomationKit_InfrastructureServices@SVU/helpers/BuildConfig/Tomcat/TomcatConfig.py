# Default constants for the generic installation of `TOMCAT` on production systems.
# Please alter the below configurations to suit your environment needs.
BASE_URL           = 'https://tomcat.apache.org'
ARCHIVE_URL        = 'http://archive.apache.org/dist'
PACKAGE_EXTENSION  = '.tar.gz'

# `TOMCAT` version configuration.
TOMCAT_MAJOR_VERSION  = '8' # X.y.z

# Locate the latest `TOMCAT::PACKAGE::DOWNLOADS` link from the Apache `TOMCAT` Downloads Page.
# The latest version being downloaded is relative to the `VERSION` configuration option that is
# enabled and fed to the automation software.
VERSION_DOWNLOAD_URL     = BASE_URL + '/download-' + TOMCAT_MAJOR_VERSION + '0.cgi'
VERSION_DOWNLOAD_PATTERN = '/tomcat/tomcat-[0-9]+/v[0-9]+\.[0-9]+\.[0-9]+(.+)?/bin' + \
							'/apache-tomcat-[0-9]+\.[0-9]+\.[0-9]+([A-Z][0-9]+)?' + \
							PACKAGE_EXTENSION

# `TOMCAT` build environment details.
ENVIRONMENT = {
	'BUILD_TARGET': '__TOMCAT__',
	'DEPENDENCY'  : ['Java', 'Tomcat'],
	'BUILD_TYPE'  : 'Generic [Automated]',
	'DESCRIPTION' : "Build Automation for setting up `TOMCAT` Instances.",
	'OS_SUPPORT'  : {
						'Unix':    ['Solaris'],
						'Linux':   ['Ubuntu', 'RHEL'],
						'Windows': ['Server 2008 (Standard | R2)', 'Server 2012 (Standard | R2)']
					}
}

# `THREAD` name that executes the download logic for `TOMCAT`.
TOMCAT_DOWNLOADER_THREAD_NAME = 'TOMCAT::DOWNLOADER::THREAD'

# `THREAD` name that executes the untar logic for `TOMCAT`.
TOMCAT_UNTAR_THREAD_NAME      = 'TOMCAT::UNTAR::THREAD'

# Package type name convention to
# be followed within the `TAR` final
# extract directory.
# Below is the `TAR` extraction directory for `TOMCAT`.
TOMCAT_TAR_EXTRACT_PACKAGE_TYPE_LOCATION = 'Tomcat/'

# Location to keep the `TOMCAT` binary.
# Change this location parameter to
# suit your environment standards.
TOMCAT_BINARY_LOCATION = '/opt/tomcat/'

# `TOMCAT` profile file name.
TOMCAT_PROFILE_FILE_NAME = 'tomcat_profile.txt'

# The below location defines where the `TOMCAT` profile resides.
# Change the below to suit according to your environment needs.
# TOMCAT_PROFILE_FILE_LOCATION = TOMCAT_BINARY_LOCATION + TOMCAT_PROFILE_FILE_NAME

# `TOMCAT` component name to be used
# program wide.
# Used to reference or label `TOMCAT`
# related nuances.
TOMCAT_COMPONENT_NAME  = 'Tomcat'

# `TOMCAT_TAR` component name to be used
# program wide.
# This is the identifier returned by
# the DownloadManager Module.
# It references the `TOMCAT_TAR` package.
TOMCAT_TAR_COMPONENT_NAME = 'Tomcat_Tar'

# The `TOMCAT_TAR` extract name to be referenced after the
# untarring operation.
TOMCAT_TAR_EXTRACT_COMPONENT_NAME = 'Tomcat_Tar_ExtractName'