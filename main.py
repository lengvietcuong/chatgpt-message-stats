from pathlib import Path
from message_counter import MessageCounter
from presenter import Presenter


def main():
    data_folder = Path(__file__).parent / "data"
    result_file = Path(__file__).parent / "result.json"

    if not result_file.exists():
        print("Processing...")
        counter = MessageCounter(data_folder, result_file)
        counter.process_data()
        print("Done! Result file saved.\n")

    presenter = Presenter(result_file)
    presenter.print_result()
    presenter.draw_graph()


if __name__ == "__main__":
    main()