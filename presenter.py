import json
from pathlib import Path
from tabulate import tabulate
from emoji import emojize
import matplotlib.pyplot as plt


EMOJIS = {
    "messages": emojize(":speech_balloon:"),
    "words": emojize(":input_latin_letters:"),
    "tokens": emojize(":yellow_circle:"),
    "chars": emojize(":information:"),
}


class Presenter:
    def __init__(self, result_file: Path):
        self.result_file = result_file
        with open(self.result_file, "r") as file:
            self.data = json.load(file)

    def print_result(self) -> None:
        # Print the results in a tabular format
        for field, stats in self.data.items():
            if field != "monthly_messages":
                print(f"{EMOJIS[field]} {field.capitalize()}")
                print(tabulate(stats.items(), tablefmt="simple_grid", intfmt=","))
            print()

    def draw_graph(self) -> None:
        # Draw a bar graph of monthly message counts
        monthly_messages = self.data["monthly_messages"]

        months = list(monthly_messages.keys())
        message_counts = list(monthly_messages.values())

        plt.figure(figsize=(12, 6))
        plt.bar(months, message_counts)
        plt.title("Number of ChatGPT messages monthly")
        plt.xlabel("Month")
        plt.ylabel("Number of messages")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
