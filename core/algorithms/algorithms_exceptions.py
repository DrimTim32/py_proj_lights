"""This file contains OptimisationException class"""


class OptimisationException(Exception):
    """Clas for exceptions in this module"""

    def __init__(self, msg):
        super(OptimisationException, self).__init__(msg)
