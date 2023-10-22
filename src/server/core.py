from dimsim import get_distance
from asrt import get_pinyin


PinyinName = list[str]


names: list[PinyinName] = []


def min_distance(p1: PinyinName, p2: PinyinName) -> float:
    if len(p1) < len(p2):
        return min_distance(p2, p1)
    return min(
        get_distance(p2, p1[i:(i + len(p2))], pinyin=True)
        for i in range(len(p1) - len(p2) + 1)
    )


def match_pinyin(names: list[PinyinName], target: PinyinName) -> list[tuple[int, float]]:
    return sorted(
        ((i, min_distance(name, target))
         for i, name in enumerate(names)),
        key=lambda x: x[1]
    )


def load():
    names.clear()
    with open("src/server/names.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            names.append(line.split(" "))


def match_from_audio(filename: str) -> list[dict[str, str | float]]:
    pinyin = get_pinyin(filename)
    if not pinyin:
        return []
    return [{
        "name": " ".join(names[idx]),
        "sim": 1.0 / (distance + 1e-5)
    } for idx, distance in match_pinyin(names, pinyin)]


load()
