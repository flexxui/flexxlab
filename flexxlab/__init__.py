"""
Flexxlab is a Python package and command line utility to enable writing
Jupyterlab plugins using Flexx.
"""

__version__ = '1.0.0'


from flexx import set_log_level
set_log_level('warning')

# Load hooks to make this look like a Jupyter server extension
from .serverext import _jupyter_server_extension_paths, load_jupyter_server_extension

# Load hooks to make this look like a Jupyter lab extension
from .labext import _jupyter_labextension_paths, _jupyter_labextension_config
