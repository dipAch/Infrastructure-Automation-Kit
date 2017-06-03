#!/usr/bin/env python3

# Use-Case: Sample `TOMCAT` & `JDK / JRE` Downloader and Installation script.
# Author: Dipankar Achinta, <@tweeting_dipa>

"""
	This is a sample `TOMCAT` Installation Use-Case script.
	Do not use this file. Just take this as a reference on how to
	use the Automation-Kit to install the softwares that you need
	and the ones that this utility supports (as of now).

	Use the `AutomateBuild.py` file (same directory as this file),
	to house the Build Script suitable for your Environment / Project's needs.
"""

################################## MODULE IMPORT SECTION ##################################

# Generic `TOMCAT` configurations module.
import helpers.BuildConfig.Tomcat.TomcatConfig

# Import the Supervisor Script to Co-ordinate and control the Build Process flow.
# Importing both, to test out the Generic Supervisor as well as the @SVU specific Supervisor.
import helpers.SVUCustomBuildSupervisor, helpers.SVUCustomBuildSupervisor

###########################################################################################

###################################### START `TOMCAT` INSTALLATION PROCESS ###################################

# Initiate `TOMCAT` and its dependency (i.e., `JDK / JRE`) Download and Install.
# Wait for the Magic to Happen!!!
helpers.SVUCustomBuildSupervisor.SVUTomcatAutomate.__init__(helpers.BuildConfig.Tomcat.TomcatConfig.ENVIRONMENT)
helpers.SVUCustomBuildSupervisor.SVUTomcatAutomate.initiate_build_workflow()