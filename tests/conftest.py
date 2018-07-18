# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
import pytest


@pytest.fixture(scope='session')
def uuid_patch():
    return 'b360c12d-0d47-4cfc-9f9e-5d86c315b1e4'


@pytest.fixture(scope='session')
def one_test_unmarked():
    original = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
import tempfile
import json


def test_i_am_not_marked():
    pass

"""
    expected = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
import tempfile
import json


@pytest.mark.test_id('{}')
def test_i_am_not_marked():
    pass

""".format(uuid_patch())
    return OriginalAndExpected(original=original, expected=expected)


@pytest.fixture(scope='session')
def two_tests_unmarked():
    original = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
import tempfile
import json


def test_i_am_not_marked():
    pass


def test_i_am_also_not_marked():
    pass

"""
    expected = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
import tempfile
import json


@pytest.mark.test_id('{}')
def test_i_am_not_marked():
    pass


@pytest.mark.test_id('{}')
def test_i_am_also_not_marked():
    pass

""".format(uuid_patch(), uuid_patch())
    return OriginalAndExpected(original=original, expected=expected)


@pytest.fixture(scope='session')
def one_of_two_unmarked():
    original = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
import tempfile
import json


@pytest.mark.foo('bar')
@pytest.mark.bar('foo')
def test_i_am_not_marked():
    pass


@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
@pytest.mark.foo('baz')
def test_i_am_also_not_marked():
    pass

"""

    expected = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
import tempfile
import json


@pytest.mark.test_id('{}')
@pytest.mark.foo('bar')
@pytest.mark.bar('foo')
def test_i_am_not_marked():
    pass


@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
@pytest.mark.foo('baz')
def test_i_am_also_not_marked():
    pass

""".format(uuid_patch())
    return OriginalAndExpected(original=original, expected=expected)


@pytest.fixture(scope='session')
def none_unmarked():
    original = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
import tempfile
import json

@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
def test_i_am_not_marked():
    pass

@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
def test_i_am_also_not_marked():
    pass

"""
    return OriginalAndExpected(original=original, expected=original)


@pytest.fixture(scope='session')
def inside_a_class():
    original = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
import tempfile
import json

class TestFooBar(object):

    @pytest.mark.foo('bar')
    @pytest.mark.bar('foo')
    def test_i_am_not_marked():
        pass

    @pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
    @pytest.mark.foo('baz')
    def test_i_am_also_not_marked():
        pass

"""

    expected = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
import tempfile
import json

class TestFooBar(object):

    @pytest.mark.test_id('{}')
    @pytest.mark.foo('bar')
    @pytest.mark.bar('foo')
    def test_i_am_not_marked():
        pass

    @pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
    @pytest.mark.foo('baz')
    def test_i_am_also_not_marked():
        pass

""".format(uuid_patch())
    return OriginalAndExpected(original=original, expected=expected)


class OriginalAndExpected(object):
    """Contains the value before a test and the expectation"""

    def __init__(self, **kwargs):
        """Creates a new OriginalAndExpected Object
        Takes two strings, used to compare after test is complete

        Args:
            :param original (str)
            :param expected (str
        """
        self._original = kwargs['original']
        self._expected = kwargs['expected']

    @property
    def original(self):
        """The original value

        Returns:
            str
        """
        return self._original

    @property
    def expected(self):
        """The expected value

        Returns:
            str
        """
        return self._expected
