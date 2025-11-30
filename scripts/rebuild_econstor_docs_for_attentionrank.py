import json
from pathlib import Path

# Ahora usamos el conjunto de test como fuente (JSONL)
INPUT = Path("data/test.jsonl")
OUT_DIR = Path("econstor/docsutf8")


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"No se encuentra el archivo {INPUT}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Reconstruyendo docsutf8 desde {INPUT} ...")

    count = 0
    for idx, obj in enumerate(load_jsonl(INPUT)):
        # Ajusta 'text' si tu test usa otro campo para el texto
        text = (
            obj.get("text")
            or obj.get("text_en")
            or obj.get("document")
            or ""
        )
        outpath = OUT_DIR / f"{idx}.txt"
        outpath.write_text(text, encoding="utf-8")
        count += 1

    print(f"Generados {count} ficheros en {OUT_DIR}")


if __name__ == "__main__":
    main()