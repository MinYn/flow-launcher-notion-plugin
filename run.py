import sys
import os
import i18n
import logging

logging.getLogger("httpx").setLevel(logging.WARNING)

plugindir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(plugindir)
sys.path.append(os.path.join(plugindir, "lib"))
sys.path.append(os.path.join(plugindir, "plugin"))

from pyflowlauncher import JsonRPCAction, Plugin, jsonrpc
from pyflowlauncher.api import _send_action
from plugin.main import Query


if __name__ == "__main__":
    plugin = Plugin()
    i18n.set('filename_format', '{locale}.{format}')
    i18n.set('file_format', 'json')
    i18n.load_path.append(os.path.join(plugindir, 'plugin', 'locale'))
    i18n.set('locale', 'en')
    i18n.set('enable_memoization', True)
    plugin.add_method(Query(plugin))
    plugin.run()
