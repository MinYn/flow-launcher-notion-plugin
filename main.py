import logging

logging.basicConfig(
    format='[%(levelname)s|%(name)s.%(filename)s:%(lineno)s] %(asctime)s > %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %I:%M:%S %p',
    filename='flow-launcher-notion.log',
)

logger = logging.getLogger(__file__)

try:
    from pyflowlauncher import JsonRPCAction, Plugin, Result, Method
    from pyflowlauncher.result import ResultResponse
    from notion.client import Notion
    import webbrowser

    class Query(Method):

        def __call__(self, query: str) -> ResultResponse:
            notion = Notion()
            data = notion.search(query)
            for item in notion.search_response(data['results']):
                self.add_result(Result(
                    Title=item['title'],
                    SubTitle="마지막 수정 일자: {}".format (item['last_edited_time']),
                    ContextData="ctxData",
                    IcoPath=item['icon'],
                    JsonRPCAction=JsonRPCAction(
                        method="take_action",
                        parameters=["{}?deepLinkOpenNewTab=true".format(item['url'])],
                        # dontHideAfterAction=True
                    )
                ))
            return self.return_results()

    def take_action(arg):
        webbrowser.open(arg)


    if __name__ == "__main__":
        plugin = Plugin()
        plugin.add_method(Query())
        plugin.add_method(take_action)
        plugin.run()

except Exception as e:
    logger.error(e)
