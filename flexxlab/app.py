from flexx import app, event

from .registry import get_plugin_classes


class JupyterLabPluginApp(app.Model):
    """ This model represents the Flexx application that is embedded
    in JupyterLab. It is a thin wrapper that takes care of instantiating
    and registering the Flexx plugins.
    """
    
    def init(self):
        self._plugins = []  # model instances
        #@self.init2()
        app.call_later(0.1, self.init2)
    
    def init2(self):
        # Instantiate plugins
        plugins = []
        with self:
            for cls in get_plugin_classes():
                plugins.append(cls())
        # Set plugins property, so that we have access to it on the JS side
        for p in plugins:
            self.launch_plugin(p)
        
        # Keep plugins alive
        self._plugins = plugins
    
    @event.emitter
    def launch_plugin(self, p):
        """ Event emitted by the Python side to launch a new plugin.
        """
        return {'model': p}
    
    class JS:
        
        @event.connect('launch_plugin')
        def on_launch_plugin(self, *events):
            for ev in events:
                model = ev.model
                
                print('registering Flexx JLAB plugin ', model.id)
                
                func = model.jlab_activate
                autoStart = getattr(model, 'JLAB_AUTOSTART', True)
                requires = getattr(model, 'JLAB_REQUIRES', [])
                requires = [get_token(id) for id in requires]
                
                p = dict(id='flexx.' + model._class_name.lower(),
                         activate=func, autoStart=autoStart, requires=requires)
                window.jupyter.lab.registerPlugin(p)
                if p.autoStart:
                    # Autostart means activate when JLab starts, but JLab
                    # is already running so we need to start it ourselves.
                    window.jupyter.lab.activatePlugin(p.id)


def get_token(id):
    # Collect tokens of known services. Problems:
    # - We use a private attribute here
    # - Flexx does not support generators (yet), maybe its time?
    # This could be solved if we could access these tokens in 
    # another way.
    # todo: get rid of this by making plugins use `pyscript.RawJS` to import tokens
    tokens = []
    iter = window.jupyter.lab._serviceMap.keys()  
    while True:
        item = iter.next()
        tokens.append(item.value)
        if item.done:
            break
    # Check what token corresponds with the given service id
    for token in tokens:
        if token.name == id:
            return token
    else:
        raise RuntimeError('No service known by id "%s".' % id)
