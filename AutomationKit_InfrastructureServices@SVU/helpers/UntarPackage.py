#!/usr/bin/env python3

#####################################
# `IMPORT` Section.
# Make all the necessary imports here.
#####################################

# The below module is a Python built-in module
# for `UNTARRING` of compressed files.
import tarfile

# Perform `OS` level operations using the below built-in Standard Python Module.
import os

# Import the `THREADING` module to make use of Python Threads.
import threading

# Import the `TAR` configurations module for the `AUTOMATE_BUILD` application.
# Also import the common / shared configuration module.
import helpers.BuildConfig.Untar.UntarConfig, helpers.BuildConfig.Common.CommonConfig

# Import the `QUEUE` module to make use of the
# queue data-structure. In our program implementation,
# the queue data-structure is used as a medium for passing
# exception messages between the spawned threads and the
# `DOWNLOAD_MANAGER` process.
import queue

############# Configure the Logger options on this module #############

import logging
import helpers.Utilities.LoggerUtility
import helpers.BuildConfig.Logger.LoggerConfig

# The Logger name starts with a `PERIOD` (.), as it acts as
# a seperator between the Local Logger name and the Application
# wide Logger name.
UNTAR_PACKAGE_LOGGER_NAME = '.UntarPackage'

# Get the Logger Instance for the module.
untar_package_logger = logging.getLogger(helpers.BuildConfig.Logger.LoggerConfig.APP_LOGGER_NAME + UNTAR_PACKAGE_LOGGER_NAME)

#######################################################################

###############################################################
# The section below contains the `THREAD` definition,
# that helps out in the process of `EXTRACTING` the downloaded
# "*.tar.gz" packages for targeted application environments.
###############################################################

# Class Definition for the UntarPackage `THREAD`.
# Inherits properties from the `THREADING` Module.
# The default location to extract `TAR` packages is set to `DEFAULT/` folder.
class UntarPackageThread(threading.Thread):
	# Initialize the `THREAD` with sub-class specific
	# information.
	# Pass on the rest to the super-class initializer method.
	def __init__(self, group=None, target=None, name=None,
					args=(), kwargs=None, *, daemon=None):
		super().__init__(group=group, target=target, name=name,
							daemon=daemon)
		self.tar_file_name    = args[0]
		self.exception_stacktrace_queue = args[1]
		self.tar_package_type = args[2] if len(args) == 3 else helpers.BuildConfig.Untar.UntarConfig.DEFAULT_TAR_PACKAGE_TYPE
		self.untar_complete   = False

	# Defines the `RUN` method logic below.
	# This method is executed when the `THREAD` starts.
	def run(self):
		"""
		Untar `TAR` packages for installation and configuration purposes.
		This Python Module makes use of the Sandard Python Built-in Library
		for handling `TAR` files in a platform-independent and uniform manner.
		"""
		try:
			# Strip `PATH` components from the argument passed in.
			# Should only contain the `FILE-NAME` to promote code uniformity.
			tar_file_name = os.path.basename(self.tar_file_name)
			# Construct the default `TAR` package storage location.
			TAR_FILE_LOCATION = helpers.BuildConfig.Common.CommonConfig.TAR_DOWNLOAD_BASE + tar_file_name
			if TAR_FILE_LOCATION.endswith(helpers.BuildConfig.Untar.UntarConfig.TAR_EXTENSION['gz']) or \
				TAR_FILE_LOCATION.endswith(helpers.BuildConfig.Untar.UntarConfig.TAR_EXTENSION['bz2']):
				try:
					# Open the `TAR` file as a Python Object.
					tar_file = tarfile.open(TAR_FILE_LOCATION)

					# Logging a comment
					untar_package_logger.info('Tar File has been opened for extraction, from Tar Repository: {' +
												TAR_FILE_LOCATION + '}')
					# Logging a comment
					untar_package_logger.info('Checking Extract Base Directory Path: {' +
												helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
													'}. Creating if doesn\'t exists...')

					# Check to see if the `TAR` extract directory exists.
					# If not, create it and re-direct all the `TAR` extracts to the newly created directory.
					if not os.path.exists(helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY):
						os.mkdir(helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY)
						# Logging a comment
						untar_package_logger.info('Created Extract Base Directory Path: {' +
												helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY + '}')

					# Contruct the Final Directory Path.
					TAR_FINAL_EXTRACT_DIRECTORY = helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY + \
												self.tar_package_type

					# Logging a comment
					untar_package_logger.info('Checking Extract Target Directory Path: {' + 
								TAR_FINAL_EXTRACT_DIRECTORY + '}. Creating if doesn\'t exists...')

					# Check to see if `TAR` package specific directory exists.
					if not os.path.exists(TAR_FINAL_EXTRACT_DIRECTORY):
						os.mkdir(TAR_FINAL_EXTRACT_DIRECTORY)
						# Logging a comment
						untar_package_logger.info('Created Extract Target Directory Path: {' + TAR_FINAL_EXTRACT_DIRECTORY + '}')

					# Logging a comment
					untar_package_logger.info('Untarring Package to Extract Target Directory: {' +
													TAR_FINAL_EXTRACT_DIRECTORY + '}')

					# Extract the `TAR` package to the specified destination directory.
					tar_file.extractall(path=TAR_FINAL_EXTRACT_DIRECTORY)

					# Put application level logging below.
					# Logging a comment
					untar_package_logger.info('Extracted {' + tar_file_name + '} to {' + TAR_FINAL_EXTRACT_DIRECTORY + '}')
				finally:
					# Close the `TAR` stream object.
					tar_file.close()
			else:
				# Put application level logging below.
				# Logging a comment
				untar_package_logger.error('Extraction Operation Failed:: Not a {' +
												helpers.BuildConfig.Untar.UntarConfig.TAR_EXTENSION +
													'} file as per the input\'s file extension -> {' + tar_file_name + '}')
				# Raise an exception to notify that the incorrect file
				# was passed in for extraction.
				raise IOError
		except (tarfile.TarError, IOError, OSError) as untarPackage_untarPackageThread_error:
			# Put logging below.
			untar_package_logger.error('Package Extraction Failed: ' + str(untarPackage_untarPackageThread_error))
			# Put the exception object in the Exception Queue to enable
			# the TaskManager (or UntarManager) to take care
			# of the exception.
			self.exception_stacktrace_queue.put(untarPackage_untarPackageThread_error)
		else:
			# Notify `UNTAR` completion.
			self.untar_complete = True