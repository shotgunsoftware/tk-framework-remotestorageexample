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
Hook that provides upload and download functionality for the cloud storage provider.
"""
import os
import sgtk

HookBaseClass = sgtk.get_hook_baseclass()

class TemplateProvider(HookBaseClass):

    """
    This hooks is just an template hook that doesn't actually implement any upload or download behaviour.
    """

    def upload(self, published_file):
        """
        This method should contain any logic for uploading the file to the remote storage.
        Its recommended that when you upload the file you prefix the file name with the id
        so that given a PublishedFile entity you could find it and download it again without
        needing to store an explicit reference to the uploaded file in Shotgun.
        :param published_file: dict PublishedFile entity.
        :return: str path to uploaded file, None if it fails.
        """
        return

    def download(self, published_file):
        """
        Downloads the PublishedFile from the remote storage.
        This method is responsible for finding the file in the remote storage based on
        the passed published_file.
        :param published_file: dict, PublishedFile entity.
        :return: str; The path to the downloaded file.
        """
        return
