import json


class FileClient:
    def load(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as a:
            return json.load(a)

    def save(self, file_name, data):
        with open(file_name, 'w', encoding='utf-8') as a:
            json.dump(data, a, ensure_ascii=False)


