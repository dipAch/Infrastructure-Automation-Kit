##############################################################
# Module Import Section.
# Make all the necessary imports here.
##############################################################

import helpers.BuildConfig.Logger.LoggerConfig

##############################################################

# Default constants for the generic installation of `HTTPD` on production systems.
# Please alter the below configurations to suit your environment needs.
BASE_URL           = 'https://httpd.apache.org/download.cgi'
ARCHIVE_URL        = 'https://archive.apache.org/dist/httpd'
PACKAGE_EXTENSION  = '.tar.gz'

# Locate the latest `HTTPD::PACKAGE::DOWNLOADS` link from the Apache `HTTPD` Downloads Page.
DOWNLOAD_URL     = BASE_URL
DOWNLOAD_PATTERN = '/httpd-[0-9]+\.[0-9]+\.[0-9]+' + \
					PACKAGE_EXTENSION

# `HTTPD` build environment details.
ENVIRONMENT = {
	'BUILD_TARGET': '__HTTPD__',
	'DEPENDENCY'  : ['APR', 'APRUtil', 'PCRE'],
	'BUILD_TYPE'  : 'Generic [Automated]',
	'DESCRIPTION' : "Build Automation for setting up `HTTPD` Instances.",
	'OS_SUPPORT'  : {
						'Unix':    ['Solaris'],
						'Linux':   ['Ubuntu', 'RHEL']
					}
}

# `THREAD` name that executes the download logic for `HTTPD`.
HTTPD_DOWNLOADER_THREAD_NAME = 'HTTPD::DOWNLOADER::THREAD'

# `THREAD` name that executes the untar logic for `HTTPD`.
HTTPD_UNTAR_THREAD_NAME      = 'HTTPD::UNTAR::THREAD'

# Package type name convention to
# be followed within the `TAR` final
# extract directory.
# Below is the `TAR` extraction directory for `HTTPD`.
HTTPD_TAR_EXTRACT_PACKAGE_TYPE_LOCATION = 'Httpd/'

# Location to keep the `HTTPD` binary.
# Change this location parameter to
# suit your environment standards.
HTTPD_BINARY_LOCATION = '/usr/local/apache-'

# `HTTPD` component name to be used
# program wide.
# Used to reference or label `HTTPD`
# related nuances.
HTTPD_COMPONENT_NAME  = 'Httpd'

# `HTTPD_TAR` component name to be used
# program wide.
# This is the identifier returned by
# the DownloadManager Module.
# It references the `HTTPD_TAR` package.
HTTPD_TAR_COMPONENT_NAME = 'Httpd_Tar'

# The `HTTPD_TAR` extract name to be referenced after the
# untarring operation.
HTTPD_TAR_EXTRACT_COMPONENT_NAME = 'Httpd_Tar_ExtractName'

# Set the `PCRE` location pointer flag.
WITH_PCRE_POINTER = {'pcre_location': ' --with-pcre='}

# Define the Configure time Options that needs to be set.
# For more Options, just add the directive to the below list.
ENABLE_OPTIONS_FLAGS = ['--enable-so', '--with-included-apr']

# Compile and include the above list to a dictionary for better accessibility and management.
INSTALL_TIME_OPTIONS = {'prefix_options': '--prefix=', 'enable_options': ' '.join(ENABLE_OPTIONS_FLAGS)}

# Packages to check for before the build for `HTTPD` begins.
# These packages would be required by `HTTPD` and its dependencies,
# for compiling the source packages and installing their converted binaries.
packages_to_validate = ['automake', 'autoconf', 'libtool', 'make', 'gcc', 'openssl']

# Set the log location options, to store the Build Information
# for the `HTTPD` source build (i.e., this is for the `CONFIGURE`, `MAKE` and `MAKE INSTALL` processes).
HTTPD_BUILD_PROCESS_LOG_DIRECTORY = 'Httpd_Subprocess_Logs/'
HTTPD_SUBPROCESS_LOG_LOCATION     = helpers.BuildConfig.Logger.LoggerConfig.LOG_FILE_LOCATION + HTTPD_BUILD_PROCESS_LOG_DIRECTORY
HTTPD_SUBPROCESS_LOG_FILENAME     = HTTPD_SUBPROCESS_LOG_LOCATION + 'Httpd_Subprocess.log'
