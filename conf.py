# encoding: UTF-8

import sys

sys.path.append("lib")  # noqa
from lib.workflow.notify import notify
from lib.workflow import Workflow3, Workflow


Y_DICT_KEY = "YTDictKey"
Y_TRANSLATE_TOKEN = "YTToken"


def main(wf):
    # type: (Workflow) -> None
    arg = wf.args[0]  # type: unicode
    if arg.startswith(Y_DICT_KEY):
        wf.save_password(Y_DICT_KEY, arg.replace(Y_DICT_KEY, ""))
        notify("Dictionary API Key has been saved!", "Source: OSX Keychain")
    elif arg.startswith(Y_TRANSLATE_TOKEN):
        notify("Translate API Token has been saved!", "Source: OSX Keychain")
        wf.save_password(Y_TRANSLATE_TOKEN, arg.replace(Y_TRANSLATE_TOKEN, ""))
    else:
        wf.add_item("Save it as Dictionary API Key", arg=Y_DICT_KEY + arg, valid=True)
        wf.add_item(
            "Set it as Translate API Token",
            arg=Y_TRANSLATE_TOKEN + arg,
            valid=True,
        )
    wf.send_feedback()


if __name__ == "__main__":
    workflow = Workflow3()
    sys.exit(workflow.run(main))
