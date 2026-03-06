import os

def resolve_json_file(base_dir: str, raw_name: str) -> str | None:
    """
    Resolve real JSON file from human-readable name.
    Handles spaces, underscores, casing safely.
    """

    candidates = [
        raw_name,
        raw_name.replace(" ", "_"),
        raw_name.replace(" ", ""),
    ]

    for name in candidates:
        filename = f"{name}.json"
        path = os.path.join(base_dir, filename)
        if os.path.isfile(path):
            return path

    return None
