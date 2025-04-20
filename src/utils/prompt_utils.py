import csv


def apply_prompt_template(prompt: str, template: str) -> str:
    """
    Apply a prompt template to the given prompt.
    :param prompt: The original prompt.
    :param template: The template to apply.
    :return: The formatted prompt.
    """
    return template.format(prompt)


def load_prompt(prompt_path: str) -> str:
    """
    Load a prompt from a file.
    :param prompt_path: The path to the prompt file.
    :return: The loaded prompt.
    """
    with open(prompt_path, "r") as f:
        prompt = f.read()
    return prompt


def get_input_prompts(file_path: str = "prompts/input_prompts.csv") -> list:
    """
    Reads prompts from a CSV file and returns them as a list.
    :param file_path: Path to the CSV file.
    :return: List of prompts.
    """
    prompts = []
    with open(file_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        if "prompt" not in csv_reader.fieldnames:
            raise ValueError("CSV file does not contain a 'prompt' column")
        for row in csv_reader:
            prompts.append(row["prompt"])
    return prompts
