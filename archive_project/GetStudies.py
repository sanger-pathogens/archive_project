def get_studies(studies):
    '''If studies is a file then the names will be returned as a list, if not then the list is returned.'''
    if type(studies) is str:
        try:
            with open(studies) as f:
                studies_from_file = [line.rstrip('\n') for line in f]
                return studies_from_file
        except FileNotFoundError:
            print("This file can't be found. Please enter a valid path to a file or a list of study names")
            return []
    elif type(studies) is list:
        return studies
    else:
        print(type(studies), "is not a valid input type. Please enter path to a file or a list of study names")
        return []
