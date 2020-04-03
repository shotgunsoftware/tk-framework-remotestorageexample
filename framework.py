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

    def upload_publish(self, published_file):
        return self.upload_publishes([published_file])[0]

    def upload_publishes(self, published_files):
        uploaded_files = []
        for published_file in published_files:
            uploaded_files.append(self.execute_hook_method("provider_hook",
                                                           "upload",
                                                           published_file=published_file))
        return uploaded_files

    def download_publish(self, published_file):
        return self.download_publishes([published_file])[0]

    def download_publishes(self, published_files):
        downloaded_files = []
        for published_file in published_files:
            downloaded_files.append(self.execute_hook_method("provider_hook",
                                                             "download",
                                                             published_file=published_file))
        return downloaded_files
