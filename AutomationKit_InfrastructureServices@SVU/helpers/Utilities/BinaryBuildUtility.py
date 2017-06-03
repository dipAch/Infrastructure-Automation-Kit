#!/usr/bin/env python3

# This module houses the class that performs the standard procedure
# of building the binary from source, which includes configuring the
# the build installation, compiling the source and then installing
# the software in the appropriate location as specified during
# configuration time.

##############################################################
# Module Import Section.
# Make all the necessary imports here.
##############################################################

# The below module `FUNCTOOLS`, saves the Metadata Information of the wrapped functions
# or methods when wrapped / modified by multiple levels of Decorator (or @) functions.
import functools

# For performing `SHELL` level command execution (i.e., atleast in this module).
import subprocess

# For `OS` related operations and manipulations.
import os

# Import the `BUILD` configurations module(s).
import helpers.BuildConfig.Httpd.HttpdConfig, helpers.BuildConfig.Pcre.PcreConfig

# Get the common / shared configurations module.
import helpers.BuildConfig.Common.CommonConfig

############# Configure the Logger options on this module #############

import logging
import helpers.Utilities.LoggerUtility
import helpers.BuildConfig.Logger.LoggerConfig

# The Logger name starts with a `PERIOD` (.), as it acts as
# a seperator between the Local Logger name and the Application
# wide Logger name.
BINARY_BUILD_UTILITY_LOGGER_NAME = '.BinaryBuildUtility'

# Get the Logger Instance for the module.
binary_build_utility_logger = logging.getLogger(helpers.BuildConfig.Logger.LoggerConfig.APP_LOGGER_NAME +
												BINARY_BUILD_UTILITY_LOGGER_NAME)

#######################################################################

# Utility / Helper function - 0.
def execute_command(command_to_execute, subprocess_out_file):
	# Execute any command passed as an argument, by passing it to the
	# subprocess module's `CHECK_CALL` function utility.
	try:
		subprocess.check_call(command_to_execute, shell=True, stdout=subprocess_out_file, stderr=subprocess_out_file)
	except subprocess.CalledProcessError as binaryBuildUtility_execute_command_error:
		# Logging a comment
		binary_build_utility_logger.error('Execution of the Build Failed: {' +
											str(binaryBuildUtility_execute_command_error) + '}')

		# Propagate the current / recent exception to the root caller.
		raise

########################################################################
# The section below contains the Class Definition / Utility functions,
# that help out in the process of building the latest source code package(s)
# downloaded and extracted.
########################################################################

