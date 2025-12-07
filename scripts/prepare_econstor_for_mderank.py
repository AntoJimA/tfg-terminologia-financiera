#!/usr/bin/env python
import json
from pathlib import Path

# Ruta raíz del repo (ajústala si lanzas desde otro sitio)
ROOT = Path(__file__).resolve().parent.parent

# Fichero JSONL de test que ya usas con AttentionRank
TEST_JSONL = ROOT / "data" / "test.jsonl"

# Directorio destino para el dataset de MDERank
OUT_DIR = ROOT / "mdeRank" / "data" / "econstor_test"
DOCS_DIR = OUT_DIR / "docs"
GOLD_DIR = OUT_DIR / "gold"

def main():
    print(f"📄 Leyendo {TEST_JSONL}...")
    docs = []
    with TEST_JSONL.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            # Asumimos estructura: { "doc_id": ..., "text": ..., "keywords": [...] }
            doc_id = obj.get("doc_id")
            text = obj.get("text") or obj.get("text_en") or ""
            keywords = obj.get("keywords", [])

            # Si no hay texto, saltamos
            if not text.strip():
                continue

            docs.append((doc_id, text, keywords))

    print(f"✅ Cargados {len(docs)} documentos de test.jsonl")

    # Crear directorios destino
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    for idx, (doc_id, text, keywords) in enumerate(docs):
        doc_filename = DOCS_DIR / f"{idx}.txt"
        gold_filename = GOLD_DIR / f"{idx}.key"

        # Guardar texto
        doc_filename.write_text(text, encoding="utf-8")

        # Guardar keywords gold: una por línea, en minúsculas y recortadas
        with gold_filename.open("w", encoding="utf-8") as gf:
            for kw in keywords:
                kw_clean = str(kw).strip()
                if not kw_clean:
                    continue
                gf.write(kw_clean.lower() + "\n")

    print(f"📂 Documentos escritos en: {DOCS_DIR}")
    print(f"📂 Keywords gold escritas en: {GOLD_DIR}")
    print("🎉 Dataset econstor_test preparado para MDERank.")

if __name__ == "__main__":
    main()