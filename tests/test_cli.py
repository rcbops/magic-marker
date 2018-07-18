#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
from magic_marker import cli
import re


def test_magic_marker_happy_path(tmpdir_factory, one_test_unmarked, uuid_patch, mocker):
    """Test the happy path"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)
    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(one_test_unmarked.original)

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "test_this_is_a_test.py : 1 test marked with UUID" in result.output
    with open(file_path, 'r') as f:
        observed_data = f.read()
    assert observed_data == one_test_unmarked.expected


def test_magic_marker_happy_path_two_tests(tmpdir_factory, two_tests_unmarked, uuid_patch, mocker):
    """Test marking two tests in the same file"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)
    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(two_tests_unmarked.original)

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "test_this_is_a_test.py : 2 tests marked with UUID" in result.output
    with open(file_path, 'r') as f:
        observed_data = f.read()
    assert observed_data == two_tests_unmarked.expected


def test_magic_marker_no_changes_necessary(tmpdir_factory, none_unmarked):
    """Test when there are no changes expected"""

    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(none_unmarked.original)

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "No changes made" in result.output
    with open(file_path, 'r') as f:
        observed_data = f.read()
    assert observed_data == none_unmarked.expected


def test_magic_marker_mark_one(tmpdir_factory, one_of_two_unmarked, uuid_patch, mocker):
    """Test only marking one of two tests"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)
    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(one_of_two_unmarked.original)

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "test_this_is_a_test.py : 1 test marked with UUID" in result.output
    with open(file_path, 'r') as f:
        observed_data = f.read()
    assert observed_data == one_of_two_unmarked.expected


def test_magic_marker_with_whitespace(tmpdir_factory, inside_a_class, uuid_patch, mocker):
    """Test when a test is defined inside a class"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)
    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(inside_a_class.original)

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "test_this_is_a_test.py : 1 test marked with UUID" in result.output
    with open(file_path, 'r') as f:
        observed_data = f.read()
    assert observed_data == inside_a_class.expected


def test_backup(tmpdir_factory, inside_a_class):
    """Test that a target is copied to a backup location"""
    file_path = tmpdir_factory.mktemp('test').join('test_this_is_a_test.py').strpath
    with open(file_path, 'w') as f:
        f.write(inside_a_class.original)

    runner = CliRunner()
    cli_arguments = [file_path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)
    assert result.exit_code == 0
    backup_regex = re.compile('^A backup was created : (.*)$', re.MULTILINE)
    path = backup_regex.search(str(result.output)).group(1)
    with open(path, 'r') as f:
        observed_data = f.read()
    assert observed_data == inside_a_class.original
