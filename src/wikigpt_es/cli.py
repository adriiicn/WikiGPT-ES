import argparse

from wikigpt_es.chatbot import TriadaVGChatbot
from wikigpt_es.config import IndexPaths
from wikigpt_es.indexer import WikiIndex


def main() -> None:
    parser = argparse.ArgumentParser(description="Chatbot WikiGPT-ES (videojuegos) por consola.")
    parser.add_argument("--data", default="data", help="Directorio con el índice entrenado.")
    args = parser.parse_args()

    index = WikiIndex.load(IndexPaths(args.data))
    bot = TriadaVGChatbot(index)

    print("WikiGPT-ES listo. Escribe 'salir' para terminar.")
    while True:
        question = input("Tú: ").strip()
        if question.lower() in {"salir", "exit", "quit"}:
            break
        response = bot.answer(question)
        print(f"\n{response.answer}\n")
        if response.sources:
            print("Fuentes:")
            for source in response.sources:
                print(f"- {source}")
            print("")


if __name__ == "__main__":
    main()
