#!/usr/bin/env python
from __future__ import print_function
from collections.abc import Iterable


class ATHVar(object):
    """An ~ATH variable is basically a node in a binary tree;
    Except that it may only have either zero or two children.
    The children can point to any object, even the parent itself

    Note that a distinction is made between which value or variable
    is pointing to the variable's left side, and which value or
    variable is pointing to the variable's right side.
    """
    __slots__ = (_alive, _left, _right, value, isLeftOf, isRightOf, __dict__)

    def __init__(self, *args, alive=True):
        self._alive = alive
        self.value = None
        argnum = len(args)
        if argnum == 0:
            self._left = None
            self._right = None
        elif argnum == 1:
            arg = args[0]
            if isinstance(arg, Iterable):
                if len(arg) == 2:
                    # If passed an iterable, 
                    self._left = ATHVar(arg[0])
                    self._right = ATHVar(arg[1])
                else:
                    raise TypeError('~ATH variables must be bifurcatable')
            elif isinstance(arg, ATHVar):
                # Shallow copy if passed another ATHVar reference.
                self._left, self._right = arg.parts
            elif isinstance(arg, str):
                slen = len(arg)
                if not slen:
                    # If passed an empty string, kill it.
                    self._alive = False
                elif slen == 1:
                    # If passed a single char, store the value.
                    self.value = arg
                else:
                    # If passed a string, its children will hold:
                    # The first character on the left,
                    self._left = ATHVar(arg[0])
                    # and a pointer to the rest on the right.
                    self._right = ATHVar(arg[1:])
            else:
                raise TypeError('~ATH variables must be bifurcatable')
        elif argnum == 2:
            self._left = args[0]
            self._right = args[1]
        else:
            raise TypeError('~ATH variables must be bifurcatable')
        # self.isLeftOf = []
        # self.isRightOf = []

    def __str__(self):
        """Allows ATHVar instances holding strings to be read."""
        if not self._alive:
            return '\n'
        return str(self._left.value) + str(self._right)

    def __bool__(self):
        """Returns living status of the object."""
        return self._alive

    @property
    def parts(self):
        """Returns a tuple of the variable's children."""
        return (self._left, self._right)

    def bifurcate(self):
        """Returns a tuple of the variable's children.
        If the children are pointing to nothing, create new ~ATH variables
        for them to point to."""
        if not self.parts is (None, None):
            self._left = ATHVar()
            # self._left.isLeftOf.append(self)
            self._right = ATHVar()
            # self._right.isRightOf.append(self)
        return self.parts

    def kill(self):
        """Kills this object, enabling loops using it to close."""
        self._alive = False


class Script(ATHVar):

    def __init__(self, script, *args):
        self.script = script
        self.seek = 0
        self.locals = {
            'NULL': ATHVar(alive=False),
            'THIS': self,
            'ARGS': args,
        }
        self.stack = []
        self._alive = True

    def parseline(self):
        pass

    def execute(self, command, *args):
        pass

    def evaluate(self):
        return_value = None
        while self._alive:
            self.kill()
        return return_value
