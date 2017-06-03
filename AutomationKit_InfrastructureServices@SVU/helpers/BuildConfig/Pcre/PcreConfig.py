##############################################################
# Module Import Section.
# Make all the necessary imports here.
##############################################################

import helpers.BuildConfig.Logger.LoggerConfig

##############################################################

# Get the configuration options set for the PCRE build
# and install on the target host.

# Set the PCRE Download URL.
DOWNLOAD_URL = 'ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.40.tar.gz'

# Get this value from the above Downloads URI.
# It would be present before the `EXTENSION` type of the Archived Source Package in the URI.
# Use it to enable the configure time `PREFIX` and `DOC_DIR` options.
PCRE_VERSION = '8.40'

# `PCRE` build environment details.
ENVIRONMENT = {
	'BUILD_TARGET': '__PCRE__',
	'DEPENDENCY'  : None,
	'BUILD_TYPE'  : 'Generic [Automated]',
	'DESCRIPTION' : "Build Automation for setting up `HTTPD` Dependency components.",
	'OS_SUPPORT'  : {
						'Unix':    ['Solaris'],
						'Linux':   ['Ubuntu', 'RHEL']
					}
}

# `THREAD` name that executes the download logic for `PCRE`.
PCRE_DOWNLOADER_THREAD_NAME = 'PCRE::DOWNLOADER::THREAD'

# `THREAD` name that executes the untar logic for `PCRE`.
PCRE_UNTAR_THREAD_NAME      = 'PCRE::UNTAR::THREAD'

# Package type name convention to
# be followed within the `TAR` final
# extract directory.
# Below is the `TAR` extraction directory for `PCRE`.
PCRE_TAR_EXTRACT_PACKAGE_TYPE_LOCATION = 'Pcre/'

# Location to keep the `PCRE` binary.
# Change this location parameter to
# suit your environment standards.
PCRE_BINARY_LOCATION = '/usr/local/pcre-'

# `DOCDIR` location for the `PCRE` install.
PCRE_DOCDIR_LOCATION = '/usr/share/doc/pcre-'

# `PCRE` component name to be used
# program wide.
# Used to reference or label `PCRE`
# related nuances.
PCRE_COMPONENT_NAME  = 'Pcre'

# `PCRE_TAR` component name to be used
# program wide.
# This is the identifier returned by
# the DownloadManager Module.
# It references the `PCRE_TAR` package.
PCRE_TAR_COMPONENT_NAME = 'Pcre_Tar'

# The `PCRE_TAR` extract name to be referenced after the
# untarring operation.
PCRE_TAR_EXTRACT_COMPONENT_NAME = 'Pcre_Tar_ExtractName'

# Set the `DOCDIR` flag as an entry in the `DOCDIR` dictionary.
PCRE_DOCDIR = {'docdir_options': '--docdir=' + PCRE_DOCDIR_LOCATION}

# Define the Configure time Options that needs to be set.
# For more Options, just add the directive to the below list.
ENABLE_OPTIONS_FLAGS = ['--enable-unicode-properties', '--enable-pcre16', '--enable-pcre32',
						'--enable-pcregrep-libz', '--disable-static']

# Have the `PREFIX` set here, and we will include the `CONFIGURE` line options at run-time
# from the `BUILD_SUPERVISOR` Script.
INSTALL_TIME_OPTIONS = {'prefix_options': '--prefix='}

# Set the log location options, to store the Build Information
# for the `PCRE` source build (i.e., this is for the `CONFIGURE`, `MAKE` and `MAKE INSTALL` processes).
PCRE_BUILD_PROCESS_LOG_DIRECTORY  = 'Pcre_Subprocess_Logs/'
PCRE_SUBPROCESS_LOG_LOCATION      = helpers.BuildConfig.Logger.LoggerConfig.LOG_FILE_LOCATION + PCRE_BUILD_PROCESS_LOG_DIRECTORY
PCRE_SUBPROCESS_LOG_FILENAME      = PCRE_SUBPROCESS_LOG_LOCATION + 'Pcre_Subprocess.log'