# SVU specific `JAVA` configuration file.
# Any `JAVA` install options specific to the @SVU Environment should
# be put in this file and this file only.

# Below configuration option holds the `PROFILE` file contents
# for the `JDK`.
JAVA_PROFILE_FILE_CONTENT = \
"""##======================================================================
##
## JDK / JRE PROFILE
##

JAVA_HOME=/opt/jdk/{}
PATH=$JAVA_HOME/jre/bin:$JAVA_HOME/bin:/opt/Documentum/Shared/dfc:$PATH

export JAVA_HOME PATH
##==========================================================================
"""