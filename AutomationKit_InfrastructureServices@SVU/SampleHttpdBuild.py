#!/usr/bin/env python3

# Use-Case: Sample `HTTPD` & {`APR`, `APR-UTIL` and `PCRE`} Build and Installation script.
# Author: Dipankar Achinta, <@tweeting_dipa>

"""
	This is a sample `HTTPD` Build and Installation Use-Case script.
	Do not use this file. Just take this as a reference on how to
	use the Automation-Kit to install the softwares that you need
	and the ones that this utility supports (as of now).

	Use the `AutomateBuild.py` file (same directory as this file),
	to house the Build Script suitable for your Environment / Project's needs.
"""

################################## MODULE IMPORT SECTION ##################################

# Generic `HTTPD` configurations module.
import helpers.BuildConfig.Httpd.HttpdConfig

# Import the Supervisor Script to Co-ordinate and control the Build Process flow.
import helpers.BuildSupervisor

###########################################################################################

###################################### START `HTTPD` INSTALLATION PROCESS ###################################

# Initiate `HTTPD` and its dependency (i.e., {`APR`, `APR-UTIL` and `PCRE`}) Download, Build and Install.
# Wait for the Magic to Happen!!!
helpers.BuildSupervisor.HttpdAutomate.__init__(helpers.BuildConfig.Httpd.HttpdConfig.ENVIRONMENT)
helpers.BuildSupervisor.HttpdAutomate.initiate_build_workflow()
