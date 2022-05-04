import sys
import importlib
import os
from . import logger


def load_module(module, path):
    if module=='user':
        try:
            file="login.py"
            filename = file.replace('.py', '')
            name = "jbot.{}.{}".format(module, filename)
            spec = importlib.util.spec_from_file_location(name, path+file)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules[f"jbot.{module}.{filename}"] = load
            logger.info(f"Bot加载-->{filename}-->完成")
        except Exception as e:
            logger.info(f"Bot加载失败-->{file}-->{str(e)}")            
            
    files = os.listdir(path)
    for file in files:
        if module=='user' and file=="login.py":
            continue
            
        try:            
            if file.endswith('.py'):
                filename = file.replace('.py', '')
                name = "jbot.{}.{}".format(module, filename)
                spec = importlib.util.spec_from_file_location(name, path+file)
                load = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load)
                sys.modules[f"jbot.{module}.{filename}"] = load
                logger.info(f"Bot加载-->{filename}-->完成")
        except Exception as e:
            logger.info(f"Bot加载失败-->{file}-->{str(e)}")
            continue

