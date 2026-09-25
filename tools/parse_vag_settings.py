import re
import json

def parse_vag():
    with open("libCarista.so.c", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    settings = set()
    occurrences = []
    for idx in range(519330, 538700):
        matches = re.findall(r'"(car_setting_[a-zA-Z0-9_]+)"', lines[idx])
        for m in matches:
            settings.add(m)
            occurrences.append((idx + 1, m, lines[idx].strip()))

    print(f"Total occurrences: {len(occurrences)}")
    print(f"Distinct setting keys in VAG settings function: {len(settings)}")

if __name__ == "__main__":
    parse_vag()
