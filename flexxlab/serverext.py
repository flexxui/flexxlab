"""
This module represents the Jupyter server extension for flexxlab. It
is responsible for adding the Flexx handlers to the Tornado application
that underlies the Jupyter server.
"""

from flexx import app


def _jupyter_server_extension_paths():
    return [{
        "module": "flexxlab"
    }]


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    if 'jupyterlab' in nb_server_app.description.lower():
        print('Loading the Flexx Jupyter server extension!')
    else:
        print('Only using Flexx in JupyterLab!')
        return
    
    tornado_app = nb_server_app.web_app
    
    # Add Flexx' handlers needed to server asset and websocket
    # todo: flexx should have a function for this
    tornado_app.add_handlers(r".*", [(r"/flexx/ws/(.*)", app._tornadoserver.WSHandler),
                                     (r"/flexx/(.*)", app._tornadoserver.MainHandler),
                                     ])
