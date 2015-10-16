from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os


class PathFinder:
    """
    Used to analyse paths for a match with initialised search term.

    Attributes:
        search_term (str): string to check directory names against.
    """

    def __init__(self, search_term):
        self.search_term = search_term

    def check_path(self, path):
        """
        Retrieve the file/directory name and compare it with the search term.

        Args:
            path: path to directory/file to be checked.

        Returns:
            True if there is a direct match (ignoring case), False otherwise.
        """
        dir_name = os.path.basename(os.path.normpath(path))
        if dir_name.lower() == self.search_term.lower():
            return True
        else:
            return False
