# Configuration Options for the Application's Logging Facility.
# Make changes to the behaviour of the Logger by changing
# the specified options present below.

import logging

# Configure the Application wide Logger name.
APP_LOGGER_NAME = 'LoggerUtility::AUTOMATE_BUILD'

# Set the Log Level for the Logger components.
LOGGER_LEVEL = logging.INFO
FILE_HANDLER_LEVEL = logging.INFO
CONSOLE_HANDLER_LEVEL = logging.WARNING

# File Handler Settings
LOG_FILE_LOCATION = '/home/vagrant/downloads/MW_AUTOMATE/logs/'
LOG_FILENAME = LOG_FILE_LOCATION + 'Build_Automate.log'

# We chose mode `w` (Write-Mode), as we need a new file to be created
# for each build. This is not a rolling application log.
# If the file already exists, the contents will be clobbered.
LOG_FILE_MODE = 'w'

# Set the Formatter settings and options.
FILE_FORMATTER_SETTING = '[%(asctime)s] :: [%(levelname)s] :: [%(threadName)-15s] :: [%(name)-15s] >> %(message)s'
CONSOLE_FORMATTER_SETTING = '[%(asctime)s] :: [%(levelname)s] :: [%(name)-15s] >> %(message)s'