#!/usr/bin/env python3

# Author: Dipankar Achinta, Email: dipankar.achinta@supervalu.com
# Outfit: Middleware Services, Email: TS.MiddlewareServices@supervalu.com

'''
Custom Script for configuring `TOMCAT` & `JDK/JRE` Download within SVU Environment.
It extends the ``Base Tomcat Automation Class`` to have the Profile Files in place.
If you need to modify or extend the behavior of this utility, you can alter it here,
instead of doing it in the Base Class, as the Download procedure is same across all
platforms and environments.
'''

###################################################################################
# `MODULE IMPORT` SECTION.
# Make all the necessary `MODULE` imports here.
# Please do not pollute the entire file with imports here and there.
###################################################################################

# Import the `BUILD` configurations module(s).
import helpers.BuildConfig.Tomcat.TomcatConfig, helpers.BuildConfig.Java.JavaConfig

# Import the Normalized `TOMCAT` Installer and Downloader class.
# The class in this module, extends the above Super Class' functionality.
import helpers.BuildSupervisor

############# Configure the Logger options on this module #############

import logging
import helpers.Utilities.LoggerUtility
import helpers.BuildConfig.Logger.LoggerConfig

# The Logger name starts with a `PERIOD` (.), as it acts as
# a seperator between the Local Logger name and the Application
# wide Logger name.
SVU_BUILD_SUPERVISOR_LOGGER_NAME = '.SVUCustomBuildSupervisor'

# Get the Logger Instance for the module.
svu_build_supervisor_logger = logging.getLogger(helpers.BuildConfig.Logger.LoggerConfig.APP_LOGGER_NAME +
														SVU_BUILD_SUPERVISOR_LOGGER_NAME)

#######################################################################

#####################################################################################
# Class Definitions to automate `BUILD` tasks.
# Please make sure to take `BACKUPS`, before making any changes to the below classes.
#####################################################################################

# Class to specialize the behavior of the Base Class for
# `TOMCAT` setup. This class is specific to the environment
# requirements for and within SuperValu.
class SVUTomcatAutomate(helpers.BuildSupervisor.TomcatAutomate):

	# <::PROTECTED_MEMBER_METHOD::>
	# This method serves specific to the SVU Environment.
	@staticmethod
	def _create_profile(environment_profile_for, profile_file_name, tomcat_profile_version='current', java_profile_version='current'):
		# Start the `PROFILE` file creation for the appropriate binary installation.
		try:
			# Logging a comment.
			svu_build_supervisor_logger.info('Creating the *' + environment_profile_for + '* profile file')

			with open(profile_file_name, 'wt') as profile_file_obj:
				if environment_profile_for == helpers.BuildConfig.Tomcat.TomcatConfig.ENVIRONMENT['BUILD_TARGET']:
					# Opens a file to write the `TOMCAT` profile.
					# `TOMCAT` uses the below profile for setting up its environment
					# during startup, i.e., which version of `JRE/JDK` to use.

					# Setup the `TOMCAT` profile.
					# This file is loaded when `TOMCAT` starts.
					# Loads the environment settings for the currently invoked `TOMCAT` installation.

					# The below `PROFILE` file properties, need to be updated
					# as per your environment requirements. It is useful, when
					# you have multiple versions of `TOMCAT`, running different versions
					# of `JRE/JDK`, depending on the applications present in the shared application
					# farm. In our environment, we use the below directory convention
					# for our `TOMCAT` & `JRE` setup.
					profile_file_obj.write('##\n## TOMCAT PROFILE\n##\n\n')
					profile_file_obj.write('. /opt/jdk/' + java_profile_version + '/jdkprofile\n\n')
					profile_file_obj.write('CATALINA_HOME=/opt/tomcat/' + tomcat_profile_version + '\n')
					profile_file_obj.write('PATH=$CATALINA_HOME/bin:/opt/Documentum/Shared/dfc:$PATH\n')
					profile_file_obj.write('DISPLAY=0.0\n\n')
					profile_file_obj.write('export CATALINA_HOME PATH DISPLAY\n')
				elif environment_profile_for == helpers.BuildConfig.Java.JavaConfig.ENVIRONMENT['BUILD_TARGET']:
					# Setup the `JAVA` profile file.
					# It loads the environment settings for the specific `JAVA` version,
					# that an application is compatible with. It is loaded when `TOMCAT`
					# starts an application instance by invoking this profile file.
					# Loading this profile will affect the current shell session and the
					# environment settings for any of its child processes.
					profile_file_obj.write('##\n## JAVA PROFILE\n##\n\n')
					profile_file_obj.write('JAVA_HOME=/opt/jdk/' + java_profile_version + '\n\n')
					profile_file_obj.write('PATH=$JAVA_HOME/jre/bin:$JAVA_HOME/bin:/opt/Documentum/Shared/dfc:$PATH\n\n')
					profile_file_obj.write('export JAVA_HOME PATH\n')

			# Logging a comment.
			svu_build_supervisor_logger.info('Profile: {' + profile_file_name + '} created for: {' +
											environment_profile_for + '}')
		except (IOError, OSError) as createProfile_error:
			# Put logging below.
			svu_build_supervisor_logger.error('ERROR::SVU_BUILD_SUPERVISOR::CREATE' + environment_profile_for + 'PROFILE_FAILED::' +
									str(createProfile_error))
			raise

	# Since the below method doesn't actually require an instance
	# to operate, it can be labelled as a `CLASS_METHOD`.
	@classmethod
	def initiate_build_workflow(cls):
		# Perform the operations defined as per the default installation
		# guide.
		# For the customized behavior, perform as specified below.
		super().initiate_build_workflow()

		# Get the `TAR_FILE_EXTENSION` length.
		# We make use of the below length to get the extracted filename
		# by slicing the `TAR_BINARY_NAME`.
		# We then pass this info to the `COPY_BINARY` procedure, so that it
		# can copy the desired `TAR_EXTRACT` to the the standard location.
		tar_extract_names, java_binary_version, tomcat_binary_version = cls.get_extracted_names()

		# The below sets up the `TOMCAT` profile file for the installation / setup.
		# This is specific to SVU Environment.
		try:
			# Create the `TOMCAT` profile file.
			cls._create_profile(cls.build_environment['BUILD_TARGET'],
									(helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_BINARY_LOCATION +
										tomcat_binary_version +
											'/' + helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_PROFILE_FILE_NAME),
												tomcat_binary_version, java_binary_version)

			# Create the `JAVA` profile file.
			cls._create_profile(helpers.BuildConfig.Java.JavaConfig.ENVIRONMENT['BUILD_TARGET'],
									(helpers.BuildConfig.Java.JavaConfig.JAVA_BINARY_LOCATION +
										java_binary_version +
											'/' + helpers.BuildConfig.Java.JavaConfig.JAVA_PROFILE_FILE_NAME),
												java_profile_version=java_binary_version)
		except (IOError, OSError) as svuBuildSupervisor_tomcatAutomate_initiateBuildWorkflow_createProfile_error:
			# Put logging below.
			svu_build_supervisor_logger.error('ERROR::SVU_BUILD_SUPERVISOR::INITIATE_BUILD_WORKFLOW::CREATE_PROFILE_FAILED::' +
						str(svuBuildSupervisor_tomcatAutomate_initiateBuildWorkflow_createProfile_error))
			raise