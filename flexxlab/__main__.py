"""
CLI for flexxlab
"""

import sys
import subprocess

from .registry import (get_plugin_names, get_class_from_name,
                       add_plugin_name, remove_plugin_name)

from .labext import write_flexx_core_js


class CLI:
    """ Command line interface class. Commands are simply defined as methods.
    """
    
    ALIASES = {}
    
    def __init__(self, args=None):
        if args is None:
            return
        
        command = args[0] if args else 'help'
        command = self.ALIASES.get(command, command)
        
        if command not in self.get_command_names():
            raise RuntimeError('Invalid command %r' % command)
        
        func = getattr(self, 'cmd_' + command)
        func(*args[1:])
    
    def get_command_names(self):
        commands = [d[4:] for d in dir(self) if d.startswith('cmd_')]
        commands.sort()
        return commands
    
    def get_global_help(self):
        lines = []
        lines.append('flexxlab command line interface')
        lines.append('  python -m flexxlab <command> [args]')
        lines.append('')
        for command in self.get_command_names():
            doc = getattr(self, 'cmd_' + command).__doc__
            if doc:
                summary = doc.strip().splitlines()[0]
                lines.append('%s %s' % (command.ljust(15), summary))
        return '\n'.join(lines)
    
    def cmd_help(self, command=None):
        """ show information on how to use this command.
        """
        
        if command:
            if command not in self.get_command_names():
                raise RuntimeError('Invalid command %r' % command)
            doc = getattr(self, 'cmd_' + command).__doc__
            if doc:
                lines = doc.strip().splitlines()
                doc = '\n'.join([lines[0]] + [line[8:] for line in lines[1:]])
                print('%s - %s' % (command, doc))
            else:
                print('%s - no docs' % command)
        else:
            print(self.get_global_help())
    
    def cmd_version(self):
        """ print the flexxlab version number.
        """
        import flexxlab
        print(flexxlab.__version__)
    
        #print(http_fetch('http://localhost:%i/flexx/cmd/log' % int(port)))
    
    def cmd_enable(self):
        """ Register flexxlab as a server and lab extension.
        """
        run_cmd('jupyter serverextension enable --py flexxlab')
        run_cmd('jupyter labextension install --py flexxlab')
        run_cmd('jupyter labextension enable --py flexxlab')
        
        try:
            write_flexx_core_js()
        except Exception as err:
            print('Could not update flexx-core.js:', err)
        
        print('Flexxlab is ready to use!')
    
    def cmd_disable(self):
        """ Unregister flexxlab as a server and lab extension.
        """
        run_cmd('jupyter serverextension disable --py flexxlab')
        run_cmd('jupyter labextension disable --py flexxlab')
        
        print('Flexxlab is disabled.')
    
    def cmd_add(self, name=''):
        """ Add a Flexx model as a Jupyterlab plugin.
        """
        msg = 'flexxlab add command need qualified path to a Flexx Model class, '
        msg += 'e.g. "foo.bar.MyModel", '
        
        if not name:
            sys.exit(msg + 'but no name was given.')
        if not '.' in name:
            sys.exit(msg + 'but there was no dot in the name.')
        
        try:
            cls = get_class_from_name(name)
        except Exception as err:
            sys.exit(str(err))
        
        # On sucess, add name. Not cls.__qualname__ because the user may
        # deliberately use another namespace.
        add_plugin_name(name)
    
    def cmd_remove(self, name=''):
        """ Remove a Flexxlab plugin.
        """
        msg = 'flexxlab remove command need qualified path to a Flexx Model class, '
        msg += 'e.g. "foo.bar.MyModel", '
        
        if not name:
            sys.exit(msg + 'but no name was given.')
        if not '.' in name:
            sys.exit(msg + 'but there was no dot in the name.')
        
        remove_plugin_name(name)
    
    def cmd_list(self):
        """ List the currently enabled Flexxlab plugins.
        """
        names = get_plugin_names()
        if not names:
            print('There are currently 0 enabled Flexxlab plugins.')
        else:
            print('There are currently %i enabled Flexxlab plugins:' % len(names))
            for name in names:
                print('    ' + name)


def run_cmd(cmd):
    """ Run a CLI command. Only for simple commands that don't require escaping.
    """
    print(cmd)
    try:
        subprocess.check_call(cmd.split(' '))
    except subprocess.CalledProcessError:
        sys.exit(1)


def main():
    # Main entry point (see setup.py)
    CLI(sys.argv[1:])


if __name__ == '__main__':
    main()
