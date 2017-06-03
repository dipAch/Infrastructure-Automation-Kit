#!/usr/bin/env python3

# Author : Achinta, Dipankar (@tweeting_dipa); <Office Email>: dipankar.achinta@supervalu.com
# Created: October, 2016

###################################################################################
# `MODULE IMPORT` SECTION.
# Make all the necessary `MODULE` imports here.
# Please do not pollute the entire file with imports here and there.
###################################################################################

# Import the `TIME` module to perform time-manipulation operations.
import time

# Import the `PLATFORM` module to load the target node's system specifications.
import platform

# Import the `ABC` module to work with `ABSTRACT` classes / methods.
import abc

# Import the `BUILD` configurations module(s).
import helpers.BuildConfig.Tomcat.TomcatConfig, helpers.BuildConfig.Java.JavaConfig, helpers.BuildConfig.Untar.UntarConfig

# Import the `BUILD` configurations module(s) for `HTTPD`.
import helpers.BuildConfig.Httpd.HttpdConfig, helpers.BuildConfig.Apr.AprConfig, helpers.BuildConfig.AprUtil.AprUtilConfig

# Configuration options for the `PCRE` module / library.
import helpers.BuildConfig.Pcre.PcreConfig

# Import the `JAVA` and `TOMCAT` download modules / libraries.
# Below modules contain the `THREAD` definitions for downloading
# the required packages.
import helpers.DownloaderUtilities.TomcatUtils.DownloadJava, helpers.DownloaderUtilities.TomcatUtils.DownloadTomcat

# Import the `HTTPD` download modules / libraries.
# Below modules contain the `THREAD` definitions for downloading
# the required packages.
import helpers.DownloaderUtilities.HttpdUtils.DownloadHttpd, helpers.DownloaderUtilities.HttpdUtils.DownloadApr
import helpers.DownloaderUtilities.HttpdUtils.DownloadAprUtil

# Package Logic to download the `PCRE` library.
import helpers.DownloaderUtilities.HttpdUtils.DownloadPcre

# Get the Binary Build Module for compiling and installing the Downloaded Source Packages.
import helpers.Utilities.BinaryBuildUtility

# Get the module that performs the pre-installation checks.
import helpers.Utilities.ValidateRequirementsUtility

# Import the `TASK_MANAGER` module.
# The `DOWNLOAD_MANAGER` and the `UNTAR_MANAGER`
# class definitions extends it to fufill their 
# specifications.
# This module supervises package downloads
# as well as package extractions for the 
# automated build.
import helpers.TaskManager

# Import the `UNTAR_PACKAGE` module / library.
# Below module contains the `THREAD` definition for untarring
# the required packages.
import helpers.UntarPackage

# The below module is a Python built-in module
# for `UNTARRING` of compressed files.
import tarfile

# Having trouble with `shutil`, hence bringing in the ever reliable `subprocess` module.
import subprocess

# Below `IMPORT` deals with errors during Network Communication(s).
from urllib.error import URLError, HTTPError, ContentTooShortError

# The below module takes care of Regular Expression(s)
# within the Python Programming Environment.
# Also, imported the `OS` module to take care of `OS-specific`
# operations.
import re, os

############# Configure the Logger options on this module #############

import logging
import helpers.Utilities.LoggerUtility
import helpers.BuildConfig.Logger.LoggerConfig

# The Logger name starts with a `PERIOD` (.), as it acts as
# a seperator between the Local Logger name and the Application
# wide Logger name.
BUILD_SUPERVISOR_LOGGER_NAME = '.BuildSupervisor'

# Get the Logger Instance for the module.
build_supervisor_logger = logging.getLogger(helpers.BuildConfig.Logger.LoggerConfig.APP_LOGGER_NAME + BUILD_SUPERVISOR_LOGGER_NAME)

#######################################################################

#####################################################################################
# Class Definitions to automate `BUILD` tasks.
# Please make sure to take `BACKUPS`, before making any changes to the below classes.
#####################################################################################

