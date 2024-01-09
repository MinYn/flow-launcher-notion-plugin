from flox import Flox

from notion.client import Notion
from requests.exceptions import ReadTimeout, ConnectionError, HTTPError

class NotionSearch(Flox):
    def query(self, query):
        api_secret = self.settings.get("api_secret")
        if api_secret:
            self.notion = Notion(api_secret)
        else:
            self.add_item(
                title=f"Could not connect to Notion!",
                subtitle="Please check your settings Api Secret.",
                method=self.open_setting_dialog
            )
        if query:
            try:
                data = self.notion.search(query)
            except (ReadTimeout, ConnectionError, HTTPError):
                self.add_item(
                    title=f"Could not connect to Notion!",
                    subtitle="Please check your network and try again.",
                )
                return
            else:
                for item in self.notion.search_response(data['results']):
                    self.add_item(
                        title=item['title'],
                        subtitle="{} Last Edited Time".format(item['last_edited_time']),
                        icon=item['icon'],
                        context="ctxData",
                        method=self.browser.open,
                        parameters=["{}?deepLinkOpenNewTab=true".format(item['url'])],
                    )
        else:
            self.add_item(
                title=f"Notion Search...",
                subtitle="Query Page Name",
            )

if __name__ == "__main__":
    notion_search = NotionSearch()
    notion_search.run()
