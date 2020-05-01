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


class LocalProvider(HookBaseClass):

    """
    This hooks is just an example hook that doesn't actually upload anything,
    but instead copies thee files to a location, and then retrieves them on download.
    """

    remote_storage_location = "$HOME/mock_remote_storage"

    def upload(self, published_file):
        """
        This method should contain any logic for uploading the file to the remote storage.
        Its recommended that when you upload the file you prefix the file name with the id
        so that given a PublishedFile entity you could find it and download it again without
        needing to store an explicit reference to the uploaded file in Shotgun.
        :param published_file: dict PublishedFile entity.
        :return: str path to uploaded file, None if it fails.
        """
        self.logger.info("uploading %s" % published_file)

        if (
            "path" in published_file
            and "local_path" in published_file["path"]
            and published_file["path"]["local_path"]
        ):
            # Build a path to copy the published file to in our mocked remote storage.
            destination_path = self._generate_remote_path(published_file)
            self.logger.info("mock uploading file to %s" % destination_path)
            if os.path.exists(destination_path):
                self.logger.warning(
                    "PublishedFile already exists in remote location: %s"
                    % published_file
                )
                return

            sgtk.util.filesystem.copy_file(
                published_file["path"]["local_path"], destination_path
            )
            return destination_path

        self.logger.warning(
            "No local file path found on PublishedFile: %s" % published_file
        )

    def download(self, published_file):
        """
        Downloads the PublishedFile from the remote storage.
        This method is responsible for finding the file in the remote storage based on
        the passed published_file.
        :param published_file: dict, PublishedFile entity.
        :return: str; The path to the downloaded file.
        """
        self.logger.info("downloading %s" % published_file)

        remote_path = self._generate_remote_path(published_file)
        if not os.path.exists(remote_path):
            self.logger.warning(
                "PublishedFile %s could not be found in the remote storage."
                % published_file["id"]
            )
            return None

        # TODO: maybe try and resolve the path rather than expecting to be able to place
        #  it back in exactly the same location that it was when it was published
        destination = published_file["path"]["local_path"]

        if os.path.exists(destination):
            self.logger.warning(
                "PublishedFile %s already exists locally here: %s"
                % (published_file["id"], destination)
            )
            return

        sgtk.util.filesystem.copy_file(remote_path, destination)
        return destination

    def _generate_remote_path(self, published_file):
        """
        Works out the path for the file on the remote storage.
        (This is not a required hook method)
        :param published_file:
        :return:
        """
        # Ext is usually included in the name so we are not explicitly setting it here.
        file_name = "{id}_{name}".format(
            id=published_file["id"], name=published_file["name"]
        )
        return os.path.join(os.path.expandvars(self.remote_storage_location), file_name)
