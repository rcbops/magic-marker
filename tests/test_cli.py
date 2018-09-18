#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
from click.testing import CliRunner
from magic_marker import cli
import re


def test_magic_marker_happy_path(one_test_unmarked, original_behavior_config, uuid_patch, mocker):
    """Test the happy path"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)

    runner = CliRunner()
    cli_arguments = ["--config={}".format(original_behavior_config), one_test_unmarked.path]
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "one_test_unmarked.py : 1 test mark added" in result.output
    with open(one_test_unmarked.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == one_test_unmarked.expected


def test_magic_marker_happy_path_two_tests(two_tests_unmarked, original_behavior_config, uuid_patch, mocker):
    """Test marking two tests in the same file"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)

    runner = CliRunner()
    cli_arguments = ["--config={}".format(original_behavior_config), two_tests_unmarked.path]
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "two_tests_unmarked.py : 2 test marks added" in result.output
    with open(two_tests_unmarked.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == two_tests_unmarked.expected


def test_magic_marker_no_changes_necessary(none_unmarked, original_behavior_config):
    """Test when there are no changes expected"""

    runner = CliRunner()
    cli_arguments = ["--config={}".format(original_behavior_config), none_unmarked.path]
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "0 test marks added" in result.output
    with open(none_unmarked.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == none_unmarked.expected


def test_magic_marker_mark_one(one_of_two_unmarked, original_behavior_config, uuid_patch, mocker):
    """Test only marking one of two tests"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)

    runner = CliRunner()
    cli_arguments = ["--config={}".format(original_behavior_config), one_of_two_unmarked.path]
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "one_of_two_unmarked.py : 1 test mark added" in result.output
    with open(one_of_two_unmarked.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == one_of_two_unmarked.expected


def test_magic_marker_with_whitespace(inside_a_class, original_behavior_config, uuid_patch, mocker):
    """Test when a test is defined inside a class"""

    mocker.patch('uuid.uuid1', return_value=uuid_patch)

    runner = CliRunner()
    cli_arguments = ["--config={}".format(original_behavior_config), inside_a_class.path]
    result = runner.invoke(cli.main, args=cli_arguments)

    assert result.exit_code == 0
    assert "inside_a_class.py : 1 test mark added" in result.output
    with open(inside_a_class.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == inside_a_class.expected


def test_backup(inside_a_class, original_behavior_config):
    """Test that a target is copied to a backup location"""

    runner = CliRunner()
    cli_arguments = ["--config={}".format(original_behavior_config), inside_a_class.path]
    result = runner.invoke(cli.main, args=cli_arguments)
    assert result.exit_code == 0
    backup_regex = re.compile('^A backup was created : (.*)$', re.MULTILINE)
    path = backup_regex.search(str(result.output)).group(1)
    with open(path, 'r') as f:
        observed_data = f.read()
    assert observed_data == inside_a_class.original


def test_stepped_class_workflow(stepped_class_workflow, stepped_class_config, mocker, uuid_patch):
    """Test out the new workflow"""
    
    # patch creation of possible marks, we are only using 3 marks so not going to create all 50
    patch = {'pytest_mark1': {}, 'pytest_mark2': {}, 'pytest_mark3': {}, 'pytest_mark4': {}}
    mocker.patch("flake8_pytest_mark.MarkChecker.pytest_marks", new=patch)

    mocker.patch('uuid.uuid1', return_value=uuid_patch)
    runner = CliRunner()
    cli_arguments = ["--config={}".format(stepped_class_config), stepped_class_workflow.path]
    result = runner.invoke(cli.main, args=cli_arguments)
    assert result.exit_code == 0
    with open(stepped_class_workflow.path, 'r') as f:
        observed_data = f.read()
    assert observed_data == stepped_class_workflow.expected
