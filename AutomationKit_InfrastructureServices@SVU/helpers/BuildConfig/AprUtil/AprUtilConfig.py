# The below module holds the `BASE_EXTRACT_DIRECTORY` location information.
import helpers.BuildConfig.Untar.UntarConfig

# The below module provides the `HTTPD` Extract's Package location.
import helpers.BuildConfig.Httpd.HttpdConfig

# Default constants for the generic installation of `APR-UTIL` on production systems.
# Please alter the below configurations to suit your environment needs.
BASE_URL           = 'https://apr.apache.org/download.cgi'
ARCHIVE_URL        = 'http://archive.apache.org/dist/apr'
PACKAGE_EXTENSION  = '.tar.gz'

# Locate the latest `APR-UTIL::PACKAGE::DOWNLOADS` link from the Apache `APR-UTIL` Downloads Page.
DOWNLOAD_URL     = BASE_URL
DOWNLOAD_PATTERN = '/apr-util-[0-9]+\.[0-9]+\.[0-9]+' + \
					PACKAGE_EXTENSION

# `APR-UTIL` build environment details.
ENVIRONMENT = {
	'BUILD_TARGET': '__APR-UTIL__',
	'DEPENDENCY'  : None,
	'BUILD_TYPE'  : 'Generic [Automated]',
	'DESCRIPTION' : "Build Automation for setting up `HTTPD` Dependency components.",
	'OS_SUPPORT'  : {
						'Unix':    ['Solaris'],
						'Linux':   ['Ubuntu', 'RHEL']
					}
}

# `THREAD` name that executes the download logic for `APR-UTIL`.
APR_UTIL_DOWNLOADER_THREAD_NAME = 'APR-UTIL::DOWNLOADER::THREAD'

# `THREAD` name that executes the untar logic for `APR-UTIL`.
APR_UTIL_UNTAR_THREAD_NAME      = 'APR-UTIL::UNTAR::THREAD'

# Package type name convention to
# be followed within the `TAR` final
# extract directory.
# Below is the `TAR` extraction directory for `APR-UTIL`.
APR_UTIL_TAR_EXTRACT_PACKAGE_TYPE_LOCATION = 'Apr-Util/'

# Location to keep the `APR-UTIL` binary.
# Change this location parameter to
# suit your environment standards.
APR_UTIL_SOURCE_PACKAGE_DESTINATION_LOCATION = helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY + \
								helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_TAR_EXTRACT_PACKAGE_TYPE_LOCATION

# `APR-UTIL` component name to be used
# program wide.
# Used to reference or label `APR-UTIL`
# related nuances.
APR_UTIL_COMPONENT_NAME  = 'Apr-Util'

# `APR-UTIL_TAR` component name to be used
# program wide.
# This is the identifier returned by
# the DownloadManager Module.
# It references the `APR-UTIL_TAR` package.
APR_UTIL_TAR_COMPONENT_NAME = 'Apr-Util_Tar'

# The `APR-UTIL_TAR` extract name to be referenced after the
# untarring operation.
APR_UTIL_TAR_EXTRACT_COMPONENT_NAME = 'Apr-Util_Tar_ExtractName'