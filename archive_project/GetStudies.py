def get_studies(studies):
    '''If studies is a file then the names will be returned as a list, if not then the list is returned.'''
    if type(studies) is str:
        try:
            with open(studies) as f:
                studies_from_file = [line.rstrip('\n') for line in f]
                message="Studies extracted from file\n"
                return studies_from_file, message
        except FileNotFoundError:
            message="This file can't be found. Attempt will be made to interpret as a list. If this is not intended then please enter a valid path to a file or a list of study names.\n"
            return list(studies.split(',')), message
    elif type(studies) is list:
        message="Studies extracted from list\n"
        return studies, message
    else:
        message = (type(studies), "is not a valid input type. Nothing will be uploaded. Please enter path to a file or a list of study names\n")
        return [], message
