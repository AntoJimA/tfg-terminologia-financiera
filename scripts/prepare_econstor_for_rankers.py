import json
from pathlib import Path

# Ruta al split de test que quieres usar para evaluación
TEST_PATH = Path("data/test.jsonl")

# Nombre del dataset dentro de los repos
DATASET_NAME = "econstor"

# Rutas destino para AttentionRank y MDERank
AR_DOCS_DIR   = Path("econstor/docsutf8")
MDR_DOCS_DIR  = Path(f"mdeRank/data/{DATASET_NAME}/docsutf8")
MDR_KEYS_DIR  = Path(f"mdeRank/data/{DATASET_NAME}/keys")

for d in [AR_DOCS_DIR, MDR_DOCS_DIR, MDR_KEYS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def main():
    if not TEST_PATH.exists():
        raise FileNotFoundError(f"No se encuentra {TEST_PATH}. Asegúrate de que data/test.jsonl existe.")

    count = 0
    for ex in load_jsonl(TEST_PATH):
        # Campos esperados según lo que has trabajado en Colab
        text = ex["text"]
        keywords = ex["keywords"]  # lista de strings
        # Usar IDs sencillos secuenciales para evitar caracteres problemáticos en nombres de archivo
        doc_id = str(count + 1)

        # Ficheros de texto para AR y MDERank
        (AR_DOCS_DIR / f"{doc_id}.txt").write_text(text, encoding="utf-8")
        (MDR_DOCS_DIR / f"{doc_id}.txt").write_text(text, encoding="utf-8")

        # Fichero .key con keywords gold para MDERank (una por línea)
        with (MDR_KEYS_DIR / f"{doc_id}.key").open("w", encoding="utf-8") as f:
            for kw in keywords:
                kw = (kw or "").strip()
                if not kw:
                    continue
                f.write(kw + "\n")

        count += 1

    print(f"Generados {count} documentos en:")
    print(f"  - {AR_DOCS_DIR} (textos para AttentionRank)")
    print(f"  - {MDR_DOCS_DIR} (textos para MDERank)")
    print(f"  - {MDR_KEYS_DIR} (keywords gold para MDERank)")


if __name__ == "__main__":
    main()