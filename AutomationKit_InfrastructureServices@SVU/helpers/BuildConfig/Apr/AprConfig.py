# The below module holds the `BASE_EXTRACT_DIRECTORY` location information.
import helpers.BuildConfig.Untar.UntarConfig

# The below module provides the `HTTPD` Extract's Package location.
import helpers.BuildConfig.Httpd.HttpdConfig

# Default constants for the generic installation of `APR` on production systems.
# Please alter the below configurations to suit your environment needs.
BASE_URL           = 'https://apr.apache.org/download.cgi'
ARCHIVE_URL        = 'http://archive.apache.org/dist/apr'
PACKAGE_EXTENSION  = '.tar.gz'

# Locate the latest `APR::PACKAGE::DOWNLOADS` link from the Apache `APR` Downloads Page.
DOWNLOAD_URL     = BASE_URL
DOWNLOAD_PATTERN = '/apr-[0-9]+\.[0-9]+\.[0-9]+' + \
					PACKAGE_EXTENSION

# `APR` build environment details.
ENVIRONMENT = {
	'BUILD_TARGET': '__APR__',
	'DEPENDENCY'  : None,
	'BUILD_TYPE'  : 'Generic [Automated]',
	'DESCRIPTION' : "Build Automation for setting up `HTTPD` Dependency components.",
	'OS_SUPPORT'  : {
						'Unix':    ['Solaris'],
						'Linux':   ['Ubuntu', 'RHEL']
					}
}

# `THREAD` name that executes the download logic for `APR`.
APR_DOWNLOADER_THREAD_NAME = 'APR::DOWNLOADER::THREAD'

# `THREAD` name that executes the untar logic for `APR`.
APR_UNTAR_THREAD_NAME      = 'APR::UNTAR::THREAD'

# Package type name convention to
# be followed within the `TAR` final
# extract directory.
# Below is the `TAR` extraction directory for `APR`.
APR_TAR_EXTRACT_PACKAGE_TYPE_LOCATION = 'Apr/'

# Location to keep the `APR` binary.
# Change this location parameter to
# suit your environment standards.
APR_SOURCE_PACKAGE_DESTINATION_LOCATION = helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY + \
								helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_TAR_EXTRACT_PACKAGE_TYPE_LOCATION

# `APR` component name to be used
# program wide.
# Used to reference or label `APR`
# related nuances.
APR_COMPONENT_NAME  = 'Apr-Main'

# `APR_TAR` component name to be used
# program wide.
# This is the identifier returned by
# the DownloadManager Module.
# It references the `APR_TAR` package.
APR_TAR_COMPONENT_NAME = 'Apr-Main_Tar'

# The `APR_TAR` extract name to be referenced after the
# untarring operation.
APR_TAR_EXTRACT_COMPONENT_NAME = 'Apr-Main_Tar_ExtractName'