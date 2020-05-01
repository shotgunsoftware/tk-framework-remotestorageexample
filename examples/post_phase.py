# Copyright (c) 2020 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from pprint import pformat
import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class PostPhaseHook(HookBaseClass):
    """
    This hook defines methods that are executed after each phase of a publish:
    validation, publish, and finalization. Each method receives the publish
    tree instance being used by the publisher, giving full control to further
    curate the publish tree including the publish items and the tasks attached
    to them. See the :class:`PublishTree` documentation for additional details
    on how to traverse the tree and manipulate it.
    """

    # See the developer docs for more information about the methods that can be
    # defined here: https://developer.shotgunsoftware.com/tk-multi-publish2/

    def post_finalize(self, publish_tree):
        remote_storage = self.load_framework("tk-framework-remotestorage_v1.x.x")

        # loop over all items and try and extract out the sg_publish_data if we can.
        # TODO: check that publishes with the same path have same id
        published_files = {}
        for item in publish_tree:
            p_data = self.get_published_file_data(item)
            self.logger.info("p_data %s" % p_data)
            if p_data:
                published_files[p_data["id"]] = p_data
            for child_item in item.descendants:
                c_p_data = self.get_published_file_data(child_item)
                self.logger.info("c_p_data %s" % c_p_data)
                if c_p_data:
                    published_files[c_p_data["id"]] = c_p_data

        self.logger.info(
            "Uploading the following published files: %s" % pformat(published_files)
        )
        remote_storage.upload_publishes(list(published_files.values()))

    def get_published_file_data(self, item):
        if hasattr(item.properties, "sg_publish_data"):
            return item.properties.sg_publish_data
        return None
