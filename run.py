#!/usr/bin/env python

import sys, os

def install_config():
    #install public lib path
    lib_path = os.path.join(os.path.dirname(__file__), 'lib')
    if os.path.isdir(lib_path) and lib_path not in sys.path:
        sys.path.insert(0, lib_path)
    #install conf path
    conf_path = os.path.join(os.path.dirname(__file__), 'config')
    if os.path.isdir(conf_path) and conf_path not in sys.path:
        sys.path.insert(0, conf_path)
    #install app path
    app_path = os.path.join(os.path.dirname(__file__), 'apps')
    if os.path.isdir(app_path) and app_path  not in sys.path:
        sys.path.insert(0, app_path)
    #install controllers path
    controller_path = os.path.join(os.path.dirname(__file__), 'app/controllers')
    if os.path.isdir(app_path) and app_path  not in sys.path:
        sys.path.insert(0, app_path)
    #install models path
    model_path = os.path.join(os.path.dirname(__file__), 'app/models')
    if os.path.isdir(model_path) and model_path not in sys.path:
        sys.path.insert(0, model_path)

if __name__ == "__main__":
    install_config()
    from cat.app import run
    run(os.path.dirname(__file__))
    
