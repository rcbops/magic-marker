# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
from magic_marker.fixes import Fixes


class Fixable(object):
    """A class to tell if a mark is fixable
    """

    def __init__(self):
        """Create a fixable object"""
        self._fix_functions = (self._uuid, self._empty_value)

    def check(self, flake8_outline, mark_configuration):
        """Check if a mark is fixable by any of the functions known

        Args:
            mark_configuration

        Returns:
            @classmethod from the Fixes class
        """
        for func in self._fix_functions:
            f = func(flake8_outline, mark_configuration)
            if f:
                return f
        return None, None

    def _pull_mark_config_name_from_output(self, out_line):
        return 'pytest_mark{}'.format(int(out_line['code'][-2:]))

    def _uuid(self, flake8_out_line, mark_configuration):
        """Check if a mark is fixable by the UUID schema
        If it is fixable tell how to fix it
        """
        try:
            name = mark_configuration[self._pull_mark_config_name_from_output(flake8_out_line)]['name']
            if mark_configuration[self._pull_mark_config_name_from_output(flake8_out_line)]['value_match'] == 'uuid':
                return name, Fixes.uuid  # not sure if this will work or not
        except KeyError:
            pass

    def _empty_value(self, flake8_out_line, mark_configuration):
        """Check if a mark can be fixed
        mark must not require a value
        """
        try:
            name = mark_configuration[self._pull_mark_config_name_from_output(flake8_out_line)]['name']
            if name == 'test_case_with_steps':  # hard code this hack until this can be configured
                return name, Fixes.empty_value  # not sure if this will work or not
        except KeyError:
            pass
