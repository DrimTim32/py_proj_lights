"""This file contains OptimisationException class"""


class OptimisationException(Exception):
    """Clas for exceptions in this module"""

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