# The `AUTOMATE_BUILD` Base class.
# This class contains abstract methods that need to be implemented
# by the corresponding subclasses.
class Automate(metaclass=abc.ABCMeta):
	"""
	Automate APACHE / TOMCAT build and installation. Steps performed below, adhere
	to the standard compilation and installation of the packages / softwares,
	as mentioned on the official website.
	"""

	@classmethod
	def __init__(cls, target_build_environment):
		"""
		The `INITIALIZE` method for the class instance.
		"""
		# Method to initialize the download process.
		# Create the necessary environment before executing the download.
		cls.build_environment = target_build_environment

		# Get the target system's details and store it as a dictionary.
		cls.target_platform_details =   {
											'System'         : platform.uname().system,
											'Node'           : platform.uname().node,
											'Release-Details': platform.uname().release,
											'Processor'      : platform.uname().processor
										}

		# Capture the `BUILD` start time.
		# Can be used as evidence, while auditing the `BUILD`.
		cls.build_start_time  = time.ctime()

		# Logging a comment.
		build_supervisor_logger.info('BUILD_ENVIROMENT: ' + str(cls.build_environment) + ', NODE_DETAILS: ' +
										str(cls.target_platform_details) + ', BUILD_TIME: {' + cls.build_start_time + '}')

	# The below method is a `PROTECTED` method.
	# Hence, `PROTECTED` policies apply to this
	# method.
	@staticmethod
	@abc.abstractmethod
	def _copy_binary(source_location, destination_location):
		"""
		Implement accordingly for the required `BUILD`.
		The `STATIC_METHOD` decorator specifies the method 
		type of the implementation for this class.
		The inheriting classes can change it to any other suitable
		`METHOD_TYPE` as long as they are implementing the interface
		contract correctly.
		"""

	@classmethod
	@abc.abstractmethod
	def initiate_build_workflow(cls):
		"""
		Instantiate a `DOWNLOAD_MANAGER` class entity. The instance
		should make use of the interfaces made available by
		the `DOWNLOAD_MANAGER` class to download the desired
		packages.

		Once download tasks are executed, make use of the
		`UNTAR_MANAGER` class to perform `UNTAR` operations.
		"""

