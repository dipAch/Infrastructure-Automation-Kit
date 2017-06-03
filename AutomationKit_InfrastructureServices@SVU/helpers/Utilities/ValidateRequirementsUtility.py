#!/usr/bin/env python3

################################ Requirement Validator ###############################

# This utility ensures that the system is configured with the required build tools,
# so that the automation utility can successfully perform the build activities using
# those specific tools.
# The build will fail else, thus one cannot proceed with the installtion of the before
# said software packages on the system.

######################################################################################

##############################################################
# Module Import Section.
# Make all the necessary imports here.
##############################################################

# The below modules, deal with the execution of `SHELL` commands and
# other `OS` specific manipulations and operations respectively.
import subprocess, os

############# Configure the Logger options on this module #############

import logging
import helpers.Utilities.LoggerUtility
import helpers.BuildConfig.Logger.LoggerConfig

# The Logger name starts with a `PERIOD` (.), as it acts as
# a seperator between the Local Logger name and the Application
# wide Logger name.
VALIDATE_REQUIREMENTS_UTILITY_LOGGER_NAME = '.ValidateRequirementsUtility'

# Get the Logger Instance for the module.
validate_requirements_utility_logger = logging.getLogger(helpers.BuildConfig.Logger.LoggerConfig.APP_LOGGER_NAME +
												VALIDATE_REQUIREMENTS_UTILITY_LOGGER_NAME)

#######################################################################

#####################################################################
# The below class holds the definitions pertaining to the validation
# process for the required build-time tools / utilities.
#####################################################################

class ValidateBuildTools(object):
	"""
	Validate the required build-time tools such as the
	`AUTO_TOOLS` suite which includes `AUTOMAKE`, `AUTOCONF`,
	`LIBTOOL` and also the code compilation tool such as
	`GCC`.
	The build can proceed iff these above utilities are available
	in the target system, else notify the `BUILD_SUPERVISOR` and
	abort the build.
	"""

	@classmethod
	def __init__(cls, target_build_for, package_list):
		"""
		Initialize with the `TARGET_BUILD` Environment.
		"""

		# Set the `TARGET_BUILD` Environment.
		cls.target_build_for = target_build_for

		# Set the package list to check for the packages.
		cls.package_list = package_list

		# Set this flag to decide whether the build activity
		# can proceed or not.
		cls.all_packages_available = True

		# Compile the list of packages that are not available
		# and are required in order to make the build successful.
		cls.packages_to_install = []

		# Logging a comment.
		validate_requirements_utility_logger.info('Validating Requirements for Build: {' +
													str(cls.target_build_for) + '}')

	@classmethod
	def check_availability(cls):
		"""
		Start checking the availability of the packages.
		"""

		# Open a `DEV_NULL` file to emit the output of `SUBPROCESS` there.
		with open(os.devnull, 'w') as devnull:
			# Start iterating over the packages and check their
			# availability.
			for package in cls.package_list:
				VERSION_CMD = ' --version'
				if package == 'openssl':
					VERSION_CMD = ' version'
				try:
					subprocess.check_call(package + VERSION_CMD, shell=True, stdout=devnull, stderr=devnull)
				except subprocess.CalledProcessError as validateRequirementsUtility_validateBuildTools_check_availability_error:
					# Logging a comment.
					validate_requirements_utility_logger.error('Package not available: {' + str(package) + '}, Error: {' +
											str(validateRequirementsUtility_validateBuildTools_check_availability_error) + '}')

					# Logging a comment.
					validate_requirements_utility_logger.error('Please Install Package: {' + str(package) +
																'}, to proceed with the Build Task')

					# Set the below flag to `FALSE` as package is not available.
					cls.all_packages_available = False

					# Also add the package to the below list, so we can present the
					# list of missing packages on the system.
					cls.packages_to_install.append(package)

		if not cls.all_packages_available:
			# Logging a comment.
			validate_requirements_utility_logger.error('Please Install these packages: {' +
														str(cls.packages_to_install) + '}')

			# Standard `SUBPROCESS` command failure exit code.
			STANDARD_EXIT_CODE = 127

			# Command sample that shows what failed in the raised Exception.
			COMMAND_SAMPLE     = 'UTILITY-NAME [--version | version]'

			# Abort the build.
			raise subprocess.CalledProcessError(STANDARD_EXIT_CODE, COMMAND_SAMPLE)

		# If all packages are available, then we are golden to proceed.
		validate_requirements_utility_logger.info('All the build-time packages are available to support the build activity')