class BuildFromSource(object):
	"""
	Build the Binary from Source. Perform the
	standard configuration, compilation and
	install steps.
	"""

	@classmethod
	def __init__(cls, working_directory, binary_build_for):
		# Set the working directory where the configuration,
		# compilation and installation action happens.
		if not os.path.exists(working_directory):
			# Logging a comment
			binary_build_utility_logger.error('[Class: {' + cls.__name__ + '}] Could not locate working directory: {' + \
									working_directory + '} for Build: {' + binary_build_for + '}')

			# Abort and raise Exception.
			raise OSError

		# Logging a comment
		binary_build_utility_logger.info('[Class: {' + cls.__name__ + '}] Working directory: {' + working_directory + \
									'} has been located for Build: {' + binary_build_for + '}')

		# Set the working directory option.
		cls.build_directory = working_directory

		# Get the build reason, i.e., for which package
		# has the current build process been initiated.
		cls.binary_build_for = binary_build_for

	@classmethod
	def configure(cls, configure_line_options, subprocess_out_file):
		# Construct the `CONFIGURE` line for the Binary Build.
		configure_command = './configure ' + configure_line_options

		# Make the call.
		try:
			# Logging a comment
			binary_build_utility_logger.info('Starting *configure* process for the Build: {' + cls.binary_build_for + '}')

			# The below invocation, is a layer / abstraction over the `SUBPROCESS`
			# call that invokes any command as if it were executed by a `SHELL` process
			# itself.
			execute_command(configure_command, subprocess_out_file)

			# Logging a comment
			binary_build_utility_logger.info('*configure* was executed successfully for the Build: {' + cls.binary_build_for + '}')
		except subprocess.CalledProcessError as binaryBuildUtility_buildFromSource_configure_error:
			# Logging a comment
			binary_build_utility_logger.error('*configure* command for the Build Failed: {' + cls.binary_build_for + '}, Error: {' +
												str(binaryBuildUtility_buildFromSource_configure_error) + '}')

			# Abort and re-raise the exception.
			raise

	@classmethod
	def make(cls, subprocess_out_file):
		# Construct the `MAKE` command to compile the source.
		make_command = 'make'

		# Make the call.
		try:
			# Logging a comment
			binary_build_utility_logger.info('Starting *make* process for the Build: {' + cls.binary_build_for + '}')

			# The below invocation, is a layer / abstraction over the `SUBPROCESS`
			# call that invokes any command as if it were executed by a `SHELL` process
			# itself.
			execute_command(make_command, subprocess_out_file)

			# Logging a comment
			binary_build_utility_logger.info('*make* was executed successfully for the Build: {' + cls.binary_build_for + '}')
		except subprocess.CalledProcessError as binaryBuildUtility_buildFromSource_make_error:
			# Logging a comment
			binary_build_utility_logger.error('*make* command for the Build Failed: {' + cls.binary_build_for + '}, Error: {' +
												str(binaryBuildUtility_buildFromSource_make_error) + '}')

			# Abort and re-raise the exception.
			raise

	@classmethod
	def make_install(cls, subprocess_out_file):
		# Construct the `MAKE INSTALL` command to perform or initiate
		# the installation of the compiled source build.
		make_install_command = 'make install'

		# Make the call.
		try:
			# Logging a comment
			binary_build_utility_logger.info('Starting *make install* process for the Build: {' + cls.binary_build_for + '}')

			# The below invocation, is a layer / abstraction over the `SUBPROCESS`
			# call that invokes any command as if it were executed by a `SHELL` process
			# itself.
			execute_command(make_install_command, subprocess_out_file)

			# Logging a comment
			binary_build_utility_logger.info('*make install* was executed successfully for the Build: {' +
														cls.binary_build_for + '}')
		except subprocess.CalledProcessError as binaryBuildUtility_buildFromSource_make_install_error:
			# Logging a comment
			binary_build_utility_logger.error('*make install* command for the Build Failed: {' +
												cls.binary_build_for + '}, Error: {' +
												str(binaryBuildUtility_buildFromSource_make_install_error) + '}')

			# Abort and re-raise the exception.
			raise

	@classmethod
	def initiate_source_build(cls, configure_line_options):
		"""
		Initiate the workflow for building the `BINARIES` from
		`SOURCE_CODE`. This would invoke the `CONFIGURE`, `MAKE` and
		`MAKE_INSTALL` commands for completing the task at hand.
		"""

		# Get the Current Working Directory.
		# Preserve this directory so that we can change
		# back to this directory after the software build
		# operation completes.
		initial_directory = os.getcwd()

		# Change to the directory of the Source that we are building.
		# All the work will occur in this directory here-after, for the
		# current build process.
		os.chdir(cls.build_directory)

		# Logging a comment
		binary_build_utility_logger.info('Building: {' + cls.binary_build_for + '}')

		# Logging a comment
		binary_build_utility_logger.info('Working Directory Changed to: {' + cls.build_directory + '}')

		# Open a `SUBPROCESS_OUT` file to emit the output of `SUBPROCESS` there.
		with open(cls.subprocess_out_file, helpers.BuildConfig.Common.CommonConfig.SUBPROCESS_OUT_FILE_MODE) as \
			subprocess_out_file:
			try:
				# Configure the Source Tree for compilation and installation.
				cls.configure(configure_line_options, subprocess_out_file)

				# Compile the configured Source.
				cls.make(subprocess_out_file)

				# Install the Compiled Source (i.e., the binary).
				cls.make_install(subprocess_out_file)
			except subprocess.CalledProcessError as binaryBuildUtility_buildFromSource_initiate_source_build_error:
				# Logging a comment
				binary_build_utility_logger.error('** Unfortunately the Build has failed in directory: {' +
													cls.build_directory + '} for Build: {' + cls.binary_build_for +
													'} with Error: {' +
													str(binaryBuildUtility_buildFromSource_initiate_source_build_error) + '} **')

				# Logging a comment
				binary_build_utility_logger.error('Please check: {' + cls.subprocess_out_file + '} for more information')

				# Re-raise Exception and abort build.
				raise

		# Logging a comment
		binary_build_utility_logger.info('Build Completed for: {' + cls.binary_build_for + '}')

		# Logging a comment
		binary_build_utility_logger.info('Reverting to Previous Directory: {' + initial_directory + '}')
		
		# Get back to the previously set directory as the build operation
		# has completed.
		os.chdir(initial_directory)

class HttpdBuildFromSource(BuildFromSource):
	"""
	Build `HTTPD` and `PCRE` from source.
	"""

	@classmethod
	def __init__(cls, working_directory, binary_build_for):

		# Call the SuperClass' `__init__` method.
		super().__init__(working_directory, binary_build_for)

		# The below is specific for the current `HTTPD` Build and Installation.
		# Set the appropriate output-file, based on the type of build.
		if cls.binary_build_for == helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_COMPONENT_NAME:

			# Check if the Log Location for emitting the `SUBPROCESS` logs exists.
			# If not, please create it at initialization time.
			if not os.path.exists(helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_SUBPROCESS_LOG_LOCATION):
				os.mkdir(helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_SUBPROCESS_LOG_LOCATION)

			# Set the file-name that would house the `SUBPROCESS` modules' work.
			cls.subprocess_out_file = helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_SUBPROCESS_LOG_FILENAME
		elif cls.binary_build_for == helpers.BuildConfig.Pcre.PcreConfig.PCRE_COMPONENT_NAME:

			# Check if the Log Location for emitting the `SUBPROCESS` logs exists.
			# If not, please create it at initialization time.
			if not os.path.exists(helpers.BuildConfig.Pcre.PcreConfig.PCRE_SUBPROCESS_LOG_LOCATION):
				os.mkdir(helpers.BuildConfig.Pcre.PcreConfig.PCRE_SUBPROCESS_LOG_LOCATION)

			# Set the file-name that would house the `SUBPROCESS` modules' work.
			cls.subprocess_out_file = helpers.BuildConfig.Pcre.PcreConfig.PCRE_SUBPROCESS_LOG_FILENAME