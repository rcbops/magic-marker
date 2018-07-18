#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
from magic_marker import cli


def test_magic_marker_happy_path(tmpdir_factory):
    unmarked_test = """
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

    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(unmarked_test)
    with open(file_path, 'r') as f:
        original_data = f.readlines()

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "test_this_is_a_test.py : 1 test marked with UUID" in result.output
    with open(file_path, 'r') as f:
        observed_data = f.readlines()
    change = list(set(observed_data) - set(original_data))
    assert len(change) == 1
    assert "@pytest.mark.test_id(" in change[0]


def test_magic_marker_happy_path_two_tests(tmpdir_factory):
    unmarked_test = """
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

    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(unmarked_test)
    with open(file_path, 'r') as f:
        original_data = f.readlines()

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "test_this_is_a_test.py : 2 tests marked with UUID" in result.output
    with open(file_path, 'r') as f:
        observed_data = f.readlines()
    change = list(set(observed_data) - set(original_data))
    assert len(change) == 2
    assert "@pytest.mark.test_id(" in change[0]


def test_magic_marker_no_changes_necessary(tmpdir_factory):
    unmarked_test = """
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

    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(unmarked_test)
    with open(file_path, 'r') as f:
        original_data = f.readlines()

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "No changes made" in result.output
    with open(file_path, 'r') as f:
        observed_data = f.readlines()
    change = list(set(observed_data) - set(original_data))
    assert len(change) == 0


def test_magic_marker_mark_one(tmpdir_factory):
    unmarked_test = """
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

    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(unmarked_test)
    with open(file_path, 'r') as f:
        original_data = f.readlines()

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "test_this_is_a_test.py : 1 test marked with UUID" in result.output
    with open(file_path, 'r') as f:
        observed_data = f.readlines()
    change = list(set(observed_data) - set(original_data))
    assert len(change) == 1


def test_magic_marker_with_whitespace(tmpdir_factory):
    unmarked_test = """
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

    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(unmarked_test)
    with open(file_path, 'r') as f:
        original_data = f.readlines()

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "test_this_is_a_test.py : 1 test marked with UUID" in result.output
    with open(file_path, 'r') as f:
        observed_data = f.readlines()
    change = list(set(observed_data) - set(original_data))
    assert len(change) == 1
    assert change[0][0:4] == '    '
