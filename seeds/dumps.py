import os

from seeds.schema.result import SeedsResult


def save_seeds_result(result: SeedsResult, scenario: str):
    if not os.path.exists("dumps"):
        os.mkdir("dumps")

    seeds_file = f"./dumps/{scenario}_seeds.json"
    with open(seeds_file, 'w+', encoding="utf-8") as file:
        file.write(result.model_dump_json())
