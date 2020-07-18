from subprocess import check_output
import os


def get_lanes(study):
    '''Use pf to find paths to data for given study. If paths returned then check that these exist.'''
    data = check_output(["pf", "data", "-t", "study", "-i", study]).decode('ascii').splitlines()
    if len(data) == 0:
        message = 'Unknown study or no data associated with study: {}\n'.format(study)
        return [], message
    else:
        existing_data = [path for path in data if os.path.exists(path) is not False]
        fake_paths = [path for path in data if os.path.exists(path) is not True]
        message = ''
        messages = []
        if len(fake_paths) != 0:
            for fake_path in fake_paths:
                messages.append("This path was returned by pf, but does not actually exist: {}\n".format(fake_path))
            message = ''.join(messages)
        return existing_data, message
