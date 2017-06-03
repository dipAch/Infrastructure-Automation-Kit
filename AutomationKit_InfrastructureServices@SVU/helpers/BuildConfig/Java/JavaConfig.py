# Default constants for the generic installation of `JAVA` on production systems.
# Please alter the below configurations to suit your environment needs.
BASE_URL           = 'http://www.oracle.com'
JAVA_PACKAGE       = 'server-jre'
JAVA_VERSION       = '[0-9]+'
ARCHITECTURE_SET   = 'linux-x64'
PACKAGE_EXTENSION  = '.tar.gz'

# Locate the `JAVA::PACKAGE::DOWNLOADS` link from the Primary Oracle `JAVA` Downloads Page.
DOWNLOADS_URL      = BASE_URL + '/technetwork/java/javase/downloads/index.html'
DOWNLOAD_PATTERN   = '/technetwork/java/javase/downloads/' + JAVA_PACKAGE + JAVA_VERSION + '-downloads-[0-9]+\.html'

# Download the "*.tar.gz" package for `JAVA`.
# Need to extract the link for the package download
# from the downloads page.
# Below are the identifier entities for doing that.
DOWNLOAD_TAR_PATTERN = 'http://download\.oracle\.com/otn-pub/java/jdk/[7-9]u([0-9]+)?-.+/' + JAVA_PACKAGE + \
						'-[7-9]u([0-9]+)?-' + ARCHITECTURE_SET + PACKAGE_EXTENSION

# `JAVA` build environment details.
ENVIRONMENT = {
	'BUILD_TARGET': '__JAVA__',
	'DEPENDENCY'  : None,
	'BUILD_TYPE'  : 'Generic [Automated]',
	'DESCRIPTION' : "Build Automation for setting up Java Dependent Instances.",
	'OS_SUPPORT'  : {
						'Unix':    ['Solaris'],
						'Linux':   ['Ubuntu', 'RHEL']
					}
}

# `THREAD` name that executes the download logic for `JAVA`.
JAVA_DOWNLOADER_THREAD_NAME = 'JAVA::DOWNLOADER::THREAD'

# `THREAD` name that executes the untar logic for `JAVA`.
JAVA_UNTAR_THREAD_NAME      = 'JAVA::UNTAR::THREAD'

# Package type name convention to
# be followed within the `TAR` final
# extract directory.
# Below is the `TAR` extraction directory for `JAVA`.
JAVA_TAR_EXTRACT_PACKAGE_TYPE_LOCATION = 'Java/'

# Location to keep the `JAVA` binary.
# Change this location parameter to
# suit your environment standards.
JAVA_BINARY_LOCATION = '/opt/jdk/'

# `JAVA` profile file name.
# This option is specific to the SVU Environment / Setup.
# Not required in case if, it's a Generic Install.
JAVA_PROFILE_FILE_NAME = 'java_profile.txt'

# `JAVA` component name to be used
# program wide.
# Used to reference or label `JAVA`
# related nuances.
JAVA_COMPONENT_NAME  = 'Java'

# `JAVA_TAR` component name to be used
# program wide.
# This is the identifier returned by
# the DownloadManager Module.
# It references the `JAVA_TAR` package.
JAVA_TAR_COMPONENT_NAME = 'Java_Tar'

# The `JAVA_TAR` extract name to be referenced after the
# untarring operation.
JAVA_TAR_EXTRACT_COMPONENT_NAME = 'Java_Tar_ExtractName'