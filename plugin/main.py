import i18n
import dateutil.parser
import pytz

from pyflowlauncher import Plugin, Result, Method, api as API
from pyflowlauncher.result import ResultResponse

from requests.exceptions import ReadTimeout, ConnectionError, HTTPError

from .client import Notion

class Query(Method):
    def __init__(self, plugin: Plugin) -> None:
        super().__init__()
        self.plugin = plugin

    def __call__(self, query: str) -> ResultResponse:
        try:
            api_secret = self.plugin.settings.get("api_secret")
            if api_secret:
                notion = Notion(api_secret)
                if query:
                    try:
                        data = notion.search(query)
                    except (ReadTimeout, ConnectionError, HTTPError) as e:
                        self.add_result(Result(
                            Title=i18n.t("error"),
                            SubTitle=i18n.t("error-network")
                        ))
                    else:
                        for item in notion.search_response(data['results']):
                            last_edited_time = dateutil.parser.parse(item['last_edited_time']).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M")
                            self.add_result(Result(
                                Title=item['title'],
                                SubTitle=i18n.t("last-edited", datetime=last_edited_time),
                                IcoPath=item['icon'],
                                ContextData="ctxData",
                                JsonRPCAction=API.open_url("{}?deepLinkOpenNewTab=true".format(item['url']))
                            ))
                else:
                    self.add_result(Result(
                        Title=i18n.t("searching"),
                        SubTitle=i18n.t("searching-subtitle")
                    ))
            else:
                self.add_result(Result(
                    Title=i18n.t("error"),
                    SubTitle=i18n.t("error-api-secret"),
                    JsonRPCAction=API.open_setting_dialog()
                ))
        except Exception as e:
            self._logger.error(e)
        return self.return_results()
