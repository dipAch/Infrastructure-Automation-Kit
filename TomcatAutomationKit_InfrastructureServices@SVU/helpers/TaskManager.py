#!/usr/bin/env python3

# Author: Dipankar Achinta (@tweeting_dipa) [2017]

###########################################
# `IMPORT` Section.
# Make all the necessary `IMPORTS` below.
###########################################

# Import the `BUILD` configurations module(s).
import helpers.BuildConfig.Common.CommonConfig, helpers.BuildConfig.Tomcat.TomcatConfig, helpers.BuildConfig.Java.JavaConfig

# Import the `ABC` module to work with `ABSTRACT` classes / methods.
import abc

# Import the `THREADING` library.
import threading

# Import the `TIME` module to perform time-manipulation operations.
import time

# Below `IMPORT` deals with errors during Network Communication(s).
from urllib.error import URLError, HTTPError, ContentTooShortError

# The below module is a Python built-in module
# for `UNTARRING` of compressed files.
import tarfile

# Import the `QUEUE` module to make use of the
# queue data-structure. In our program implementation,
# the queue data-structure is used as a medium for passing
# exception messages between the spawned threads and the
# `DOWNLOAD_MANAGER | UNTAR_MANAGER` processes.
import queue

############# Configure the Logger options on this module #############

import logging
import helpers.Utilities.LoggerUtility
import helpers.BuildConfig.Logger.LoggerConfig

# The Logger name starts with a `PERIOD` (.), as it acts as
# a seperator between the Local Logger name and the Application
# wide Logger name.
TASK_MANAGER_LOGGER_NAME = '.TaskManager'

# Get the Logger Instance for the module.
task_manager_logger = logging.getLogger(helpers.BuildConfig.Logger.LoggerConfig.APP_LOGGER_NAME + TASK_MANAGER_LOGGER_NAME)

#######################################################################

###########################################################
# Task Manager Model for resolving dependent tasks,
# required by the target software for the `AUTOMATED`
# software build.
###########################################################

class TaskManager(object):
	"""
	Class blueprint for creating task agent(s) for the build. These instances / agents will
	handle the entire dependency tasks and tasks specific to the target software for the
	automated build. The `TASK_MANAGER` makes use of `THREAD`s, which allow for concurrent tasks
	to be performed, which when done sequentially takes a lot of time.
	"""

	def __init__(self):
		"""
		The `INITIALIZE` method for the class.
		"""
		# Capture the `TASK` start time.
		# Can be used as evidence, while auditing the `BUILD`.
		self.task_start_time  = time.ctime()

		# Specify the number of retries, in case of failures. <::PROTECTED_ATTRIBUTE::>
		self._allowed_retries = helpers.BuildConfig.Common.CommonConfig.TASK_RETRIES

		# Set the current `RETRY` count. <::PROTECTED_ATTRIBUTE::>
		self._current_retry_count = 0

		# Set the success flag to `FALSE` initially for each task.
		self.task_successful = False

		# Set the `INITIAL_RUN` status.
		# Provides help in the identification of failed threads.
		self.initial_run = True

		# Helps us accumulate the failed threads and perform a retry on them.
		self.failed_thread_list = []

		# Logging a comment
		task_manager_logger.info('[Class: {' + str(self.__class__) + '}] Initialization Information: START_TIME: {' +
						self.task_start_time + '}')

	def begin(self, support_binaries):
		"""
		The `BEGIN` method takes care of the tasks to be performed for each build.
		This method employs each task as a sub-classable Threaded entity and is executed 
		by `THREAD`s spawned to make the tasks complete for the specific build(s).

		PARAMETER:=> 	[BUILD_FOR] <OPTIONAL> = Target Build's Details.
						SUPPORT_BINARIES       = A dictionary object consisting of the pre-build requisites.

		`REQUIRED_BINARIES` is a nested dictionary. It contains the `THREAD-NAME` and
		`THREAD-WORKER` logic that is to be simultaneously executed.
		"""
		pass

	def allow_retry(self):
		"""
		Keep track of the number of retries done by the `TASK_MANAGER` instance.
		Retries is by default set to 3 (`THREE`).
		Can be changed by altering the value in the corresponding `CONFIG`
		file.
		"""
		if self.current_retry_count <= self.retries_allowed():
			# Increment the `RETRY_COUNT` attribute, via. an attribute `SETTER`.
			self.current_retry_count = 1
			return True
		return False

	# Use a `PROPERTY` setter and getter to access the protected member.
	@property
	def current_retry_count(self):
		"""
		Returns the `CURRENT` retry count for the specific `TASK_MANAGER`.
		"""
		return self._current_retry_count

	@current_retry_count.setter
	def current_retry_count(self, retry_increment_by):
		# Perform the actual increment for the `RETRY_COUNT` attribute.
		self._current_retry_count += retry_increment_by

	def retries_allowed(self):
		"""
		Returns the specified maximum `RETRY` value allowed by the
		`TASK_MANAGER` for the `BUILD`.
		"""
		return self._allowed_retries

