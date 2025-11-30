import os
import csv
import json
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)


def export_predictions(dataset_name: str, top_k: int = 15):
    """
    Lee los ficheros *_candidate_cross_attn_value.csv generados por AttentionRank
    y crea un JSONL con las top-k keywords por documento.

    Supone que el script se ejecuta desde la carpeta 'attentionrank'
    y que la estructura es:
      ./<dataset_name>/processed_<dataset_name>/candidate_cross_attn_value/*.csv

    Salida: ./<dataset_name>/predictions_top<k>.jsonl
    """

    # Carpeta del dataset, p.ej. /ruta/al/repo/econstor
    dataset_dir = os.path.join(ROOT_DIR, dataset_name)
    processed_dir = os.path.join(dataset_dir, f"processed_{dataset_name}")
    cross_dir = os.path.join(processed_dir, "candidate_cross_attn_value")

    if not os.path.isdir(cross_dir):
        raise FileNotFoundError(
            f"No existe el directorio {cross_dir}. ¿Se ha ejecutado STEP 10 para {dataset_name}?"
        )

    out_path = os.path.join(dataset_dir, f"predictions_top{top_k}.jsonl")
    num_docs = 0

    with open(out_path, "w", encoding="utf-8") as out_f:
        # Recorremos todos los CSV de candidate_cross_attn_value
        for fname in sorted(os.listdir(cross_dir)):
            if not fname.endswith("_candidate_cross_attn_value.csv"):
                continue

            # ID del documento = parte antes del primer "_"
            doc_id = fname.split("_")[0]
            full_path = os.path.join(cross_dir, fname)

            candidates = []
            with open(full_path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    term = row[0].strip().lower()
                    if not term:
                        continue
                    try:
                        score = float(row[1])
                    except (ValueError, IndexError):
                        continue
                    candidates.append((term, score))

            if not candidates:
                # Documento sin candidatos válidos: lo guardamos vacío igualmente
                obj = {"doc_id": doc_id, "predicted_keywords": []}
                out_f.write(json.dumps(obj, ensure_ascii=False) + "\n")
                num_docs += 1
                continue

            # Ordenar por score descendente y quedarnos con el top-k
            candidates.sort(key=lambda x: x[1], reverse=True)
            top_terms = [t for t, _ in candidates[:top_k]]

            obj = {
                "doc_id": doc_id,
                "predicted_keywords": top_terms,
            }
            out_f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            num_docs += 1

    print(f"Guardado {num_docs} documentos en {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Exportar predicciones de AttentionRank (candidate_cross_attn_value) a JSONL."
    )
    parser.add_argument(
        "--dataset_name",
        type=str,
        default="econstor",
        help="Nombre del dataset (carpeta dentro de attentionrank). Ej: econstor",
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=15,
        help="Número de keywords a exportar por documento.",
    )
    args = parser.parse_args()

    export_predictions(args.dataset_name, args.top_k)


if __name__ == "__main__":
    main()