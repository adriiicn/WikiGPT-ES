import argparse
import tkinter as tk
from tkinter import ttk

from wikigpt_es.chatbot import TriadaVGChatbot
from wikigpt_es.config import IndexPaths
from wikigpt_es.indexer import WikiIndex


class WikiGPTGui(tk.Tk):
    def __init__(self, bot: TriadaVGChatbot) -> None:
        super().__init__()
        self.bot = bot
        self.title("WikiGPT-ES - Videojuegos")
        self.geometry("820x620")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ttk.Label(self, text="WikiGPT-ES (Arquitectura TRIADA-VG)", font=("Helvetica", 16, "bold"))
        header.grid(row=0, column=0, padx=16, pady=12, sticky="w")

        self.chat_area = tk.Text(self, wrap="word", state="disabled")
        self.chat_area.grid(row=1, column=0, padx=16, pady=12, sticky="nsew")

        input_frame = ttk.Frame(self)
        input_frame.grid(row=2, column=0, padx=16, pady=12, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        self.question_entry = ttk.Entry(input_frame)
        self.question_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.question_entry.bind("<Return>", self._handle_question)

        ask_button = ttk.Button(input_frame, text="Preguntar", command=self._handle_question)
        ask_button.grid(row=0, column=1)

        self._append_message("Sistema", "Escribe una pregunta sobre videojuegos en Wikipedia (ES).")

    def _append_message(self, sender: str, message: str) -> None:
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", f"{sender}: {message}\n\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    def _handle_question(self, event=None) -> None:
        question = self.question_entry.get().strip()
        if not question:
            return
        self.question_entry.delete(0, "end")
        self._append_message("Tú", question)

        response = self.bot.answer(question)
        self._append_message("WikiGPT-ES", response.answer)
        if response.sources:
            sources_text = "\n".join(f"- {source}" for source in response.sources)
            self._append_message("Fuentes", sources_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="GUI de WikiGPT-ES.")
    parser.add_argument("--data", default="data", help="Directorio con el índice entrenado.")
    args = parser.parse_args()

    index = WikiIndex.load(IndexPaths(args.data))
    bot = TriadaVGChatbot(index)
    app = WikiGPTGui(bot)
    app.mainloop()


if __name__ == "__main__":
    main()
