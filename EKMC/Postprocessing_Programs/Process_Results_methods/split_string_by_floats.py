'''
split_string_by_floats.py, Geoffrey Weal, 25/5/23

This program will convert a string into a list of characters and floats
'''
from copy import deepcopy

def split_string_by_floats(dirname):
    """
    This program will convert a string into a list of characters and floats

    Parameters
    ----------
    dirname : str
        This is the string to focus on

    Results
    -------
    dir_split_2 : list
        list of characters and float in the order as given in dirname
    """
    dir_split = []
    new_append = True
    for character in dirname:
        if ((character == '.') or character.isdigit()):
            if new_append:
                dir_split.append(character)
                new_append = False
            else:
                dir_split[-1] = dir_split[-1]+character
        else:
            dir_split.append(character)
            new_append = True

    dir_split_2 = []
    for tostring in dir_split:
        new_tostring = ['']
        even_point = False
        for character in tostring:
            if character == '.':
                if even_point:
                    new_tostring.append('')
                    even_point = False
                else:
                    even_point = True
            new_tostring[-1] = new_tostring[-1]+character
        dir_split_2 += deepcopy(new_tostring)

    for index in range(len(dir_split_2)):
        value = dir_split_2[index]
        try:
            value = float(value)
        except Exception as expection:
            pass
        dir_split_2[index] = value

    for index in range(len(dir_split_2)):
        value = dir_split_2[index]
        if isinstance(value,str):
            if len(value) > 1:
                raise Exception('Error here')
            value = ord(value)
        dir_split_2[index] = value

    return dir_split_2



