import os
import json
from pdb import set_trace as stop

CONFIG_DIR = ".valenoq"
CONFIG_FILE_NAME = "api.config"

class ValenoqIllegalConfigParam(Exception):
    pass


class ValenoqConfigCannotBeCreated(Exception):
    pass

def set(*args, **kwargs):
    """
    Storing configuration data into a local config file (~/.valenoq/api.config)

    Parameters
    ------------
    api_key: str
        The API key (available after registration at https://valenoq.com)

    """
    api_key = kwargs.get("api_key")
    if api_key:
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, CONFIG_DIR)
        if not os.path.isdir(config_dir):
            # create dir first
            try:
                os.mkdir(config_dir)
            except PermissionError:
                raise ValenoqConfigCannotBeCreated("Permission denied to create a folder %s. Please create manually or change permissions" %config_dir)

        config_file = os.path.join(config_dir, CONFIG_FILE_NAME)
        with open(config_file, "w") as ifile:
            ifile.write(json.dumps({"api_key": api_key}))
    else:
        raise ValenoqIllegalConfigParam("The only supported configuration parameter is api_key. The value of the api_key cannot be empty")
