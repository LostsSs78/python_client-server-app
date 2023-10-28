from tkinter import *
from tkinter.scrolledtext import ScrolledText
from datetime import *


def text_update(username: str, text_widget: ScrolledText, entry):
    current_time = datetime.now().time()
    hours, minutes, seconds = current_time.hour, current_time.minute, current_time.second

    try:
        if type(entry) == type(''):
            text = entry
        else:
            text = entry.get()
            entry.delete(0, END)
    except Exception as _ex:
        return print('INFO ERROR IN \'text_update\' FUNCTION ' + str(_ex))

    message = f'::{hours}:{minutes}:{seconds}::{username}>>>' + text

    text_widget.configure(state='normal')
    text_widget.insert(END, '\n' + message)
    text_widget.configure(state='disabled')