# Class to specialize the behavior of the Base Class for
# `TOMCAT` setup. The below class implements the abstract
# method(s) of the `AUTOMATE` class defined above.
class TomcatAutomate(Automate):

	# <::PROTECTED_MEMBER_METHOD::>
	@classmethod
	def _copy_binary(cls, source_location, destination_location, extracted_binary_name, extracted_version_identifier):
		try:
			# Check to see if the binary destination exists.
			# If not, create it before initiating the copy.
			if not os.path.exists(destination_location):
				os.mkdir(destination_location)

			# Logging a comment.
			build_supervisor_logger.info('Performing *COPY* operation for `BINARY_PACKAGE`: {' + extracted_binary_name +
											'} from `SOURCE_LOCATION`: {' + source_location + '} to `DESTINATION_LOCATION`: {' +
												destination_location + '}')

			# Using subprocess' *check_call* to use the system `COPY` command.
			# shultil.copytree is having trouble copying symlinks.
			# Will look into that later.
			WHITE_SPACE_SEPERATOR = ' '

			# As `OS` belongs to the `*NIX` family.
			OS_COPY_DIRECTIVE = 'cp -Rp'

			# Now run the copy command to perform the *COPY* operation.
			# Both os.mkdir & COPY command can create onlt one-level of extra directories.
			# If multiple level of additional directories have to be created, than they will
			# fail and raise an exception.
			# So, make sure you have the directory structure planned out before copying anything,
			# and make calls to directory creation utilities (platform specific) or language enabled functions,
			# iff multiple levels of directory setup are required (p.s. that might require code change).
			cp_command = (OS_COPY_DIRECTIVE + WHITE_SPACE_SEPERATOR + os.path.join(source_location, extracted_binary_name) +
								WHITE_SPACE_SEPERATOR + os.path.join(destination_location, extracted_version_identifier))
			subprocess.check_call(cp_command, shell=True)

			# Logging a comment.
			build_supervisor_logger.info('Copy Operation Successful')
		except (subprocess.CalledProcessError, OSError) as copyBinary_error:
			# Put logging below.
			build_supervisor_logger.error('ERROR::BUILD_SUPERVISOR::COPY_BINARY_FAILED::' + str(copyBinary_error))
			raise

	# Utility / Helper for getting the extracted binaries' names.
	@staticmethod
	def get_extracted_names():
		# Logging a comment.
		build_supervisor_logger.info('Initiating Binary Name discovery')

		tar_extract_names = {helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_TAR_EXTRACT_COMPONENT_NAME: None,
						helpers.BuildConfig.Java.JavaConfig.JAVA_TAR_EXTRACT_COMPONENT_NAME: None}

		JAVA_BINARY_VERSION = TOMCAT_BINARY_VERSION = None

		# Iterate over each of the keys to identify the package type,
		# and to get its version and other related information. (In our case just the version).
		for tar_extract_name in list(tar_extract_names.keys()):
			if helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_COMPONENT_NAME in tar_extract_name:
				tar_extract_path = (helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
										helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_TAR_EXTRACT_PACKAGE_TYPE_LOCATION)
			elif helpers.BuildConfig.Java.JavaConfig.JAVA_COMPONENT_NAME in tar_extract_name:
				tar_extract_path = (helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
										helpers.BuildConfig.Java.JavaConfig.JAVA_TAR_EXTRACT_PACKAGE_TYPE_LOCATION)
			tar_extract_names[tar_extract_name] = os.listdir(tar_extract_path).pop()

			# Meanwhile get the version number for each of the binaries.
			# We would use it for defining the binary namespace in the destination
			# directories and also for writing to the Package Profile files.
			# Putting the unique identifier in a variable for better visibility
			# and organization. Also, the unique identifier may change over time.
			# So putting it in a variable where it's visible and accesible to change.
			# The underscore identifier is present in the `JDK` Binary name.
			# Hence, it helps in differentiating `TOMCAT` and `JAVA` binaries.
			UNIQUE_BINARY_IDENTIFIER = '_'
			if helpers.BuildConfig.Java.JavaConfig.JAVA_COMPONENT_NAME in tar_extract_name:
				java_binary_name_pattern = '\d\.\d\.\d_\d+'
				match_result = re.search(java_binary_name_pattern, tar_extract_names[tar_extract_name])
			elif helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_COMPONENT_NAME in tar_extract_name:
				tomcat_binary_name_pattern = '\d\.\d\.\d+'
				match_result = re.search(tomcat_binary_name_pattern, tar_extract_names[tar_extract_name])

			if match_result is not None:
				if UNIQUE_BINARY_IDENTIFIER in match_result.group(0):
					JAVA_BINARY_VERSION = match_result.group(0)
				else:
					TOMCAT_BINARY_VERSION = match_result.group(0)

		# Logging a comment.
		build_supervisor_logger.info('Binary Names have been successfully extracted')

		# Logging a comment.
		build_supervisor_logger.info('Extracted VERSIONS => JAVA: {' + JAVA_BINARY_VERSION + '}, TOMCAT: {' +
										TOMCAT_BINARY_VERSION + '}')

		return tar_extract_names, JAVA_BINARY_VERSION, TOMCAT_BINARY_VERSION

	# Since the below method doesn't actually require an instance
	# to operate, it can be labelled as a `CLASS_METHOD`.
	@classmethod
	def initiate_build_workflow(cls):
		"""
		Initiate the workflow for the `AUTOMATED_BUILD`.
		Workflow includes: { DOWNLOAD_PACKAGES, UNTAR_PACKAGES [, COPY_BINARY...] }
		"""
		# Build a `DOWNLOAD_MANAGER` instance.
		download_manager = helpers.TaskManager.DownloadManager()
		try:
			REQUIRED_BINARIES = {
				helpers.BuildConfig.Java.JavaConfig.JAVA_COMPONENT_NAME      : {
					'thread_name'  : helpers.BuildConfig.Java.JavaConfig.JAVA_DOWNLOADER_THREAD_NAME,
					'thread_worker': helpers.DownloaderUtilities.TomcatUtils.DownloadJava.JavaDownloaderThread
				},
				helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_COMPONENT_NAME: {
					'thread_name'  : helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_DOWNLOADER_THREAD_NAME,
					'thread_worker': helpers.DownloaderUtilities.TomcatUtils.DownloadTomcat.TomcatDownloaderThread
				}
			}

			# Gets back a dictionary containing the downloaded file-names of the `TAR` packages.
			# Packages to be downloaded are provided by the `REQUIRED_BINARIES` configuration.
			tar_binaries = download_manager.begin(cls.build_environment['BUILD_TARGET'], REQUIRED_BINARIES)

			# Logging a comment.
			build_supervisor_logger.info('`TAR` Binary Downloads Successful')
		except (URLError, HTTPError, ContentTooShortError, UnicodeDecodeError, IOError, OSError) as \
				buildSupervisor_tomcatAutomate_initiateBuildWorkflow_downloadManager_error:
			# Put logging below.
			build_supervisor_logger.error('ERROR::BUILD_SUPERVISOR::INITIATE_BUILD_WORKFLOW::DOWNLOAD_MANAGER_FAILED::' +
									str(buildSupervisor_tomcatAutomate_initiateBuildWorkflow_downloadManager_error))
			raise

		# Build an `UNTAR_MANAGER` instance.
		untar_manager = helpers.TaskManager.UntarManager()
		try:
			TAR_BINARIES = {
				helpers.BuildConfig.Java.JavaConfig.JAVA_COMPONENT_NAME      : {
					'thread_name'  : helpers.BuildConfig.Java.JavaConfig.JAVA_UNTAR_THREAD_NAME,
					'thread_worker': helpers.UntarPackage.UntarPackageThread,
					'thread_args'  : {
						'tar_file_name'    : tar_binaries[helpers.BuildConfig.Java.JavaConfig.JAVA_TAR_COMPONENT_NAME],
						'tar_package_type' : helpers.BuildConfig.Java.JavaConfig.JAVA_TAR_EXTRACT_PACKAGE_TYPE_LOCATION
					}
				},
				helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_COMPONENT_NAME: {
					'thread_name'  : helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_UNTAR_THREAD_NAME,
					'thread_worker': helpers.UntarPackage.UntarPackageThread,
					'thread_args'  : {
						'tar_file_name'   : tar_binaries[helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_TAR_COMPONENT_NAME],
						'tar_package_type': helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_TAR_EXTRACT_PACKAGE_TYPE_LOCATION
					}
				}
			}

			# Begin Package untarring operation.
			untar_manager.begin(TAR_BINARIES)

			# Logging a comment.
			build_supervisor_logger.info('`UNTAR` Operation Successful')
		except (tarfile.TarError, IOError, OSError) as buildSupervisor_tomcatAutomate_initiateBuildWorkflow_untarManager_error:
			# Put logging below.
			build_supervisor_logger.error('ERROR::BUILD_SUPERVISOR::INITIATE_BUILD_WORKFLOW::UNTAR_MANAGER_FAILED::' +
								str(buildSupervisor_tomcatAutomate_initiateBuildWorkflow_untarManager_error))
			raise

		# Get the extracted package names and also the version number
		# for each of the downloaded/extracted packages.
		# We then pass this information to the `COPY_BINARY` procedure, so that it
		# can copy the desired `TAR_EXTRACT` to the the standard location.
		tar_extract_names, java_binary_version, tomcat_binary_version = cls.get_extracted_names()

		# Copy the required binaries to the standard location.
		# Please change the location value as per your
		# standard enterprise requirement.
		try:
			# Copy the `TOMCAT` binary to the standard location.
			cls._copy_binary(source_location=(helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
									helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_TAR_EXTRACT_PACKAGE_TYPE_LOCATION),
							destination_location=helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_BINARY_LOCATION,
				extracted_binary_name=tar_extract_names[helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_TAR_EXTRACT_COMPONENT_NAME],
						extracted_version_identifier=tomcat_binary_version)

			# Copy the `JAVA` binary to the standard location.
			cls._copy_binary(source_location=(helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
									helpers.BuildConfig.Java.JavaConfig.JAVA_TAR_EXTRACT_PACKAGE_TYPE_LOCATION),
							destination_location=helpers.BuildConfig.Java.JavaConfig.JAVA_BINARY_LOCATION,
				extracted_binary_name=tar_extract_names[helpers.BuildConfig.Java.JavaConfig.JAVA_TAR_EXTRACT_COMPONENT_NAME],
							extracted_version_identifier=java_binary_version)
		except OSError as buildSupervisor_tomcatAutomate_initiateBuildWorkflow_copyBinary_error:
			# Put logging below.
			build_supervisor_logger.error('ERROR::BUILD_SUPERVISOR::INITIATE_BUILD_WORKFLOW::COPY_BINARY_FAILED::' +
						str(buildSupervisor_tomcatAutomate_initiateBuildWorkflow_copyBinary_error))
			raise

