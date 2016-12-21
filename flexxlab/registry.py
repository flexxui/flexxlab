"""
This module handles the registering of Flexxlab plugins.
"""

import os

from flexx.util.config import appdata_dir
from flexx import app

regfile = os.path.join(appdata_dir('flexx'), 'flexxlab_registry.txt')


def get_class_from_name(qualname):
    """ Get the Model class based on its qualified name.
    """
    assert '.' in qualname, 'qualname needs dot'
    module_name, _, class_name = qualname.rpartition('.')
    m = __import__(module_name, fromlist=['does_not_matter'])
    if not hasattr(m, class_name):
        raise ValueError('Module %s does not have a class %s.' %
                         (module_name, class_name))
    cls = getattr(m, class_name)
    if not (isinstance(cls, type) and issubclass(cls, app.Model)):
        raise TypeError('Name %s is not a Model subclass.' % qualname)
    return cls


def get_plugin_names():
    """ Get the list of names of registered plugins.
    """
    pluginlist = []
    # Read
    if os.path.isfile(regfile):
        with open(regfile, 'rb') as f:
            pluginlist = f.read().decode().splitlines()
    # Clean
    pluginlist = [line.strip() for line in pluginlist]
    pluginlist = [line for line in pluginlist if line]
    return pluginlist


def get_plugin_classes():
    """ Get the list of Model classes that represent the plugins.
    """
    classes = []
    for name in get_plugin_names():
        try:
            classes.append(get_class_from_name(name))
        except Exception as err:
            print('Could not load %s: %s' % (name, str(err)))
    return classes


def _save_plugin_names(pluginlist):
    """ Save the list of plugins.
    """
    # Ensure that the file exists
    dname = os.path.dirname(regfile)
    if not os.path.isdir(dname):
        os.mkdir(dname)
    
    # Store back
    with open(regfile, 'wb') as f:
        text = '\r\n'.join(pluginlist)  # be nice to notepad users
        f.write(text.encode())


def add_plugin_name(qualname):
    """ Add plugin based on name of the class. No checks are done.
    """
    pluginlist = get_plugin_names()
    if qualname in pluginlist:
        print('Flexxlab plugin %s is already enabled.' % qualname)
    else:
        pluginlist.append(qualname)
        print('Flexxlab plugin %s is now enabled.' % qualname)
    _save_plugin_names(pluginlist)


def remove_plugin_name(qualname):
    """ Remove the plugin with the given name.
    """
    pluginlist = get_plugin_names()
    if qualname in pluginlist:
        pluginlist.remove(qualname)
        print('Flexxlab plugin %s is now disabled.' % qualname)
    else:
        print('Flexxlab plugin %s was not enabled.' % qualname)
    _save_plugin_names(pluginlist)
