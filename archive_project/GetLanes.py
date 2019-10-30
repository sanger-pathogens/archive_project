from subprocess import check_output
import os


def get_lanes(study):
    '''Use pf to find paths to data for given study. If paths returned then check that these exist.'''
    data = check_output(["pf", "data", "-t", "study", "-i", study]).decode('ascii').splitlines()
    if len(data) == 0:
        print('Unknown study or no data associated with study', study)
        return []
    else:
        existing_data = [path for path in data if os.path.exists(path) is not False]
        fake_path = [path for path in data if os.path.exists(path) is not True]
        if len(fake_path) != 0:
            print("These paths were returned by pf, but do not actually exist", fake_path)
        return existing_data
