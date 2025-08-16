"""
reverse_readline.py, Geoffrey Weal, 26/3/22

reverse_readline is a generator that returns the lines of a file in reverse order
"""
import os

def get_EKMC_version():
    """
    This method will grab the version of this EKMC program without starting up the EKMC process in full

    Returns
    -------
    The version of this EKMC program
    """

    # First, get the path to the __init__file.
    path_to_init_file = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../__init__.py'))

    # Second, read through the __init__.py file and search for the __version__ line.
    version_no = str(None)
    with open(path_to_init_file, 'r') as FILE:
        for line in FILE:
            if '__version__ =' in line:
                line = line.rstrip().split()
                version_no = line[2].replace("'",'')
                break

    # Third, return the version number
    return version_no