# flexxlab

Enable writing JupyterLab plugins using Flexx.


## Installation and dependencies

At the moment, this needs bleeding edge versions of Flexx (and also Jupyterlab?).

Install from github, we're not on pypi yet.


## Quickstart

* `python -m flexxlab enable` to set things up
* `python -m flexxlab add my.module.MyModelSubclass`
* Example: `python -m flexxlab add flexxlab.examples.mondriaan.MondriaanPlugin`
* `jupyter lab` as usual


## Usage

* `flexxlab enable` to set things up. After updating Flexx, you'll want to run
  this again to install the latest `flexx-core.js` into Jupyterlab.
* `flexxlab disable` to turn it all off again.
* `flexxlab add x.y.MyModel` to turn Flexx plugins on. The class being referenced
  must be a subclass of `flexx.app.Model`. It should preferably have a
  `jlab_activate` in JS, but this not needed per see; you could even
  `flexxlab add flexx.ui.Button`.
* `flexxlab remove x.y.MyModel` to turn Flexx plugins off.

