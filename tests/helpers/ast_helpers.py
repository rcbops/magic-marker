#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================================================================================================
# Imports
# ======================================================================================================================
import ast


class BaseDecoratorRetriever(ast.NodeVisitor):

    def _generate_pytest_decorators(self, decorators):
        """Rebuilds pytest decorators based on available info inside the AST nodes

        Args:
            decorators (list): list of AST decorator nodes

        Returns:
            list: A list of string representations of pytest decorators
        """
        generated_decorators = []
        for decorator in decorators:
            mark_name = decorator.func.attr
            args = []
            for arg in decorator.args:
                args.append("'{}'".format(arg.s))
            d = "@pytest.mark.{}({})".format(mark_name, ', '.join(args))
            generated_decorators.append(d)
        return generated_decorators

    def _reduce_decorators_to_pytest(self, decorators):
        """reduces a list of decorators to a list that
        are decorators used by pytest

        Args:
            decorators (list): A list of decorators from AST

        Returns:
            list: decorators that are 'pytest'
        """
        reduced = []
        for decorator in decorators:
            try:
                if decorator.func.value.value.id == 'pytest':
                    reduced.append(decorator)
            except AttributeError:
                pass
        return reduced


class ClassDecoratorRetriever(BaseDecoratorRetriever):
    """A class to help pull out decorators from an AST node ClassDef"""

    def __init__(self):
        """Creates a new ClassDecoratorRetriever object"""
        self.classes = {}

    def visit_Module(self, node):
        """An overload of an ast.NodeVisitor method
        Will visit all Module nodes when .visit is called

        Args:
            node (ast.AST)

        Returns:
            dict: a dict of class names (key) & list of decorators (value)
        """
        self.generic_visit(node)
        return self.classes

    def visit_ClassDef(self, node):
        """An overload of an ast.NodeVisitor method
        Will visit all ClassDef nodes when .visit is called

        Args:
            node (ast.AST)
        """
        self.classes[node.name] = self._generate_pytest_decorators(node.decorator_list)
        self.generic_visit(node)


class FunctionDecoratorRetriever(BaseDecoratorRetriever):
    """A class to help pull out decorators from an AST node FunctionDef"""

    def __init__(self):
        """Creates a new ClassDecoratorRetriever object"""
        self.functions = {}

    def visit_Module(self, node):
        """An overload of an ast.NodeVisitor method
        Will visit all Module nodes when .visit is called

        Args:
            node (ast.AST)

        Returns:
            dict: a dict of function names (key) & list of decorators (value)
        """
        self.generic_visit(node)
        return self.functions

    def visit_FunctionDef(self, node):
        """An overload of an ast.NodeVisitor method
        Will visit all FunctionDef nodes when .visit is called

        Args:
            node (ast.AST)
        """
        self.functions[node.name] = self._generate_pytest_decorators(node.decorator_list)
        self.generic_visit(node)