# Class to specialize the behavior of the Base Class for
# `HTTPD` setup. The below class implements the abstract
# method(s) of the `AUTOMATE` class defined above.
class HttpdAutomate(Automate):

	# <::PROTECTED_MEMBER_METHOD::>
	@classmethod
	def _copy_binary(cls, source_location, destination_location, extracted_source_name,
						extracted_httpd_source_package, dependency_build):
		try:
			# Construct the complete destination path.
			if dependency_build == helpers.BuildConfig.Apr.AprConfig.ENVIRONMENT['BUILD_TARGET']:
				destination_location += extracted_httpd_source_package + '/srclib/' + 'apr/'
			elif dependency_build == helpers.BuildConfig.AprUtil.AprUtilConfig.ENVIRONMENT['BUILD_TARGET']:
				destination_location += extracted_httpd_source_package + '/srclib/' + 'apr-util/'

			# Check to see if the destination location exists.
			# If not, create it before initiating the copy.
			if not os.path.exists(destination_location):
				os.mkdir(destination_location)

			# Logging a comment.
			build_supervisor_logger.info('Performing *COPY* operation for `SOURCE_FILE_PACKAGE`: {' + extracted_source_name +
											'} from `SOURCE_LOCATION`: {' + source_location + '} to `DESTINATION_LOCATION`: {' +
												destination_location + '}')

			# Using subprocess' *check_call* to use the system `COPY` command.
			# shultil.copytree is having trouble copying symlinks.
			# Will look into that later.
			WHITE_SPACE_SEPERATOR = ' '

			# As `OS` belongs to the `*NIX` family.
			OS_COPY_DIRECTIVE = 'cp -Rp'

			# Now run the copy command to perform the *COPY* operation.
			# Both os.mkdir & COPY command can create only one-level of extra directories.
			# If multiple level of additional directories have to be created, than they will
			# fail and raise an exception.
			# So, make sure you have the directory structure planned out before copying anything,
			# and make calls to directory creation utilities (platform specific) or language enabled functions,
			# iff multiple levels of directory setup are required (p.s. that might require code change).
			cp_command = (OS_COPY_DIRECTIVE + WHITE_SPACE_SEPERATOR + os.path.join(source_location, (extracted_source_name + '/*')) +
								WHITE_SPACE_SEPERATOR + destination_location)
			subprocess.check_call(cp_command, shell=True)

			# Logging a comment.
			build_supervisor_logger.info('Copy Operation Successful')
		except (subprocess.CalledProcessError, OSError) as copyBinary_error:
			# Put logging below.
			build_supervisor_logger.error('ERROR::BUILD_SUPERVISOR::COPY_BINARY_FAILED::' + str(copyBinary_error))
			raise

	# Utility / Helper for getting the extracted binaries' names.
	@staticmethod
	def get_extracted_names():
		# Logging a comment.
		build_supervisor_logger.info('Initiating Binary Name discovery')

		tar_extract_names = {helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_TAR_EXTRACT_COMPONENT_NAME: None,
								helpers.BuildConfig.Apr.AprConfig.APR_TAR_EXTRACT_COMPONENT_NAME: None,
									helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_TAR_EXTRACT_COMPONENT_NAME: None,
										helpers.BuildConfig.Pcre.PcreConfig.PCRE_TAR_EXTRACT_COMPONENT_NAME: None}

		HTTPD_BINARY_VERSION = PCRE_BINARY_VERSION = None

		# Iterate over each of the keys to identify the package type,
		# and to get its version and related information. (In our case just the version).
		for tar_extract_name in list(tar_extract_names.keys()):
			if helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_COMPONENT_NAME in tar_extract_name:
				tar_extract_path = (helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
										helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_TAR_EXTRACT_PACKAGE_TYPE_LOCATION)
			elif helpers.BuildConfig.Apr.AprConfig.APR_COMPONENT_NAME in tar_extract_name:
				tar_extract_path = (helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
										helpers.BuildConfig.Apr.AprConfig.APR_TAR_EXTRACT_PACKAGE_TYPE_LOCATION)
			elif helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_COMPONENT_NAME in tar_extract_name:
				tar_extract_path = (helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
										helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_TAR_EXTRACT_PACKAGE_TYPE_LOCATION)
			elif helpers.BuildConfig.Pcre.PcreConfig.PCRE_COMPONENT_NAME in tar_extract_name:
				tar_extract_path = (helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
										helpers.BuildConfig.Pcre.PcreConfig.PCRE_TAR_EXTRACT_PACKAGE_TYPE_LOCATION)
			tar_extract_names[tar_extract_name] = os.listdir(tar_extract_path).pop()

			# Meanwhile get the version number for each of the binaries
			binary_version_identifier_pattern = '\d+\.\d+(\.\d+)?'

			# Start pattern matching the version number in each of the binaries.
			match_result = re.search(binary_version_identifier_pattern, tar_extract_names[tar_extract_name])

			if match_result is not None:
			 	if helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_COMPONENT_NAME in tar_extract_name:
			 		HTTPD_BINARY_VERSION    = match_result.group(0)
			 	elif helpers.BuildConfig.Pcre.PcreConfig.PCRE_COMPONENT_NAME in tar_extract_name:
			 		PCRE_BINARY_VERSION     = match_result.group(0)

		# Logging a comment.
		build_supervisor_logger.info('Package Names have been successfully extracted')

		# Logging a comment.
		build_supervisor_logger.info('Extracted VERSIONS => HTTPD: {' + HTTPD_BINARY_VERSION + '}' +
										', PCRE: {' + PCRE_BINARY_VERSION + '}')

		return tar_extract_names , HTTPD_BINARY_VERSION, PCRE_BINARY_VERSION

	# Since the below method doesn't actually require an instance
	# to operate, it can be labelled as a `CLASS_METHOD`.
	@classmethod
	def initiate_build_workflow(cls):
		"""
		Initiate the workflow for the `AUTOMATED_BUILD`.
		Workflow includes: { DOWNLOAD_PACKAGES, UNTAR_PACKAGES [, COMPILE_FROM_SOURCE...] }
		"""

		# Pre-Installation Check and Requirements Validation.
		try:
			# Start the Requirements Check.
			helpers.Utilities.ValidateRequirementsUtility.ValidateBuildTools.__init__(cls.build_environment['BUILD_TARGET'],
													helpers.BuildConfig.Httpd.HttpdConfig.packages_to_validate)

			# Start the availability checker procedure.
			helpers.Utilities.ValidateRequirementsUtility.ValidateBuildTools.check_availability()
		except subprocess.CalledProcessError as \
						buildSupervisor_httpdAutomate_initiateBuildWorkflow_validateRequirementsUtility_error:
			# Put logging below.
			build_supervisor_logger.error('ERROR::BUILD_SUPERVISOR::INITIATE_BUILD_WORKFLOW::VALIDATE_REQUIREMENTS_FAILED::' +
									str(buildSupervisor_httpdAutomate_initiateBuildWorkflow_validateRequirementsUtility_error))
			raise

		# Build a `DOWNLOAD_MANAGER` instance.
		download_manager = helpers.TaskManager.DownloadManager()
		try:
			REQUIRED_BINARIES = {
				helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_COMPONENT_NAME       : {
					'thread_name'  : helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_DOWNLOADER_THREAD_NAME,
					'thread_worker': helpers.DownloaderUtilities.HttpdUtils.DownloadHttpd.HttpdDownloaderThread
				},
				helpers.BuildConfig.Apr.AprConfig.APR_COMPONENT_NAME             : {
					'thread_name'  : helpers.BuildConfig.Apr.AprConfig.APR_DOWNLOADER_THREAD_NAME,
					'thread_worker': helpers.DownloaderUtilities.HttpdUtils.DownloadApr.AprDownloaderThread
				},
				helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_COMPONENT_NAME: {
					'thread_name'  : helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_DOWNLOADER_THREAD_NAME,
					'thread_worker': helpers.DownloaderUtilities.HttpdUtils.DownloadAprUtil.AprUtilDownloaderThread
				},
				helpers.BuildConfig.Pcre.PcreConfig.PCRE_COMPONENT_NAME          : {
					'thread_name'  : helpers.BuildConfig.Pcre.PcreConfig.PCRE_DOWNLOADER_THREAD_NAME,
					'thread_worker': helpers.DownloaderUtilities.HttpdUtils.DownloadPcre.PcreDownloaderThread
				}
			}

			# Gets back a dictionary containing the downloaded file-names of the `TAR` packages.
			# Packages to be downloaded are provided by the `REQUIRED_BINARIES` configuration.
			tar_binaries = download_manager.begin(cls.build_environment['BUILD_TARGET'], REQUIRED_BINARIES)

			# Logging a comment.
			build_supervisor_logger.info('`TAR` Source Package Downloads Successful')
		except (URLError, HTTPError, ContentTooShortError, UnicodeDecodeError, IOError, OSError) as \
				buildSupervisor_httpdAutomate_initiateBuildWorkflow_downloadManager_error:
			# Put logging below.
			build_supervisor_logger.error('ERROR::BUILD_SUPERVISOR::INITIATE_BUILD_WORKFLOW::DOWNLOAD_MANAGER_FAILED::' +
									str(buildSupervisor_httpdAutomate_initiateBuildWorkflow_downloadManager_error))
			raise

		# Build an `UNTAR_MANAGER` instance.
		untar_manager = helpers.TaskManager.UntarManager()
		try:
			TAR_BINARIES = {
				helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_COMPONENT_NAME       : {
					'thread_name'  : helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_UNTAR_THREAD_NAME,
					'thread_worker': helpers.UntarPackage.UntarPackageThread,
					'thread_args'  : {
						'tar_file_name'    : tar_binaries[helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_TAR_COMPONENT_NAME],
						'tar_package_type' : helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_TAR_EXTRACT_PACKAGE_TYPE_LOCATION
					}
				},
				helpers.BuildConfig.Apr.AprConfig.APR_COMPONENT_NAME             : {
					'thread_name'  : helpers.BuildConfig.Apr.AprConfig.APR_UNTAR_THREAD_NAME,
					'thread_worker': helpers.UntarPackage.UntarPackageThread,
					'thread_args'  : {
						'tar_file_name'   : tar_binaries[helpers.BuildConfig.Apr.AprConfig.APR_TAR_COMPONENT_NAME],
						'tar_package_type': helpers.BuildConfig.Apr.AprConfig.APR_TAR_EXTRACT_PACKAGE_TYPE_LOCATION
					}
				},
				helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_COMPONENT_NAME: {
					'thread_name'  : helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_UNTAR_THREAD_NAME,
					'thread_worker': helpers.UntarPackage.UntarPackageThread,
					'thread_args'  : {
						'tar_file_name'   : tar_binaries[helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_TAR_COMPONENT_NAME],
						'tar_package_type': helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_TAR_EXTRACT_PACKAGE_TYPE_LOCATION
					}
				},
				helpers.BuildConfig.Pcre.PcreConfig.PCRE_COMPONENT_NAME          : {
					'thread_name'  : helpers.BuildConfig.Pcre.PcreConfig.PCRE_UNTAR_THREAD_NAME,
					'thread_worker': helpers.UntarPackage.UntarPackageThread,
					'thread_args'  : {
						'tar_file_name'   : tar_binaries[helpers.BuildConfig.Pcre.PcreConfig.PCRE_TAR_COMPONENT_NAME],
						'tar_package_type': helpers.BuildConfig.Pcre.PcreConfig.PCRE_TAR_EXTRACT_PACKAGE_TYPE_LOCATION
					}
				},
			}

			# Begin Package untarring operation.
			untar_manager.begin(TAR_BINARIES)

			# Logging a comment.
			build_supervisor_logger.info('`UNTAR` Operation Successful')
		except (tarfile.TarError, IOError, OSError) as buildSupervisor_httpdAutomate_initiateBuildWorkflow_untarManager_error:
			# Put logging below.
			build_supervisor_logger.error('ERROR::BUILD_SUPERVISOR::INITIATE_BUILD_WORKFLOW::UNTAR_MANAGER_FAILED::' +
								str(buildSupervisor_httpdAutomate_initiateBuildWorkflow_untarManager_error))
			raise

		# Get the extracted package names and also the version number
		# for each of the downloaded/extracted packages.
		# We then pass this information to the `COPY_BINARY` procedure, so that it
		# can copy the desired `TAR_EXTRACT` to the the desired location.
		# Also the version numbers would be used while configuring and installing the
		# compiled Source for `HTTPD` and `PCRE`.
		tar_extract_names, httpd_binary_version, pcre_binary_version = cls.get_extracted_names()

		# Copy the required sources to the desired location.
		# Please change the location value as per your
		# standard enterprise requirement.
		try:
			# Copy the `APR` source to the HTTPD's srclib directory location.
			cls._copy_binary(source_location=(helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
									helpers.BuildConfig.Apr.AprConfig.APR_TAR_EXTRACT_PACKAGE_TYPE_LOCATION),
							destination_location=helpers.BuildConfig.Apr.AprConfig.APR_SOURCE_PACKAGE_DESTINATION_LOCATION,
				extracted_source_name=tar_extract_names[helpers.BuildConfig.Apr.AprConfig.APR_TAR_EXTRACT_COMPONENT_NAME],
			extracted_httpd_source_package=tar_extract_names[helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_TAR_EXTRACT_COMPONENT_NAME],
			dependency_build=helpers.BuildConfig.Apr.AprConfig.ENVIRONMENT['BUILD_TARGET'])

			# Copy the `APR-UTIL` source to the HTTPD's srclib directory location.
			cls._copy_binary(source_location=(helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
									helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_TAR_EXTRACT_PACKAGE_TYPE_LOCATION),
				destination_location=helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_SOURCE_PACKAGE_DESTINATION_LOCATION,
			extracted_source_name=tar_extract_names[helpers.BuildConfig.AprUtil.AprUtilConfig.APR_UTIL_TAR_EXTRACT_COMPONENT_NAME],
			extracted_httpd_source_package=tar_extract_names[helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_TAR_EXTRACT_COMPONENT_NAME],
			dependency_build=helpers.BuildConfig.AprUtil.AprUtilConfig.ENVIRONMENT['BUILD_TARGET'])
		except OSError as buildSupervisor_httpdAutomate_initiateBuildWorkflow_copyBinary_error:
			# Put logging below.
			build_supervisor_logger.error('ERROR::BUILD_SUPERVISOR::INITIATE_BUILD_WORKFLOW::COPY_BINARY_FAILED::' +
						str(buildSupervisor_httpdAutomate_initiateBuildWorkflow_copyBinary_error))
			raise

		# Start building the Source Packages to install them.
		# The Build process includes Configuring, Compiling and
		# finally Installing the packages to the designated targets.
		try:
			################################################## BUILD PHASE I #################################################

			# Start the Build for `PCRE`.
			# Starting this means that all other dependencies and downloads have been resolved (If any).
			# Or else, this section of the code will fail.
			helpers.Utilities.BinaryBuildUtility.HttpdBuildFromSource.__init__(
										helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
										helpers.BuildConfig.Pcre.PcreConfig.PCRE_TAR_EXTRACT_PACKAGE_TYPE_LOCATION +
										tar_extract_names[helpers.BuildConfig.Pcre.PcreConfig.PCRE_TAR_EXTRACT_COMPONENT_NAME],
										binary_build_for=helpers.BuildConfig.Pcre.PcreConfig.PCRE_COMPONENT_NAME)

			# Include the version number in the docs directory for better management of software.
			helpers.BuildConfig.Pcre.PcreConfig.PCRE_DOCDIR['docdir_options'] += pcre_binary_version

			# Have the modified option included in the options list.
			helpers.BuildConfig.Pcre.PcreConfig.ENABLE_OPTIONS_FLAGS.append(
														helpers.BuildConfig.Pcre.PcreConfig.PCRE_DOCDIR['docdir_options'])

			# Include the version number in the install directory for better management of software.
			helpers.BuildConfig.Pcre.PcreConfig.PCRE_BINARY_LOCATION += pcre_binary_version

			# Set the `PREFIX` for the install needed by the `CONFIGURE` Options line.
			helpers.BuildConfig.Pcre.PcreConfig.INSTALL_TIME_OPTIONS['prefix_options'] += \
																helpers.BuildConfig.Pcre.PcreConfig.PCRE_BINARY_LOCATION

			helpers.BuildConfig.Pcre.PcreConfig.INSTALL_TIME_OPTIONS['enable_options'] = \
											' '.join(helpers.BuildConfig.Pcre.PcreConfig.ENABLE_OPTIONS_FLAGS)

			# Prepare the final Options line.
			CONFIGURE_OPTIONS_LINE = ' '.join(helpers.BuildConfig.Pcre.PcreConfig.INSTALL_TIME_OPTIONS.values())

			# Initiate the Binary Build from Source.
			helpers.Utilities.BinaryBuildUtility.HttpdBuildFromSource.initiate_source_build(CONFIGURE_OPTIONS_LINE)

			################################################# BUILD PHASE II ################################################

			# Start the Build for `HTTPD`.
			# Starting this means that all other dependencies and downloads have been resolved (If any).
			# Or else, this section of the code will fail.
			helpers.Utilities.BinaryBuildUtility.HttpdBuildFromSource.__init__(
										helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
										helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_TAR_EXTRACT_PACKAGE_TYPE_LOCATION +
										tar_extract_names[helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_TAR_EXTRACT_COMPONENT_NAME],
										binary_build_for=helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_COMPONENT_NAME)

			# Include the version number in the install directory for better management of software.
			helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_BINARY_LOCATION += httpd_binary_version

			# Set the `PREFIX` for the install needed by the `CONFIGURE` Options line.
			helpers.BuildConfig.Httpd.HttpdConfig.INSTALL_TIME_OPTIONS['prefix_options'] += \
																helpers.BuildConfig.Httpd.HttpdConfig.HTTPD_BINARY_LOCATION

			# Point `HTTPD` to the `PCRE`'s install location.
			# The below `PCRE_BINARY_LOCATION` option contains the updated value
			# (i.e., the version specific location) as per the change made while
			# configuring the `PCRE` build.
			helpers.BuildConfig.Httpd.HttpdConfig.WITH_PCRE_POINTER['pcre_location'] += \
																	helpers.BuildConfig.Pcre.PcreConfig.PCRE_BINARY_LOCATION

			# Add the following flag as `HTTPD` is having a hard time finding the installed `PCRE` package.
			helpers.BuildConfig.Httpd.HttpdConfig.INSTALL_TIME_OPTIONS['enable_options'] += \
														helpers.BuildConfig.Httpd.HttpdConfig.WITH_PCRE_POINTER['pcre_location']

			# Prepare the final Options line.
			CONFIGURE_OPTIONS_LINE = ' '.join(helpers.BuildConfig.Httpd.HttpdConfig.INSTALL_TIME_OPTIONS.values())

			# Initiate the Binary Build from Source.
			helpers.Utilities.BinaryBuildUtility.HttpdBuildFromSource.initiate_source_build(CONFIGURE_OPTIONS_LINE)
		except (OSError, subprocess.CalledProcessError) as \
						buildSupervisor_httpdAutomate_initiateBuildWorkflow_binaryBuildUtility_error:
				# Put logging below.
				build_supervisor_logger.error('ERROR::BUILD_SUPERVISOR::INITIATE_BUILD_WORKFLOW::BINARY_BUILD_FAILED::' +
						str(buildSupervisor_httpdAutomate_initiateBuildWorkflow_binaryBuildUtility_error))

				# Re-raise Exception and abort build.
				raise