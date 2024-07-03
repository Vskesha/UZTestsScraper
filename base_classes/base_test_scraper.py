import json
from abc import ABC, abstractmethod
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from base_classes.test_types import Types


class TestScraper(ABC):
    def __init__(self, answers_filename: str | Path, answers_json: str | Path):
        self.answers_filename = answers_filename
        self.answers_json = answers_json
        self.answers = self.load_answers()

    @abstractmethod
    def add_answers_from_file(self, source_filename: str | Path):
        pass

    def add_question(
        self,
        question: str,
        question_type: Types,
        options: list[str],
        corrects: list[bool | str],
        solved: bool,
    ):
        """
        adds question to self.answers dictionary
        """
        if question in self.answers:
            old_options = set(op["text"] for op in self.answers[question]["options"])
            new_options = set(options)
            if old_options == new_options:
                print(f'Запитання: "{question[:50]} ..." вже зустрічалось раніше.')
                return
            question += "_"

        self.answers[question] = {
            "type": question_type,
            "solved": solved,
            "options": [
                {"text": txt, "correct": cor} for txt, cor in zip(options, corrects)
            ],
        }
        print(f'Запитання: "{question[:50]}..." було додано до бази запитань.')

    def dump_answers(self):
        with open(self.answers_json, "w", encoding="utf-8") as f:
            json.dump(self.answers, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_html_from_file(filename: str) -> str:
        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()
        return html

    def load_answers(self):
        with open(self.answers_json, "r", encoding="utf-8") as f:
            answers = json.load(f)
        return answers

    def write_answers_to_html(self):
        env = Environment(loader=FileSystemLoader("../templates"))
        template = env.get_template("answers_template.html")
        html = template.render({"answers": self.answers})
        with open(self.answers_filename, "w", encoding="utf-8") as f:
            f.write(html)
