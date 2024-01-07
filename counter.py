import json
from pathlib import Path
from collections import defaultdict, Counter
from zipfile import ZipFile
import tiktoken
from tabulate import tabulate
from emoji import emojize


EMOJIS = {
    "messages": emojize(":speech_balloon:"),
    "words": emojize(":input_latin_letters:"),
    "tokens": emojize(":yellow_circle:"),
    "chars": emojize(":information:"),
}


def extract_and_delete_zip(zip_data_file: Path) -> None:
    extract_folder = zip_data_file.with_suffix("")
    extract_folder.mkdir(exist_ok=True)

    with ZipFile(zip_data_file, "r") as zip_ref:
        zip_ref.extractall(extract_folder)
    zip_data_file.unlink()


def tokens_count(string: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")  # For GPT 3.5 and GPT 4
    num_tokens = len(encoding.encode(string))
    return num_tokens


def count(conversations_file: Path, result_file: Path) -> dict:
    with open(conversations_file, "r") as file:
        conversations = json.load(file)

    counter = defaultdict(Counter)

    for conversation in conversations:
        elements = conversation["mapping"]
        for element_contents in elements.values():
            message_details = element_contents["message"]
            if message_details is None:
                continue

            sender = message_details["author"]["role"]
            if sender == "user":
                sender = "User"
            elif sender == "assistant":
                sender = "ChatGPT"
            else:
                continue  # Ignore 'system' messages

            message_content = message_details["content"]["parts"][0]
            counter["messages"][sender] += 1
            counter["words"][sender] += len(message_content.split())
            counter["tokens"][sender] += tokens_count(message_content)
            counter["chars"][sender] += len(message_content)

    for field, stats in counter.items():
        counter[field]["Total"] = sum(stats.values())

    with open(result_file, "w") as file:
        json.dump(counter, file, indent=4)


def process_data(result_file: Path) -> None:
    data_folder = Path(__file__).parent / "data"
    data_folder.mkdir(exist_ok=True)

    for item in data_folder.iterdir():
        if item.suffix.lower() == ".zip":
            extract_and_delete_zip(item)

        conversations_file = item.with_suffix("") / "conversations.json"
        if conversations_file.exists():
            break
    else:
        raise FileNotFoundError(
            "Could not find your data."
            "\nPlease move your downloaded zip data file into the 'data' folder and try again."
        )

    count(conversations_file, result_file)


def print_result(result_file: Path) -> None:
    with open(result_file, "r") as file:
        counter = json.load(file)

    for field, stats in counter.items():
        print(f"\n{EMOJIS[field]} {field.capitalize()}")
        print(tabulate(stats.items(), tablefmt="fancy_grid", intfmt=","))


def main():
    result_file = Path(__file__).parent / "result.json"
    if not result_file.exists():
        print("Processing...")
        process_data(result_file)

    print_result(result_file)


if __name__ == "__main__":
    main()
