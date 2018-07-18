# -*- coding: utf-8 -*-

"""MagicMarker is a tool that automatically marks pytests with a UUID"""
# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
from flake8.main.cli import main as flake8_main
from contextlib import contextmanager
from os import fdopen, remove
import sys
import six
import tempfile
import json
import uuid
import re


class MagicMarker(object):

    def __init__(self, **kwargs):
        """Crate a new MagicMarker object
        You must supply directory or data

        Args:
            mark (str): The mark to create
            directory (str): The directory to target for the fix, optional
            data (str): The parsed json data from flake8-json, optional

        """
        self._mark = kwargs['mark']
        try:
            self._directory = kwargs['directory']
        except KeyError:
            pass
        try:
            self._json_data = kwargs['data']
        except KeyError:
            pass

    def run_flake8_and_mark(self):
        """Run flak8 and edit and fix errors

        Returns:
            Str: the message stating what was performed
        """
        flake8_config = """
[flake8]
pytest_mark1 = name={}
               value_match=uuid
            """.format(self._mark)

        file_handle, path = tempfile.mkstemp(text=True)

        with fdopen(file_handle, 'w') as config:
            config.write(flake8_config)

        args = [
            'flake8',
            self._directory,
            "--config={}".format(path),
            "--format=json",
            "--select=M501"  # only covers case of no mark present
        ]

        with self.patch_sys_argv(args), self.captured_stdout() as stdout:
            try:
                flake8_main()
            except SystemExit:
                pass  # This is raised by flake8
        remove(path)
        full_output = json.loads(stdout.getvalue())
        return self.fix_it(full_output)

    def fix_it(self, flake8_output):
        """Perform the fix

        Args:
            flake8_output (dict[list[dict]]): parsed output from flake8-json

        Returns:
            Str: the message stating what was performed
        """
        message = ""
        for file_path in flake8_output:
            if flake8_output[file_path]:
                filname, fixcount = self._fix_file(flake8_output[file_path])
                if fixcount == 1:
                    message += "\n{} : {} test marked with UUID".format(filname, fixcount)
                else:
                    message += "\n{} : {} tests marked with UUID".format(filname, fixcount)
        if message:
            return message
        else:
            return "No changes made"

    def _fix_file(self, fixes_required):
        """Fixes an individual file

        Args:
            fixes_required (list[dict]): a list of the fixes required for this file

        Returns:
            Tuple (str, str):  filename and number of fixes performed
        """
        filename = str(fixes_required[0]['filename'])
        with open(filename, 'r') as f:
            data = f.readlines()

        fixes_required.sort(key=lambda x: x['line_number'])
        fixes_required.reverse()  # work from the bottom of the file up
        for fix in fixes_required:
            fix_position = fix['line_number']
            if fix_position:
                fix_position += -1
            mark = self._match_indent(data[fix_position], self._uuid_mark())
            data.insert(fix_position, mark)

        with open(filename, 'w') as f:
            f.writelines(data)
        return filename, len(fixes_required)

    def _uuid_mark(self):
        """generate a UUID mark string

        Returns:
            Str: the correctly formatted UUID mark string
        """
        return "@pytest.mark.{}(\"{}\")\n".format(self._mark, str(uuid.uuid1()))

    def _match_indent(self, def_string, target_line):
        """Match the indent of the original string

        Args:
            def_string (str): the original string from the test definition
            target_line (str): the string that should be updated

        Returns:
            Str : The new string updated with correct whitespace
        """
        regex = re.compile('(^\s*)')
        whitespace = re.match(regex, def_string).groups(1)
        if whitespace:
            target_line = whitespace[0] + target_line
        return target_line

    @contextmanager
    def patch_sys_argv(self, new_argv):
        """"""
        orig = sys.argv
        sys.argv = new_argv
        yield
        sys.argv = orig

    @contextmanager
    def captured_output(self, stream_name):
        """Return a context manager used by captured_stdout/stdin/stderr
        that temporarily replaces the sys stream *stream_name* with a StringIO.

        Args:
            stream_name (str): The name of the stream to capture

        Note: This function and the following ``captured_std*`` are copied
              from CPython's ``test.support`` module."""
        orig_stdout = getattr(sys, stream_name)
        setattr(sys, stream_name, six.StringIO())
        try:
            yield getattr(sys, stream_name)
        finally:
            setattr(sys, stream_name, orig_stdout)

    def captured_stdout(self):
        """Capture the output of sys.stdout:
           with captured_stdout() as stdout:
               print("hello")
           self.assertEqual(stdout.getvalue(), "hello\n")

        Returns:
            GeneratorContextManager
        """
        return self.captured_output("stdout")
