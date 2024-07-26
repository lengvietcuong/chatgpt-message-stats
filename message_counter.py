import json
from pathlib import Path
from collections import defaultdict, Counter
from zipfile import ZipFile
import tiktoken
from datetime import datetime


class MessageCounter:
    def __init__(self, data_folder: Path, result_file: Path):
        self.data_folder = data_folder
        self.result_file = result_file
        self.conversations_file = None

    def extract_and_delete_zip(self, zip_data_file: Path) -> None:
        # Extract contents of the zip file and then delete it
        extract_folder = zip_data_file.with_suffix("")
        extract_folder.mkdir(exist_ok=True)
        with ZipFile(zip_data_file, "r") as zip_ref:
            zip_ref.extractall(extract_folder)
        zip_data_file.unlink()

    def count_tokens(self, string: str) -> int:
        # Count the number of tokens in a string using tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")  # For GPT 3.5 and GPT 4
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def count_messages(self) -> dict:
        with open(self.conversations_file, "r") as file:
            conversations = json.load(file)

        counter = defaultdict(Counter)
        monthly_messages = defaultdict(int)

        for conversation in conversations:
            create_time = conversation.get("create_time")
            if create_time:
                date = datetime.fromtimestamp(create_time)
                month_year = f"{date.year}-{date.month:02d}"

            elements = conversation["mapping"]
            for element_contents in elements.values():
                message_details = element_contents["message"]
                if message_details is None:
                    continue

                sender = message_details["author"]["role"]
                if sender == "user":
                    sender = "User"
                    if create_time:
                        monthly_messages[month_year] += 1
                elif sender == "assistant":
                    sender = "ChatGPT"
                else:
                    continue  # Ignore 'system' messages

                message_content = message_details["content"]["parts"][0]
                counter["messages"][sender] += 1
                counter["words"][sender] += len(message_content.split())
                counter["tokens"][sender] += self.count_tokens(message_content)
                counter["chars"][sender] += len(message_content)

        # Calculate totals for each field
        for field, stats in counter.items():
            counter[field]["total"] = sum(stats.values())

        # Add monthly messages to the counter
        counter["monthly_messages"] = dict(sorted(monthly_messages.items()))

        # Save results to file
        with open(self.result_file, "w") as file:
            json.dump(counter, file, indent=4)

        return counter

    def process_data(self) -> None:
        # Process the data from the zip file
        self.data_folder.mkdir(exist_ok=True)
        for item in self.data_folder.iterdir():
            if item.suffix.lower() == ".zip":
                self.extract_and_delete_zip(item)
            self.conversations_file = item.with_suffix("") / "conversations.json"
            if self.conversations_file.exists():
                break
        else:
            raise FileNotFoundError(
                "Could not find your data."
                "\nPlease move your downloaded zip data file into the 'data' folder and try again."
            )

        self.count_messages()
