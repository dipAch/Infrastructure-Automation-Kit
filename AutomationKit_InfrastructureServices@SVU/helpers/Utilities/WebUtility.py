#!/usr/bin/env python3

# This module holds the essential tools for navigating the web
# and perform operations such as downloading software packages.
# This module provides the utility functions to parse web resources
# and extract the URLs or links from them to get the desired resource
# endpoints.

##############################################################
# Module Import Section.
# Make all the necessary imports here.
##############################################################

# Import the IO configurations module.
# This below module holds the configuration options
# for IO related operations performed by the automation
# software.
# Also, imported the common configurations module.
import helpers.BuildConfig.IO.IOConfig, helpers.BuildConfig.Common.CommonConfig

# The below module takes care of Regular Expression(s)
# within the Python Programming Environment.
# Also, imported the `OS` module to take care of `OS-specific`
# operations.
import re, os

# Currently making use of `URLLIB`.
# Need to make the port to `URLLIB3`.
# Need to plan the code in such a way that it
# doesn't break when making the module upgrade
# to `URLLIB3`.
try:
	from urllib.request import Request, urlopen
	from urllib.error   import URLError, HTTPError, ContentTooShortError
except ImportError:
	# This is bound to fail in `PYTHON3` (As no module named `URLLIB2`).
	# Still keeping this as a placeholder.
	# This section needs to be modified when
	# upgrading to `URLLIB3` specification.
	from urllib2 import Request, urlopen

############# Configure the Logger options on this module #############

import logging
import helpers.Utilities.LoggerUtility
import helpers.BuildConfig.Logger.LoggerConfig

# The Logger name starts with a `PERIOD` (.), as it acts as
# a seperator between the Local Logger name and the Application
# wide Logger name.
WEB_UTILITY_LOGGER_NAME = '.WebUtility'

# Get the Logger Instance for the module.
web_utility_logger = logging.getLogger(helpers.BuildConfig.Logger.LoggerConfig.APP_LOGGER_NAME + WEB_UTILITY_LOGGER_NAME)

#######################################################################

#################################################################
# The section below contains the utility functions,
# that help out in the process of downloading the latest
# "*.tar.gz" package(s).
#################################################################

# Utility Function - 0
def get_link(target_url, link_pattern):
	"""
	Helper function to extract links, necessary
	to locate the correct package. This function
	parses the URL response to extract and follow the links,
	that lead to the "*.tar.gz" software package.
	"""

	# The name of the function for logging purposes.
	# Change the function object reference, in case the function name is changed.
	# The underscore in the beginning marks that this is an
	# internal-use local variable.
	_function_name = get_link.__name__

	try:
		request_object  = Request(target_url)
		response_object = urlopen(request_object)

		# Logging a comment
		web_utility_logger.info('[Function: {' + _function_name + '}] Request sent to URI: {' + target_url + '}')

		# Store the Response [or Content] from the URI.
		content_body    = response_object.read().decode('UTF-8')

		# Logging a comment
		web_utility_logger.info('[Function: {' + _function_name + '}] Response Received from URI: {' + target_url + '}')
	except (URLError, HTTPError, ContentTooShortError, UnicodeDecodeError, IOError, OSError) as webutility_get_link_error:
		# Put logging below.
		web_utility_logger.error('[Function: {' + _function_name + '}] URI Request Failed: ' + str(webutility_get_link_error))
		raise
	else:
		# The below returns either the matched string within
		# the content of the response, or it would return `NONE`
		# meaning it couldn't locate the pattern.
		match_result        = re.search(link_pattern, content_body)
		return match_result
	finally:
		# Close the `SOCKET` stream object.
		response_object.close()

# Utility Function - 1
def download_tar_binary(url_tar_file_name, tar_request_object):
	"""
	Get the "*.tar.gz" package from the requested URI. The chore of this 
	utility function is to just download the `TAR` package and save it
	to a file on-disk.
	"""

	# The name of the function for logging purposes.
	# Change the function object reference, in case the function name is changed.
	# The underscore in the beginning marks that this is an
	# internal-use local variable.
	_function_name = download_tar_binary.__name__

	try:
		# Get the URL response from the supplied link.
		binary_response   = urlopen(tar_request_object)

		# Logging a comment
		web_utility_logger.info('[Function: {' + _function_name + '}] Checking Tar Download Base Directory Path: {' +
								helpers.BuildConfig.Common.CommonConfig.TAR_DOWNLOAD_BASE + '}. Creating if doesn\'t exists...')

		# Check if the `TAR` base downloads directory exists.
		if not os.path.exists(helpers.BuildConfig.Common.CommonConfig.TAR_DOWNLOAD_BASE):
			os.mkdir(helpers.BuildConfig.Common.CommonConfig.TAR_DOWNLOAD_BASE)
			# Logging a comment
			web_utility_logger.info('[Function: {' + _function_name + '}] Created Tar Download Base Directory Path: {' +
											helpers.BuildConfig.Common.CommonConfig.TAR_DOWNLOAD_BASE + '}')

		tar_file_name     = os.path.basename(url_tar_file_name)
		tar_file_location = helpers.BuildConfig.Common.CommonConfig.TAR_DOWNLOAD_BASE + tar_file_name
		# Start the "*.tar.gz" (compressed) binary download.
		with open(tar_file_location, 'wb') as tar_object:
			while True:
				# Read the "*.tar.gz" response in chunks
				tar_chunk = binary_response.read(helpers.BuildConfig.IO.IOConfig.CHUNK)
				if not tar_chunk:
					break
				# Write the response chunk to the "target on-disk file".
				tar_object.write(tar_chunk)

		# Logging a comment
		web_utility_logger.info('[Function: {' + _function_name + '}] Tar successfully Downloaded to Location: {' +
									tar_file_location + '}')

		# Return the `TAR` file-name.
		return tar_file_name
	except (URLError, HTTPError, ContentTooShortError, IOError, OSError) as webUtility_download_tar_binary_error:
		# Put logging below.
		web_utility_logger.error('[Function: {' + _function_name + '}] Tar Download Failed: ' +
									str(webUtility_download_tar_binary_error))
		raise
	finally:
		# Close the `SOCKET` stream object.
		binary_response.close()