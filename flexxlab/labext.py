"""
This module represents the labextension for flexxlab, which is used
to create a new session for each page load, and to provide the page
with the session id.

Would be nice if somewhere in this extension we could get ahold of the
tornado application object, so that we can register Flexx' handlers. Then
we would not need the server extension anymore.
"""

import os
import errno

from flexx import app

from .app import JupyterLabPluginApp


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
flexx_app_name = 'jlab'


MANIFEST = """{
"name": "flexxlab",
"entry": "flexx@1.0.0/dummy.js",
"files": ["flexx-core.js"],
"modules": {
    "flexx@1.0.0/dummy.js": []
}
}"""


ENTRY = """
/** START DEFINE BLOCK for flexx@1.0.0/dummy.js **/
jupyter.define('flexx@1.0.0/dummy.js', function (module) {
    module.exports = {
       id: 'flexx-entry',
       activate: function () { }
    };
});
/** END DEFINE BLOCK for flexx@1.0.0/dummy.js **/
"""

# todo: we may not be able to write here ... so package, meh

def _jupyter_labextension_paths():
    # This is called once, when the server starts.
    # It must return a dict that describes the lab extension.
    
    print('inside Flexx _jupyter_labextension_paths')
    
    # Write flexx bootstap js
    code = ENTRY + app.assets.get_asset('flexx-core.js').to_string()
    path = os.path.join(THIS_DIR, 'static')
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    with open(os.path.join(path, 'flexx-core.js'), 'wb') as f:
        f.write(code.encode('utf-8'))
    with open(os.path.join(path, 'flexxlab.manifest'), 'wb') as f:
        f.write(MANIFEST.encode('utf-8'))
    
    return [{
        'name': 'flexxlab',
        'src': 'static',
    }]


def _jupyter_labextension_config():
    # This (optional function) is called at each launch of the `/lab` page.
    # It must return a dict with config options to supply to the client.
    # We use it to instantiate a session too.
    
    print('inside Flexx _jupyter_labextension_config - getting session')
    
    # The application arg is a NotebookWebApplication, which ultimately derives
    # from the Tornado application class.
    session = get_session()
    
    return {'flexx_app_name': flexx_app_name, 'flexx_session_id': session.id}


def get_session():
    """ Get session instance for the flexx jlab app.
    """
    
    # The server extension should have create the jlab app, for which
    # we create sessions here
    
    if flexx_app_name not in app.manager.get_app_names():
        # This should be run just once
        
        # Create Flexx tornado server object, but don't let it host; we only
        # realy need it for its call_later() method.
        app.create_server(host=False)
        # Specify the JLab app
        app.App(JupyterLabPluginApp).serve(flexx_app_name)
    
    # Create session, tell it to ignore phosphor-all lib, because Flexx
    # is able to use JLab's Phosphor.
    session = app.manager.create_session(flexx_app_name)
    session.assets_to_ignore.add('phosphor-all.js')
    session.assets_to_ignore.add('phosphor-all.css')
    return session
