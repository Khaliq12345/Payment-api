import json


def get_group_amount(group_id: str) -> float | int:
    """Get the group amount from the a json file"""
    try:
        with open("./src/groups.json", "rb") as f:
            json_string = f.read()
            json_dict = json.loads(json_string)
            return json_dict[f"{group_id}"]["amount"]
    except Exception as e:
        return 100


def update_group_amount(group_id: str, amount: float):
    filepath = "./src/groups.json"

    # Read existing data
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Update the group
    data[group_id] = {"amount": amount}

    # Write back to file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return data
