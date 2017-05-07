#!/usr/bin/env python3

# Author: Dipankar Achinta (@tweeting_dipa) [2017]

##############################################################
# Module Import Section.
# Make all the necessary imports here.
##############################################################

# Import the `THREADING` module to make use of Python Threads.
import threading

# Get the configuration options for the appropriate
# `TOMCAT` package to be downloaded.
import BuildConfig.Tomcat.TomcatConfig

# Get the Web Utility Module for easing out the web related operations.
import WebUtility

# Currently making use of `URLLIB`.
# Need to make the port to `URLLIB3`.
# Need to plan the code in such a way that it
# doesn't break when making the module upgrade
# to `URLLIB3`.
try:
	from urllib.request import Request
	from urllib.error   import URLError, HTTPError, ContentTooShortError
except ImportError:
	# This is bound to fail in `PYTHON3` (As no module named `URLLIB2`).
	# Still keeping this as a placeholder.
	# This section needs to be modified when
	# upgrading to `URLLIB3` specification.
	from urllib2 import Request

# Import the `QUEUE` module to make use of the
# queue data-structure. In our program implementation,
# the queue data-structure is used as a medium for passing
# exception messages between the spawned threads and the
# `DOWNLOAD_MANAGER` process.
import queue

############# Configure the Logger options on this module #############

import logging
import LoggerUtility
import BuildConfig.Logger.LoggerConfig

# The Logger name starts with a `PERIOD` (.), as it acts as
# a seperator between the Local Logger name and the Application
# wide Logger name.
DOWNLOAD_TOMCAT_LOGGER_NAME = '.DownloadTomcat'

# Get the Logger Instance for the module.
download_tomcat_logger = logging.getLogger(BuildConfig.Logger.LoggerConfig.APP_LOGGER_NAME + DOWNLOAD_TOMCAT_LOGGER_NAME)

#######################################################################

##############################################################
# The section below contains the `THREAD` definition,
# that helps out in the process of downloading the latest
# `TOMCAT` "*.tar.gz" package for `JAVA` driven applications.
# Downloads the latest version in the specified `MAJOR-VERSION`
# range.
##############################################################

# Class Definition for the TomcatDownloader `THREAD`.
# Inherits properties from the `THREADING` Module.
class TomcatDownloaderThread(threading.Thread):
	# Initialize the `THREAD` with sub-class specific
	# information.
	# Pass on the rest to the super-class initializer method.
	def __init__(self, group=None, target=None, name=None,
					args=(), kwargs=None, *, daemon=None):
		super().__init__(group=group, target=target, name=name,
							daemon=daemon)
		self.download_complete          = False
		self.tar_file_name              = None
		self.exception_stacktrace_queue = args[0]

	# Defines the `RUN` method logic below.
	# This method is executed when the `THREAD` starts.
	def run(self):
		"""
		Perform the latest `TOMCAT` (as specified in version configuration) package download
		by first extracting the "*.tar.gz" link from the returned URI response for the Standard
		Tomcat Download Page and then downloading the package for local / shared installation. 
		"""
		try:
			# Make the match test for the intended pattern within the URI returned resource.
			match_result        = WebUtility.get_link(BuildConfig.Tomcat.TomcatConfig.VERSION_DOWNLOAD_URL,
														BuildConfig.Tomcat.TomcatConfig.VERSION_DOWNLOAD_PATTERN)

			# Pretty Self Explanatory.
			# Check the match for `PATTERN::NOT::FOUND`.
			if match_result is None:
				# Enable logging here and abort.
				# We need to update the URI configurations.
				raise IOError

			# Logging a comment
			download_tomcat_logger.info('Found URI Pattern: {' + match_result.group(0) + '} from Referrer URI {' +
																		BuildConfig.Tomcat.TomcatConfig.VERSION_DOWNLOAD_URL + '}')

			# Get the "*.tar.gz" package from the `TOMCAT-ARCHIVES` repository.
			ARCHIVE_TAR_URL     = BuildConfig.Tomcat.TomcatConfig.ARCHIVE_URL + match_result.group(0)

			# Logging a comment
			download_tomcat_logger.info('Tar Download URI constructed: {' + ARCHIVE_TAR_URL + '}')

			# Prepare the request to download the file.
			tar_request_object  = Request(ARCHIVE_TAR_URL)
			url_tar_file_name   = ARCHIVE_TAR_URL

			# Logging a comment
			download_tomcat_logger.info('{Request Prepared} Handing Off the Request Object to the *WebUtility* Service')

			# Invoke the Download action.
			# Pass in the URI file-name to use as the download base-name and
			# the `REQUEST` object to initiate the request.
			# Provide the `TAR` file-name to the DownloadManager Module.
			self.tar_file_name  = WebUtility.download_tar_binary(url_tar_file_name, tar_request_object)
		except (URLError, HTTPError, ContentTooShortError, UnicodeDecodeError, IOError, OSError) as \
				downloadTomcat_tomcatDownloaderThread_error:
			# Put logging below.
			download_tomcat_logger.error('Tomcat Download Failed: ' + str(downloadTomcat_tomcatDownloaderThread_error))
			# Put the exception object in the Exception Queue to enable
			# the TaskManager (or DownloadManager) to take care
			# of the exception.
			self.exception_stacktrace_queue.put(downloadTomcat_tomcatDownloaderThread_error)
		else:
			# Notify Download Complete.
			self.download_complete = True