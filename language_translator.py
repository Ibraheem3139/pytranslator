import tkinter as tk
from tkinter import ttk
from translate import Translator

class LanguageTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translator")
        self.root.configure(bg="#F0F0F0")  # Light grey background

        self.label = ttk.Label(root, text="Enter text to translate:", font=("Helvetica", 14))
        self.label.pack(pady=(15, 5))

        self.text_input = self.create_scrolled_text()
        self.text_input.pack(pady=5)

        self.language_label = ttk.Label(root, text="Select target language:", font=("Helvetica", 14))
        self.language_label.pack(pady=(10, 5))

        self.languages = {
            'Urdu': 'ur',
            'Sindhi': 'sd',
            'Tamil': 'ta',
            'Telugu': 'te',
            'Kannada': 'kn',
            'Punjabi': 'pa',
            'Balochi': 'bal'
        }
        self.language_combobox = ttk.Combobox(root, values=list(self.languages.keys()), font=("Helvetica", 12))
        self.language_combobox.pack()

        self.translate_button = ttk.Button(root, text="Translate", command=self.translate_text)
        self.translate_button.pack(pady=10)

        self.translated_text = self.create_scrolled_text(state='disabled')
        self.translated_text.pack()

        self.root.bind("<Control-MouseWheel>", self.zoom_text)  # Bind zoom event

    def create_scrolled_text(self, **kwargs):
        text_widget = tk.Text(self.root, height=10, width=40, wrap=tk.WORD, **kwargs)
        text_widget.configure(font=("Helvetica", 12), bg="white")
        return text_widget

    def translate_text(self):
        text_to_translate = self.text_input.get("1.0", "end-1c")
        selected_language = self.language_combobox.get()
        target_language = self.languages[selected_language]

        chunk_size = 500
        chunks = [text_to_translate[i:i+chunk_size] for i in range(0, len(text_to_translate), chunk_size)]

        translator = Translator(to_lang=target_language)
        translated_chunks = []

        for chunk in chunks:
            translation = translator.translate(chunk)
            translated_chunks.append(translation)

        translated_text = "".join(translated_chunks)
        self.translated_text.config(state='normal')
        self.translated_text.delete("1.0", "end")
        self.translated_text.insert("1.0", translated_text)
        self.translated_text.config(state='disabled')

    def zoom_text(self, event):
        if event.state == 12:
            if event.delta > 0:
                self.change_font_size(1)
            elif event.delta < 0:
                self.change_font_size(-1)

    def change_font_size(self, direction):
        current_font = self.text_input['font']
        size = current_font.split()[1]
        new_size = max(int(size) + direction, 6)
        new_font = f"Helvetica {new_size}"
        self.text_input.configure(font=new_font)
        self.translated_text.configure(font=new_font)

if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageTranslatorApp(root)
    root.mainloop()
