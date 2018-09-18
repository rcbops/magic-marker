# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
import uuid


class Fixes(object):
    """A class containing fixes"""

    @classmethod
    def uuid(cls, mark_name):
        """The fix for a mark with a UUID"""
        return "@pytest.mark.{}('{}')\n".format(mark_name, str(uuid.uuid1()))

    @classmethod
    def empty_value(cls, mark_name):
        """The fix for a mark with a empty_value"""
        return "@pytest.mark.{}()\n".format(mark_name)
