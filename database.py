from main import app
import sqlite3


def save_paste(text, is_private):
    notes = []
    private_notes = []
    if is_private: 
        private_notes.append(text)