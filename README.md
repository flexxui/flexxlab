# flexxlab

Enable writing JupyterLab plugins using Flexx.


## Installation and dependencies

At the moment, this needs bleeding edge versions of Flexx (and also Jupyterlab?).

* Download or clone the source from Github.
* `pip install -e .`


## Quickstart

* `flexxlab enable` to set things up.
* `flexxlab add flexx.ui.examples.mondriaan.Mondriaan` is one example.
* `flexxlab add my.module.MyModelSubclass` to use your own Flexx widget.
* `jupyter lab` as usual.


## Usage

* Use `flexxlab enable` to set things up. After updating Flexx, you'll
  want to run this again to install the latest `flexx-core.js` into Jupyterlab.
* Use `flexxlab disable` to turn it all off again.
* Use `flexxlab add x.y.MyModel` to register a Flexx Model/Widget as a plugin.
* Use `flexxlab remove x.y.MyModel` to turn Flexx plugins off.


## Writing plugins

Plugins are simply a subclass of `flexx.app.Model` or `flexx.ui.Widget`.
It should preferably have a `jlab_activate` in JS, and can also implement
`JLAB_AUTOSTART` and `JLAB_REQUIRES`. For example:

```py
class MyPlugin(ui.Widget):
    
    def init(self):
        
        # Popluate the widget as usual
        with ui.HBox():
            self.labale1 = ui.Label(text='bla bla')
            self.button1 = ui.Label(text='Press me')
            ui.Widget(flex=1)  # spacer
    
    class JS:
        
        JLAB_AUTOSTART = True
        JLAB_REQUIRES = ['jupyter.services.file-browser',
                         'jupyter.services.document-registry']
        
        def jlab_activate(self, lab, fb, dr):
            self.title = 'Flexx foo demo'
            
            # Use fb (file browser) and dr (document registry) ...

```

See the https://github.com/zoofIO/flexxlab/tree/master/flexxlab/examples
for more examples. See the Flexx documentations to learn more about creating
widgets with Flexx.
