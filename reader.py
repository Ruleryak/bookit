import os
import time
import tkinter as tk
import pyphen
import tkinter.messagebox as msgbox
from tkinter import filedialog
from ebooklib import epub
from bs4 import BeautifulSoup


def load_epub_file():
    file_path = filedialog.askopenfilename(filetypes=[("EPUB files", "*.epub")])
    if file_path:
        book = epub.read_epub(file_path)
        return book
    return None

def count_syllables(word):
    dic = pyphen.Pyphen(lang='en')
    syllables = dic.inserted(word).split("-")
    return len(syllables)

def display_words(text, speed, mode="wpm"):
    root = tk.Tk()
    root.attributes("-fullscreen", True)

    label = tk.Label(root, font=("Arial", 48), wraplength=root.winfo_screenwidth())
    label.pack(expand=True)

    global words
    words = text.split()

    def update_word(word_index):
        if 0 <= word_index < len(words):
            label.config(text=words[word_index])
            word_len = len(words[word_index])
            syllable_count = count_syllables(words[word_index])
            if mode == "wpm":
                delay = 60_000 / speed
            else:  # mode == "spm"
                delay = 60_000 * syllable_count / speed
            root.after(int(delay), update_word, word_index + 1)
        else:
            root.destroy()

    root.after(0, update_word, 0)
    root.mainloop()

def display_text(book, chapter_index, speed, mode="wpm"):
    nav_item = next(item for item in book.get_items() if isinstance(item, epub.EpubNav))
    nav_soup = BeautifulSoup(nav_item.content.decode('utf-8'), 'html.parser')
    nav_element = None
    for nav in nav_soup.find_all('nav'):
        if nav.get('epub:type') == 'toc':
            nav_element = nav
            break
    nav_points = nav_element.find_all('a') if nav_element else []

    chapters = []
    for nav_point in nav_points:
        chapter_id = nav_point['href'].split('#')[0]
        chapter = book.get_item_with_href(chapter_id)
        if chapter not in chapters:
            chapters.append(chapter)

    chapter = chapters[chapter_index]
    chapter_soup = BeautifulSoup(chapter.content.decode('utf-8'), 'html.parser')
    parsed_text = ' '.join(chapter_soup.stripped_strings)

    display_words(parsed_text, speed, mode=mode)

def clean_filename(filename):
    base_name = os.path.basename(filename)
    name, _ = os.path.splitext(base_name)
    cleaned_name = name.replace('_', ' ')
    return cleaned_name + '…'

def display_chapter_menu(book):
    nav_item = next(item for item in book.get_items() if isinstance(item, epub.EpubNav))
    nav_soup = BeautifulSoup(nav_item.content.decode('utf-8'), 'html.parser')
    nav_element = None
    for nav in nav_soup.find_all('nav'):
        if nav.get('epub:type') == 'toc':
            nav_element = nav
            break
    nav_points = nav_element.find_all('a') if nav_element else []

    chapters = []
    for nav_point in nav_points:
        chapter_id = nav_point['href'].split('#')[0]
        chapter = book.get_item_with_href(chapter_id)
        if chapter not in chapters:
            chapters.append(chapter)

    def on_chapter_select(chapter_index):
        speed = wpm_scale.get() if speed_control.get() == "wpm" else spm_scale.get()
        display_text(book, chapter_index, speed, mode=speed_control.get())

    root = tk.Tk()
    root.geometry("400x400")

    wpm_scale = tk.Scale(root, from_=100, to=500, orient="horizontal", label="Words per minute")
    wpm_scale.set(250)
    wpm_scale.pack()

    spm_scale = tk.Scale(root, from_=100, to=1500, orient="horizontal", label="Syllables per minute")
    spm_scale.set(750)
    spm_scale.pack()

    speed_control = tk.StringVar()
    speed_control.set("wpm")
    wpm_radio = tk.Radiobutton(root, text="Words per minute", variable=speed_control, value="wpm")
    wpm_radio.pack(anchor="w")
    spm_radio = tk.Radiobutton(root, text="Syllables per minute", variable=speed_control, value="spm")
    spm_radio.pack(anchor="w")

    chapter_listbox = tk.Listbox(root, selectmode="browse")

    # Update this loop to use the clean_filename() helper function
    for chapter in chapters:
        cleaned_title = clean_filename(chapter.file_name)
        chapter_listbox.insert(tk.END, cleaned_title)

    chapter_listbox.pack(fill="both", expand=True)

    def on_listbox_select(event):
        index = chapter_listbox.curselection()[0]
        on_chapter_select(index)

    chapter_listbox.bind("<<ListboxSelect>>", on_listbox_select)
    root.mainloop()

def main():
    book = load_epub_file()
    if book:
        display_chapter_menu(book)
    else:
        print("No EPUB file selected.")

if __name__ == "__main__":
    main()
