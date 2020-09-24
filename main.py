# encoding: UTF-8

import sys

sys.path.append("lib")  # noqa
from collections import namedtuple

import lib.requests
from lib.requests import HTTPError
from lib.workflow import Workflow3, Workflow, KeychainError, ICON_WARNING

from conf import Y_DICT_KEY, Y_TRANSLATE_TOKEN

Item = namedtuple("Item", "title,subtitle")
RU_ALPHA = u"йцукенгшщзхъфывапролджэёячсмитьбю"

Y_DICT_URL = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup"
Y_TRANSLATE_URL = "https://translate.api.cloud.yandex.net/translate/v2/translate"
Y_SPELLER_URL = "https://speller.yandex.net/services/spellservice.json/checkText"


def is_russian(s):
    # type: (unicode) -> bool
    for char in s:
        if char in RU_ALPHA:
            return True
    return False


def dictionary_lookup(word, key):
    # type: (unicode, unicode) -> List[Item]
    lang = u"ru-en" if is_russian(word) else u"en-ru"
    url = u"{}?key={}&lang={}&text={}".format(Y_DICT_URL, key, lang, word)

    resp = lib.requests.get(url)
    resp.raise_for_status()

    result = resp.json().get("def", [])
    items = []
    for definition in result:
        for tr in definition["tr"]:
            subtitle = ""
            if definition.get("ts"):
                subtitle += "[%s] " % definition["ts"]
            synonyms = [syn["text"] for syn in tr.get("syn", [])][:3]
            if synonyms:
                subtitle += " " + ", ".join(synonyms)
            means = [mean["text"] for mean in tr.get("mean", [])][:3]
            if means:
                subtitle += " | " + ", ".join(means)
            examples = [ex["text"] for ex in tr.get("ex", [])][:2]
            if examples:
                subtitle += " (" + " / ".join(examples) + ")"
            items.append(Item(title=tr["text"], subtitle=subtitle))
    return items


def check_spelling(word):
    # type: (unicode) -> List[Item]
    lang = u"ru" if is_russian(word) else u"en"
    url = u"{}?text={}&lang={}".format(Y_SPELLER_URL, word, lang)
    resp = lib.requests.get(url)
    resp.raise_for_status()

    data = resp.json()
    if data:
        return [Item(title=s, subtitle="") for s in data[0].get("s", [])]
    return []


def translate_phrase(phrase, token):
    # type: (unicode, unicode) -> List[Item]
    if is_russian(phrase):
        src, target = "ru", "en"
    else:
        src, target = "en", "ru"
    data = {"sourceLanguageCode": src, "targetLanguageCode": target, "texts": [phrase]}

    resp = lib.requests.post(
        Y_TRANSLATE_URL,
        json=data,
        headers={"Authorization": "Api-Key {}".format(token)},
    )
    resp.raise_for_status()

    result = resp.json()
    return [Item(title=tr["text"], subtitle="") for tr in result["translations"]]


def err(wf, title, subtitle=""):
    # type: (Workflow, unicode, unicode) -> int
    wf.add_item(title=title, subtitle=subtitle, icon=ICON_WARNING)
    wf.send_feedback()
    return 0


def main(wf):
    # type: (Workflow) -> int

    query = wf.args[0].strip().rstrip()  # type: unicode
    dictionary_mode = " " not in query
    if dictionary_mode:
        try:
            trs = dictionary_lookup(query, wf.get_password(Y_DICT_KEY))
        except KeychainError:
            return err(
                wf,
                "No API Key found",
                "Please set Dictionary API key with qset command",
            )
        except HTTPError:
            return err(
                wf,
                "Yandex Translate error",
                "Make sure you set Dictionary API key properly",
            )
    else:
        try:
            wf.clear_data()
            trs = translate_phrase(query, wf.get_password(Y_TRANSLATE_TOKEN))
        except KeychainError:
            return err(
                wf,
                "No API token found",
                "Please set Translate API token with qset command",
            )
        except HTTPError:
            return err(
                wf,
                "Yandex Translate error",
                "Make sure you set Translate API token properly",
            )

    for tr in trs:
        wf.add_item(title=tr.title, subtitle=tr.subtitle)

    if not trs and dictionary_mode:
        suggestions = check_spelling(query)
        for s in suggestions:
            wf.add_item(title=s.title, arg=s.title, valid=True)
        if not suggestions:
            wf.add_item("Nothing found..")
    elif not trs:
        wf.add_item("Nothing found..")

    wf.send_feedback()


if __name__ == "__main__":
    workflow = Workflow3()
    sys.exit(workflow.run(main))