###########################################
# Download Manager Model for downloading
# dependencies and target software for the
# `AUTOMATED` software build.
###########################################

class DownloadManager(TaskManager):
	"""
	Class blueprint for creating download agent(s) for the build. These instances / agents will
	handle the entire dependency downloads and target software download for the automated
	build. To make the downloads more time efficient, we are using the `THREADING` module
	that the Python Standard Library provides. This allows us for concurrent simultaneous
	downloads, which when done sequentially takes a lot of time.
	"""

	def begin(self, build_for, required_binaries):
		"""
		The `BEGIN` method takes care of the `TAR` package downloads.
		Puts them under the `CONFIGURED` or `DEFAULT` directory accordingly.

		PARAMETER:=> 	BUILD_FOR         = Target software for which the automated build is being performed.
						REQUIRED_BINARIES = A dictionary object consisting of dependent tasks and other details.

		`REQUIRED_BINARIES` is a nested dictionary. It contains the `THREAD-NAME` and
		`THREAD-WORKER` logic that is to be simultaneously executed.
		"""

		# Keeps a handle to the newly spawned threads.
		# Makes it easy for the caller to inspect the
		# threads and also for accessing their state
		# post execution.
		thread_for = {}

		while not self.task_successful and self.allow_retry():
			try:
				# Instantiate the `QUEUE` exception stacktrace object for the spawned threads.
				exception_stacktrace_queue = queue.Queue()

				# Logging a comment
				task_manager_logger.info('[Class: {' + str(self.__class__) + '}] Instantiating Downloader Threads...')

				for component in list(required_binaries.keys()):
					if self.initial_run or component in self.failed_thread_list:
						downloader_thread = \
								required_binaries[component]['thread_worker'](name=required_binaries[component]['thread_name'],
																				args=(exception_stacktrace_queue,))
						thread_for[component] = downloader_thread

						# Logging a comment
						task_manager_logger.info('[Class: {' + str(self.__class__) + '}] Instantiated Downloader Thread: {' +
														downloader_thread.getName() + '}')

						# Start the `THREAD`.
						downloader_thread.start()

				# The below method makes the main thread (or process) to block
				# until the minion `THREAD`s complete their tasks.
				# This would in turn block the `BEGIN` method from returning
				# back to the caller.
				the_main_thread = threading.main_thread()

				for active_thread in threading.enumerate():
					# If we `JOIN` the main thread of execution,
					# it will introduce a deadlock. Hence, that
					# needs to be skipped.
					if active_thread is the_main_thread:
						continue

					# `JOIN` all the other active threads.
					# It will block the main thread from exiting, i.e.,
					# it waits for the chilren threads to finish their
					# execution.
					active_thread.join()

				# Check the Exception Stack and re-raise the exception (If Any).
				# The below statement is reached only after the threads finish
				# their work either normally or abnormally.
				if not exception_stacktrace_queue.empty():
					# Get the first exception element and raise the same.
					# Once, the exception is raised (if any), the exception
					# handler will handle the overall exceptions raised by the
					# spawned threads by checking their status flags.
					raise exception_stacktrace_queue.get()

			except (URLError, HTTPError, ContentTooShortError, UnicodeDecodeError, IOError, OSError) as \
					taskManager_downloadManager_error:
				# Put logging below.
				task_manager_logger.error('[Class: {' + str(self.__class__) + '}] Download Operation Failed: ' +
												str(taskManager_downloadManager_error))

				# Delete the exception stacktrace queue
				# before continuing with the next iteration of
				# trials. This stacktrace object just lets us
				# identify whether any exception(s) occurred in any of
				# the spawned threads. Once we confirm that an exception
				# has occurred, we check the status of all the threads
				# spawned by the `DOWNLOAD_MANAGER` process and put them
				# up for retry only if that particular thread failed during
				# its execution.
				del exception_stacktrace_queue

				# It's past its `INITIAL_RUN` now.
				# Mark it as `FALSE`.
				self.initial_run = False

				# Iterate over the spawned `THREAD` list dictionary.
				# Check for each `THREAD`'s completion status.
				# If completion status is `UNSET` (or False), add it to the
				# failed thread list.
				for component in list(thread_for.keys()):
					if not thread_for[component].download_complete:
						# Logging a comment
						task_manager_logger.critical('[Class: {' + str(self.__class__) +
												'}] Downloader Thread Failed for Component: {' +
														component + '}')

						# We don't want to re-add the component, if it is
						# already present in the below list.
						# Otherwise, it would spawn multiple `THREAD`s for
						# the same component.
						# The below check is an alternative to having cleared
						# the list before each failed iteration.
						if component not in self.failed_thread_list:
							self.failed_thread_list.append(component)

				# Check if the `DOWNLOAD` operation succeeded after the specified number of retries (If any).
				# Raise the error if it failed for more than the specified value of `RETRY`.
				if self.current_retry_count > self.retries_allowed():
					# Logging a comment
					task_manager_logger.critical('[Class: {' + str(self.__class__) + '}] Maximum Retries Exceeded. Please \
													run a Diagnostic for probable issues.')
					raise

				# Logging a comment
				task_manager_logger.info('[Class: {' + str(self.__class__) + '}] Current Download Retry Count: {' +
												self.current_retry_count + '}')
			else:
				# Get the `END_TIME` for the `DOWNLOAD` activity,
				# for traceback / logging purposes.
				# This is noted only for successful downloads.
				self.task_end_time = time.ctime()

				# Set the `DOWNLOAD` success flag to `TRUE.`
				self.task_successful = True

				# Logging a comment
				task_manager_logger.info('[Class: {' + str(self.__class__) + '}] Download Successfully Completed')

				# Return below dictionary, iff `BUILD` is for `TOMCAT`.
				if build_for == helpers.BuildConfig.Tomcat.TomcatConfig.ENVIRONMENT['BUILD_TARGET']:
					# Return the `TAR` package names.
					# These would be used by the `UNTAR` module
					# to extract the files to the local / shared filesystem(s).
					return {helpers.BuildConfig.Java.JavaConfig.JAVA_TAR_COMPONENT_NAME:
											thread_for[helpers.BuildConfig.Java.JavaConfig.JAVA_COMPONENT_NAME].tar_file_name,
								helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_TAR_COMPONENT_NAME:
											thread_for[helpers.BuildConfig.Tomcat.TomcatConfig.TOMCAT_COMPONENT_NAME].tar_file_name}

