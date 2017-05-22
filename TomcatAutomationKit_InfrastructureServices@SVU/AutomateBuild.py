#!/usr/bin/env python3

# Author : Achinta, Dipankar (@tweeting_dipa); <Office Email>: dipankar.achinta@supervalu.com
# Created: October, 2016

"""
Summary:  This is the Supervisor script that controls the `AUTO_BUILD` processes,
          for `TOMCAT` setup on any target server.
            
          This program performs a generic installation of the above mentioned
          packages (or softwares). The installation defaults to the one present
          on the official website for these software instances.
"""

###################################################################################
# `MODULE IMPORT` SECTION.
# Make all the necessary `MODULE` imports here.
# Please do not pollute the entire file with imports here and there.
###################################################################################

# Get the `BUILD_SUPERVISOR` Abstract Base Class.
import helpers.BuildSupervisor