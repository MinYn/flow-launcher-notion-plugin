import sys
import os

plugindir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(plugindir)
sys.path.append(os.path.join(plugindir, "lib"))
sys.path.append(os.path.join(plugindir, "plugin"))

import i18n
import logging
import locale

logging.getLogger("httpx").setLevel(logging.WARNING)

from pyflowlauncher import Plugin
from plugin.main import Query


if __name__ == "__main__":
    plugin = Plugin()
    i18n.set('filename_format', '{locale}.{format}')
    i18n.set('file_format', 'json')
    i18n.load_path.append(os.path.join(plugindir, 'plugin', 'locale'))
    i18n.set('locale', 'en_US')
    i18n.set('enable_memoization', True)
    plugin.add_method(Query(plugin))
    plugin.run()
