import csv
import sys
import logging

from datetime import datetime
from typing import List, Tuple
from os import listdir, path
from os.path import join


logging.basicConfig(format=f"[%(levelname)s]: %(message)s", level=logging.INFO, stream=sys.stdout)

DISCORD_STOP_WORDS_FILE = "./stopwords/discord_stopwords.txt"

WA_STOP_WORDS = [word.replace('\n', '') for word in open(DISCORD_STOP_WORDS_FILE).readlines()]


def get_dir_files(dir_path: str, extension_filter: str = None) -> Tuple[List[str], List[str]]:
    files_name = listdir(path=dir_path)
    if extension_filter:
        files_name = [file for file in files_name if file.endswith(extension_filter)]
    txt_files_paths = [path.join(dir_path, file) for file in files_name]
    return files_name, txt_files_paths


def stop_word_checker(content) -> bool:
    for stop_word in WA_STOP_WORDS:
        if stop_word in content:
            return True
    return False


def save_text(text_list: List[str], output_path: str) -> None:
    logging.info(f'Saving {output_path}')
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(text_list))


def save_tokens(token_list: List[str], output_path: str) -> None:
    logging.info(f'Saving {output_path}')

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(token_list))


def parse_chat(file_path: str) -> Tuple[List[str], List[str]]:
    chat_text = []
    invalid_lines = []
    unique_tokens = []

    with open(file_path, encoding="utf-8") as csvfile:
        lines = csv.DictReader(csvfile, delimiter=",", quotechar='"')

        for line in lines:
            author, content = line['Author'], line['Content']

            if author == 'Deleted User#0000':
                invalid_lines.append(f"{author} - {content}")
                continue
            if author not in unique_tokens:
                unique_tokens.append(author)
            if stop_word_checker(content):
                invalid_lines.append(f"[STOP_WORD] {author} - {content}")
                continue

            chat_text.append(f"{author} {content}")
    logging.info(f'Found {len(invalid_lines)} invalid lines in {file_path}')
    logging.info(f'Post-parse total messages {len(chat_text)} in {file_path}')
    logging.info(f'Post-parse unique tokens {len(unique_tokens)} in {file_path}')

    open(f"../data/invalid_lines/invalid_lines_{datetime.today().strftime('%Y-%m-%d')}", 'w', encoding="utf-8")\
        .writelines("\n".join(invalid_lines))

    return chat_text, unique_tokens


def main():
    output_path = "../data/chat_parsed/"
    chat_path = join(output_path, 'wa-chats.txt')
    tokens_path = join(output_path, 'special-tokens.txt')

    chats_path = "../data/chat_raw"
    txt_files_name, txt_files_paths = get_dir_files(dir_path=chats_path, extension_filter=".csv")

    wa_text = []
    for file_name, file_path in zip(txt_files_name, txt_files_paths):
        file_text_parsed, special_tokens = parse_chat(file_path)
        wa_text.extend(file_text_parsed)
    save_tokens(special_tokens, tokens_path)
    save_text(wa_text, chat_path)


if __name__ == '__main__':
    main()
