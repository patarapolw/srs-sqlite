import re
# from markdown import markdown
import webbrowser
from threading import Thread
from time import sleep


def get_url_images_in_text(text):
    return re.findall(r'((?:(?<=^)|(?<=\s))[^\s<>\"\']+\.(?:png|jpg|jpeg|gif))', text, flags=re.IGNORECASE)


def compare_list_match_regex(subset, superset):
    def _sub_compare():
        for super_item in superset:
            if re.search(sub_item, super_item, flags=re.IGNORECASE):
                return True

        return False

    result = []
    for sub_item in subset:
        result.append(_sub_compare())

    return all(result)


# def parse_markdown(text, image_width=500):
#     text = re.sub(r'\n+', '\n\n', text)
#     for url in get_url_images_in_text(text):
#         text = text.replace(url, '<img src="{}" width="{}"/>'.format(url, image_width))
#
#     return markdown(text)


def open_browser_tab(url):
    def _open_tab():
        sleep(1)
        webbrowser.open_new_tab(url)

    thread = Thread(target=_open_tab)
    thread.daemon = True
    thread.start()