###########################################
# Untar Manager Model for extracting
# dependencies and target software for the
# `AUTOMATED` software build.
###########################################

class UntarManager(TaskManager):
	"""
	Class blueprint for creating `UNTAR` agent(s) for the build. These instances / agents will
	handle the entire dependency and target software extraction for the automated
	build. To make the extractions more time efficient, we are using the `THREADING` module
	that the Python Standard Library provides. This allows us for concurrent simultaneous
	extraction, which when done sequentially takes a lot of time.
	"""

	def begin(self, tar_binaries):
		"""
		The `BEGIN` method takes care of the `TAR` package extractions.
		Puts them under the `CONFIGURED` or `DEFAULT` directory accordingly.

		PARAMETER:=> TAR_BINARIES = A dictionary object consisting of dependent task rules and other details.

		`TAR_BINARIES` is a dictionary. It contains the `THREAD-NAME` and
		`THREAD-WORKER` logic that is to be simultaneously executed.
		"""
		# Keeps a handle to the newly spawned threads.
		# Makes it easy for the caller to inspect the
		# threads and also for accessing their state
		# post execution.
		thread_for = {}

		while not self.task_successful and self.allow_retry():
			try:
				# Instantiate the `QUEUE` exception stacktrace object for the spawned threads.
				exception_stacktrace_queue = queue.Queue()

				# Logging a comment
				task_manager_logger.info('[Class: {' + str(self.__class__) + '}] Instantiating Extraction Threads...')

				for component in list(tar_binaries.keys()):
					if self.initial_run or component in self.failed_thread_list:
						untar_thread = \
								tar_binaries[component]['thread_worker'](name=tar_binaries[component]['thread_name'],
														args=(tar_binaries[component]['thread_args']['tar_file_name'],
																exception_stacktrace_queue,
																	tar_binaries[component]['thread_args']['tar_package_type'],))
						thread_for[component] = untar_thread

						# Logging a comment
						task_manager_logger.info('[Class: {' + str(self.__class__) + '}] Instantiated Extraction Thread: {' +
														untar_thread.getName() + '}')

						# Start the `THREAD`.
						untar_thread.start()

				# The below method makes the main thread (or process) to block
				# until the minion `THREAD`s complete their tasks.
				# This would in turn block the `BEGIN` method from returning
				# back to the caller.
				the_main_thread = threading.main_thread()

				for active_thread in threading.enumerate():
					# If we `JOIN` the main thread of execution,
					# it will introduce a deadlock. Hence, that
					# needs to be skipped.
					if active_thread is the_main_thread:
						continue

					# `JOIN` all the other active threads.
					# It will block the main thread from exiting, i.e.,
					# it waits for the chilren threads to finish their
					# execution.
					active_thread.join()

				# Check the Exception Stack and re-raise the exception (If Any).
				# The below statement is reached only after the threads finish
				# their work either normally or abnormally.
				if not exception_stacktrace_queue.empty():
					# Get the first exception element and raise the same.
					# Once, the exception is raised (if any), the exception
					# handler will handle the overall exceptions raised by the
					# spawned threads by checking their status flags.
					raise exception_stacktrace_queue.get()

			except (tarfile.TarError, IOError, OSError) as taskManager_untarManager_error:
				# Put logging below.
				task_manager_logger.error('[Class: {' + str(self.__class__) + '}] Extraction Operation Failed: ' +
												str(taskManager_untarManager_error))

				# Delete the exception stacktrace queue
				# before continuing with the next iteration of
				# trials. This stacktrace object just lets us
				# identify whether any exception(s) occurred in any of
				# the spawned threads. Once we confirm that an exception
				# has occurred, we check the status of all the threads
				# spawned by the `UNTAR_MANAGER` process and put them
				# up for retry only if that particular thread failed during
				# its execution.
				del exception_stacktrace_queue

				# It's past its `INITIAL_RUN` now.
				# Mark it as `FALSE`.
				self.initial_run = False

				# Iterate over the spawned `THREAD` list dictionary.
				# Check for each `THREAD`'s completion status.
				# If completion status is `UNSET` (or False), add it to the
				# failed thread list.
				for component in list(thread_for.keys()):
					if not thread_for[component].untar_complete:
						# Logging a comment
						task_manager_logger.critical('[Class: {' + str(self.__class__) +
												'}] Extraction Thread Failed for Component: {' +
															component + '}')

						# We don't want to re-add the component, if it is
						# already present in the below list.
						# Otherwise, it would spawn multiple `THREAD`s for
						# the same component.
						if component not in self.failed_thread_list:
							self.failed_thread_list.append(component)

				# Check if the `EXTRACTION` operation succeeded after the specified number of retries (If any).
				# Raise the error if it failed for more than the specified value of `RETRY`.
				if self.current_retry_count > self.retries_allowed():
					# Logging a comment
					task_manager_logger.critical('[Class: {' + str(self.__class__) + '}] Maximum Retries Exceeded. Please \
														run a Diagnostic for probable issues.')
					raise

				# Logging a comment
				task_manager_logger.info('[Class: {' + str(self.__class__) + '}] Current Extraction Retry Count: {' +
												self.current_retry_count + '}')
			else:
				# Get the `END_TIME` for the `UNTAR` activity,
				# for traceback / logging purposes.
				# This is noted only for successful extractions.
				self.task_end_time = time.ctime()

				# Set the `UNTAR` success flag to `TRUE.`
				self.task_successful = True

				# Logging a comment
				task_manager_logger.info('[Class: {' + str(self.__class__) + '}] Extraction Successfully Completed')