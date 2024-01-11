from notion_client import Client
import requests
import struct
import os


class Notion():
    plugin_path="plugin"
    icon_path=os.path.join(plugin_path, "icons")
    emoji_icon_path=os.path.join(plugin_path, "emojiicons")
    _default_icon_path=os.path.join(icon_path, "notion-icon.png")

    def __init__(self, token):
        self._client = Client(auth=token)

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
        icon = os.path.join(self.emoji_icon_path, f"{emojicodepoints}.png")
        return icon

    def external_icon_parse(self, data_icon):
        icon_url = data_icon['external']['url']
        filename = icon_url.split('/')[-1]
        filepath = os.path.join(self.icon_path, filename)
        self.file_save(icon_url, filepath)
        icon = filepath
        return icon

    def file_icon_parse(self, data_icon):
        icon_url = data_icon['file']['url']
        filename = icon_url.split('/')[-1].split('?')[0]
        filepath = os.path.join(self.icon_path, filename)
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
