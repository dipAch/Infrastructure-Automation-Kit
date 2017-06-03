# `TAR` download base option.
# The below setting holds the base directory to all the `TAR` package downloads.
# Change this configuration option below, to store the `TAR` package(s) to your desired location.
TAR_DOWNLOAD_BASE = '/home/vagrant/downloads/MW_AUTOMATE/TarPackages/'

# Specify the value for successive `RETRIES`.
# Change this value if necessary for your `ENVIRONMENT`.
TASK_RETRIES     = 3

######################## SUBPROCESS OUT FILE MODE ########################
# This flag is common for any of the builds.
# This flag specifies the write-to-file mode, for capturing each of the
# `SUBPROCESS`' build-time output.
SUBPROCESS_OUT_FILE_MODE = 'w'