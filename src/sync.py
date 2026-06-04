import hashlib
import json
from pathlib import Path


HASH_FILE = Path("data/article_hashes.json")


def calculate_file_hash(file_path: Path) -> str:
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def load_hashes(hash_file: Path = HASH_FILE) -> dict[str, str]:
    if not hash_file.exists():
        return {}

    with hash_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_hashes(hashes: dict[str, str], hash_file: Path = HASH_FILE) -> None:
    hash_file.parent.mkdir(parents=True, exist_ok=True)

    with hash_file.open("w", encoding="utf-8") as file:
        json.dump(hashes, file, indent=2)


def detect_changed_files(markdown_files: list[Path]) -> tuple[list[Path], dict[str, int]]:
    old_hashes = load_hashes()
    new_hashes = {}

    changed_files = []
    added = 0
    updated = 0
    skipped = 0

    for file_path in markdown_files:
        file_hash = calculate_file_hash(file_path)
        key = file_path.name
        new_hashes[key] = file_hash

        if key not in old_hashes:
            changed_files.append(file_path)
            added += 1
        elif old_hashes[key] != file_hash:
            changed_files.append(file_path)
            updated += 1
        else:
            skipped += 1

    save_hashes(new_hashes)

    return changed_files, {
        "added": added,
        "updated": updated,
        "skipped": skipped,
    }