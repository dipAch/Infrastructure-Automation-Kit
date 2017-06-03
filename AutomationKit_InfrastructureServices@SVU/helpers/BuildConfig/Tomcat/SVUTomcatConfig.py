# SVU specific `TOMCAT` configuration file.
# Any `TOMCAT` install options specific to the @SVU Environment should
# be put in this file and this file only.

# Below configuration option holds the `PROFILE` file contents
# for `TOMCAT`.
TOMCAT_PROFILE_FILE_CONTENT = \
"""##======================================================================
##
## TOMCAT PROFILE
##

. /opt/jdk/{0}/jdkprofile

CATALINA_HOME=/opt/tomcat/{1}
PATH=$CATALINA_HOME/bin:/opt/Documentum/Shared/dfc:$PATH
DISPLAY=0.0

export CATALINA_HOME PATH DISPLAY
##==========================================================================
"""