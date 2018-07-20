#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
from magic_marker import cli
import re


def test_magic_marker_happy_path(one_test_unmarked, uuid_patch, mocker):
    """Test the happy path"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)

    runner = CliRunner()
    cli_arguments = [one_test_unmarked.path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "one_test_unmarked.py : 1 test marked with UUID" in result.output
    with open(one_test_unmarked.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == one_test_unmarked.expected


def test_magic_marker_happy_path_two_tests(two_tests_unmarked, uuid_patch, mocker):
    """Test marking two tests in the same file"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)

    runner = CliRunner()
    cli_arguments = [two_tests_unmarked.path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "two_tests_unmarked.py : 2 tests marked with UUID" in result.output
    with open(two_tests_unmarked.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == two_tests_unmarked.expected


def test_magic_marker_no_changes_necessary(none_unmarked):
    """Test when there are no changes expected"""

    runner = CliRunner()
    cli_arguments = [none_unmarked.path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "No changes made" in result.output
    with open(none_unmarked.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == none_unmarked.expected


def test_magic_marker_mark_one(one_of_two_unmarked, uuid_patch, mocker):
    """Test only marking one of two tests"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)

    runner = CliRunner()
    cli_arguments = [one_of_two_unmarked.path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "one_of_two_unmarked.py : 1 test marked with UUID" in result.output
    with open(one_of_two_unmarked.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == one_of_two_unmarked.expected


def test_magic_marker_with_whitespace(inside_a_class, uuid_patch, mocker):
    """Test when a test is defined inside a class"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)

    runner = CliRunner()
    cli_arguments = [inside_a_class.path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "inside_a_class.py : 1 test marked with UUID" in result.output
    with open(inside_a_class.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == inside_a_class.expected


def test_backup(inside_a_class):
    """Test that a target is copied to a backup location"""

    runner = CliRunner()
    cli_arguments = [inside_a_class.path, 'test_id']
    result = runner.invoke(cli.main, args=cli_arguments)
    assert result.exit_code == 0
    backup_regex = re.compile('^A backup was created : (.*)$', re.MULTILINE)
    path = backup_regex.search(str(result.output)).group(1)
    with open(path, 'r') as f:
        observed_data = f.read()
    assert observed_data == inside_a_class.original
