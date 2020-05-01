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
Hook that loads defines all the available actions, broken down by publish type.
"""

import os
import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class MayaActions(HookBaseClass):
    def _create_reference(self, path, sg_publish_data):
        """
        Create a reference with the same settings Maya would use
        if you used the create settings dialog.

        :param path: Path to file.
        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields.
        """
        file_path = self._ensure_file_is_local(path, sg_publish_data)

        # Now the file is downloaded we can let the base functionality run.
        super(MayaActions, self)._create_reference(file_path, sg_publish_data)

    def _do_import(self, path, sg_publish_data):
        """
        Create a reference with the same settings Maya would use
        if you used the create settings dialog.

        :param path: Path to file.
        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields.
        """
        file_path = self._ensure_file_is_local(path, sg_publish_data)

        # Now the file is downloaded we can let the base functionality run.
        super(MayaActions, self)._do_import(file_path, sg_publish_data)

    def _ensure_file_is_local(self, path, published_file):
        """
        Given a PublishedFile entity dictionary and a path
        It will attempt to download the file if it is not already downloaded.
        :param path:
        :param published_file:
        :return:
        """
        if os.path.exists(path):
            # file already exists locally
            return path

        remote_storage = self.load_framework("tk-framework-remotestorage_v1.x.x")
        downloaded_file = remote_storage.download_publish(published_file)

        if downloaded_file is None:
            # We haven't downloaded a file, and the path doesn't already exist
            # We can't import it.
            raise Exception(
                "The PublishedFile %s could not be downloaded and does not exist "
                "locally, so could not be imported; file: %s"
                % (published_file["id"], path)
            )

        if downloaded_file is not None and downloaded_file != path:
            # The example remote storage hook behaviour is to download to the exact same
            # location that the file was published to.
            raise Exception(
                "The downloaded file path does not match the original "
                "published one; original: %s downloaded: %s" % (path, downloaded_file)
            )
        return downloaded_file
