from notion_client import Client
import requests
import struct
import os
from dotenv import dotenv_values

config = dotenv_values(".env")

class Notion():
    _default_icon_path="icons\\notion-icon.png"
    _client = Client(auth=config.get("API_KEY"))

    def _decodeemoji(self, emoji):
        if emoji:
            b = emoji.encode('utf_32_le')
            count = len(b) // 4
            # If count is over 10, we don't have an emoji
            if count > 10:
                return None
            cp = struct.unpack('<%dI' % count, b)
            hexlist = []
            for x in cp:
                hexlist.append(hex(x)[2:])
            return hexlist
        return None

    def search(self, query, page_size=5):
        response = self._client.search(query=query, page_size=page_size)
        return response
    
    def file_save(self, url, file_path):
        if not os.path.isfile(file_path):
            r = requests.get(url, allow_redirects=True)
            open(file_path, 'wb').write(r.content)

    def emoji_icon_parse(self, data_icon):
        hexlist = self._decodeemoji(data_icon['emoji'])
        emojicodepoints = ""
        count = 0
        for x in hexlist:
            count += 1
            if count > 1:
                emojicodepoints += "_"
            emojicodepoints += x
        icon = f"emojiicons\\{emojicodepoints}.png"
        return icon

    def external_icon_parse(self, data_icon):
        icon_url = data_icon['external']['url']
        filename = icon_url.split('/')[-1]
        filepath = f"icons\\{filename}"
        self.file_save(icon_url, filepath)
        icon = filepath
        return icon

    def file_icon_parse(self, data_icon):
        icon_url = data_icon['file']['url']
        filename = icon_url.split('/')[-1].split('?')[0]
        filepath = f"icons\\{filename}"
        self.file_save(icon_url, filepath)
        icon = filepath
        return icon

    def icon_parse(self, data_icon):
        icon = self._default_icon_path
        if data_icon:
            data_icon_type = data_icon['type']
            if data_icon_type == "emoji":
                icon = self.emoji_icon_parse(data_icon)
            elif data_icon_type == "external":
                icon = self.external_icon_parse(data_icon)
            elif data_icon_type == "file":
                icon = self.file_icon_parse(data_icon)
        return icon
    
    def title_parse(self, data_properties):
        title = None
        for _, value in data_properties.items():
            if value['type'] == 'title':
                title = value['title'][0]['plain_text']
                break
        return title

    def search_response(self, results):
        result = []
        for data in results:
            icon = self.icon_parse(data['icon'])
            title = self.title_parse(data['properties'])
            last_edited_time = data['last_edited_time']
            url = data['url']
            result.append({
                "icon": icon,
                "title": title,
                "url": url,
                "last_edited_time": last_edited_time,
            })
        return result

if __name__ == "__main__":
    notion = Notion()
    data = notion.search("면접")
    for item in notion.search_response(data['results']):
        print(item)
