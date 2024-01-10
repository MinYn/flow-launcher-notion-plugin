import sys
import os

plugin_root = sys.argv[0]
os.chdir(os.path.dirname(os.path.abspath(plugin_root)))

from plugin.main import NotionSearch

if __name__ == "__main__":
    notion_search = NotionSearch()
    notion_search.run()
