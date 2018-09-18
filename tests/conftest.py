# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
import pytest


@pytest.fixture(scope='session')
def uuid_patch():
    return 'b360c12d-0d47-4cfc-9f9e-5d86c315b1e4'


@pytest.fixture()
def one_test_unmarked(tmpdir_factory):
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
    return OriginalAndExpected(original=original,
                               expected=expected,
                               tmpdir_factory=tmpdir_factory,
                               name='one_test_unmarked.py')


@pytest.fixture()
def two_tests_unmarked(tmpdir_factory):
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
    return OriginalAndExpected(original=original,
                               expected=expected,
                               tmpdir_factory=tmpdir_factory,
                               name='two_tests_unmarked.py')


@pytest.fixture()
def one_of_two_unmarked(tmpdir_factory):
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
    return OriginalAndExpected(original=original,
                               expected=expected,
                               tmpdir_factory=tmpdir_factory,
                               name='one_of_two_unmarked.py')


@pytest.fixture()
def none_unmarked(tmpdir_factory):
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
    return OriginalAndExpected(original=original,
                               expected=original,
                               tmpdir_factory=tmpdir_factory,
                               name='none_unmarked.py')


@pytest.fixture()
def inside_a_class(tmpdir_factory):
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
    return OriginalAndExpected(original=original,
                               expected=expected,
                               tmpdir_factory=tmpdir_factory,
                               name='inside_a_class.py')


@pytest.fixture()
def stepped_class_workflow(tmpdir_factory):
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

    @pytest.mark.foo('baz')
    def test_i_am_also_not_marked():
        pass


class TestBaz(object):

    @pytest.mark.foo('bar')
    @pytest.mark.bar('foo')
    def test_i_am_not_marked():
        pass

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

@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
@pytest.mark.test_case_with_steps()
class TestFooBar(object):

    @pytest.mark.foo('bar')
    @pytest.mark.bar('foo')
    def test_i_am_not_marked():
        pass

    @pytest.mark.foo('baz')
    def test_i_am_also_not_marked():
        pass


@pytest.mark.test_id('b360c12d-0d47-4cfc-9f9e-5d86c315b1e4')
@pytest.mark.test_case_with_steps()
class TestBaz(object):

    @pytest.mark.foo('bar')
    @pytest.mark.bar('foo')
    def test_i_am_not_marked():
        pass

    @pytest.mark.foo('baz')
    def test_i_am_also_not_marked():
        pass

""".format(uuid_patch())
    return OriginalAndExpected(original=original,
                               expected=expected,
                               tmpdir_factory=tmpdir_factory,
                               name='stepped_class_workflow.py')


@pytest.fixture()
def stepped_class_config(tmpdir_factory):
    config = """
[flake8]
ignore = E501
pytest_mark1 = name=test_id,
               value_match=uuid,
               enforce_unique_value=true,
               exclude_functions=true,
pytest_mark2 = name=jira,
               regex_match=[a-zA-Z]+-\d+,
               allow_multiple_args=true,
               exclude_functions=true
pytest_mark3 = name=test_case_with_steps,
               exclude_methods=true,
               exclude_functions=true,
               exclude_classes=false
filename_check1 = filter_regex=test_.+,
                  filename_regex=test_[\w-]+$
    """
    path = tmpdir_factory.mktemp('data').join('basic_config').strpath
    with open(path, 'w') as f:
        f.write(config)
    return path


@pytest.fixture()
def original_behavior_config(tmpdir_factory):
    config = """
[flake8]
ignore = E501
pytest_mark1 = name=test_id,
               value_match=uuid,
               enforce_unique_value=true,
               exclude_classes=true,
pytest_mark2 = name=jira,
               regex_match=[a-zA-Z]+-\d+,
               allow_multiple_args=true,
               exclude_classes=true
filename_check1 = filter_regex=test_.+,
                  filename_regex=test_[\w-]+$
    """
    path = tmpdir_factory.mktemp('data').join('basic_config').strpath
    with open(path, 'w') as f:
        f.write(config)
    return path


class OriginalAndExpected(object):
    """Contains the value before a test and the expectation"""

    def __init__(self, **kwargs):
        """Creates a new OriginalAndExpected Object
        Takes two strings, used to compare after test is complete

        Args:
            :param original (str)
            :param expected (str)
            :param tmpdir_factory (tmpdir_factory)
            :param name (str)
        """
        self._original = kwargs['original']
        self._expected = kwargs['expected']
        self._path = kwargs['tmpdir_factory'].mktemp('data').join(kwargs['name']).strpath
        with open(self._path, 'w') as f:
            f.write(self._original)

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

    @property
    def path(self):
        """The path of the original file

        Returns:
            str
        """
        return self._path
