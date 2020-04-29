# Copyright (c) 2020 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
A framework that handles uploading and downloading of files from a cloud storage provider.
"""

import sgtk

class RemoteStorageFramework(sgtk.platform.Framework):

    def init_framework(self):
        """
        Called when the Framework is initialized.
        """
        self._progress_dialog = None
        if self.engine.has_ui:
            ph = self.import_module("progress_handler")
            self._progress_dialog = ph.ProgressNotificationDialog()

    def _show_download_msg(self, msg):
        """
        Shows a modal pop up message to the user, around downloading.
        :param msg: str
        """
        if self._progress_dialog:
            self._progress_dialog.show_download_msg(msg)

    def _show_upload_msg(self, msg):
        """
        Shows a modal pop up message to the user, around uploading.
        :param msg: str
        """
        if self._progress_dialog:
            self._progress_dialog.show_upload_msg(msg)

    def _close_progress_dialog(self):
        """
        closes the pop up dialog,
        Should be called after remote process has finished, and you need to remove the dialog.
        """
        if self._progress_dialog:
            self._progress_dialog.close()

    def upload_publish(self, published_file):
        """
        Uploads a PublishedFile's path to the remote storage.
        :param published_file: dict
        :return: str path to uploaded file
        """
        paths = self.upload_publishes([published_file])[0]
        return paths[0] if len(paths) else None

    def upload_publishes(self, published_files):
        """
        Uploads a list of PublishedFile's paths to the remote storage.
        :param published_files: list of dicts
        :return: list of strings to the uploaded files
        """
        uploaded_files = []
        try:
            for published_file in published_files:
                self._show_download_msg("Sending to remote: %s ..." % published_file["code"])
                self.logger.debug("Executing upload hook for %s" % published_file)
                uploaded_files.append(self.execute_hook_method("provider_hook",
                                                               "upload",
                                                               published_file=published_file))
        finally:
            self._close_progress_dialog()
        return uploaded_files

    def download_publish(self, published_file):
        """
        Downloads a list of PublishedFiles from the remote storage to the local storage.
        :param published_file: dict
        :return: str path to the downloaded file.
        """
        paths = self.download_publishes([published_file])
        return paths[0] if len(paths) else None

    def download_publishes(self, published_files):
        """
        Downloads a list of PublishedFiles from the remote storage to the local storage.
        :param published_files: list of dicts
        :return: list of strings of paths to the downloaded files.
        """
        downloaded_files = []
        import time
        try:
            for published_file in published_files:
                self._show_download_msg("Retrieving from remote: %s ..." % published_file["code"])
                self.logger.debug("Executing download hook for %s" % published_file)
                time.sleep(15)
                downloaded_files.append(self.execute_hook_method("provider_hook",
                                                             "download",
                                                             published_file=published_file))
        finally:
            self._close_progress_dialog()
        return downloaded_files
    
