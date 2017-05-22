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

# Import the `JAVA` and `TOMCAT` download modules / libraries.
# Below modules contain the `THREAD` definitions for downloading
# the required packages.
import helpers.DownloaderUtilities.TomcatUtils.DownloadJava, helpers.DownloaderUtilities.TomcatUtils.DownloadTomcat

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

			# Using subprocess' check_call to use the system `COPY` command.
			# shultil.copytree is having trouble copying symlinks.
			# Will look into that later.
			WHITE_SPACE_SEPERATOR = ' '

			# If `OS` other than `WINDOWS`.
			OS_COPY_DIRECTIVE = 'cp -pr'

			# If `OS` is `WINDOWS`, have the below set.
			if cls.target_platform_details['System'] == 'Windows':
				OS_COPY_DIRECTIVE = 'copy'

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

		for tar_extract_name in list(tar_extract_names.keys()):
			if helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_COMPONENT_NAME in tar_extract_name:
				tar_extract_path = (helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
										helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_TAR_EXTRACT_PACKAGE_TYPE_LOCATION)
			elif helpers.BuildConfig.Java.JavaConfig.JAVA_COMPONENT_NAME in tar_extract_name:
				tar_extract_path = (helpers.BuildConfig.Untar.UntarConfig.TAR_BASE_EXTRACT_DIRECTORY +
										helpers.BuildConfig.Java.JavaConfig.JAVA_TAR_EXTRACT_PACKAGE_TYPE_LOCATION)
			tar_extract_names[tar_extract_name] = os.listdir(tar_extract_path).pop()

			# Meanwhile get the version number for each of the binary.
			# We would use it for writing to the Profile files.
			# Not sure if this functionality (i.e., creating the Profile Files
			# and also extracting the version numbers for the very same reason),
			# should be a part of this Module
			# and this class Definition. We will go with it for now, I need to
			# review that later.
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

		# Get the `TAR_FILE_EXTENSION` length.
		# We make use of the below length to get the extracted filename
		# by slicing the `TAR_BINARY_NAME`.
		# We then pass this info to the `COPY_BINARY` procedure, so that it
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