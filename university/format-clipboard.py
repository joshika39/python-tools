import time
import threading

import pyperclip

replace_dict = {
    "¨u": "ü",
    "¨U": "Ü",
    "´u": "ú",
    "´U": "Ú",
    "˝u": "ű",
    "˝U": "Ű",
    "¨o": "ö",
    "¨O": "Ö",
    "˝o": "ő",
    "˝O": "Ő",
    "´o": "ó",
    "´O": "Ó",
    "´a": "á",
    "´A": "Á",
    "´e": "é",
    "´E": "É",
    "´ı": "í",
    "´I": "Í",
    "∩": "$\\cap$ ",
    "∪": "$\\cup$ ",
    "M ": "$\\triangle$ ",
}

def format_clipboard(content, watcher=None):
    print("Clipboard changed!")
    for k, v in replace_dict.items():
        content = content.replace(k, v)
    if watcher:
        watcher.modify_last_value(content)
    pyperclip.copy(content)
    print("Clipboard formatted!")
    print(content)

class ClipboardWatcher(threading.Thread):
    def __init__(self, callback, pause=5.):
        super(ClipboardWatcher, self).__init__()
        self._callback = callback
        self._pause = pause
        self._stopping = False
        self._last_value = pyperclip.paste()

    def modify_last_value(self, value):
        self._last_value = value
            
    def run(self):       
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != self._last_value:
                recent_value = tmp_value
                self._callback(recent_value, self)
            time.sleep(self._pause)
    
    def stop(self):
        self._stopping = True

def main():
    watcher = ClipboardWatcher(format_clipboard)
    watcher.start()
    try:
        print("Waiting for changed clipboard...")
        time.sleep(10)
    except KeyboardInterrupt:
        watcher.stop()
    

if __name__ == "__main__":
    main()
