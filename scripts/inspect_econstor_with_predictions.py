import json
from pathlib import Path
import argparse


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--idx",
        type=int,
        required=True,
        help="Índice del documento que quieres inspeccionar (ej: 100)",
    )
    parser.add_argument(
        "--gold_path",
        type=str,
        default="data/test.jsonl",
        help="Ruta al JSONL de test con texto y gold keywords",
    )
    parser.add_argument(
        "--pred_path",
        type=str,
        default="econstor/predictions_bert_top15.jsonl",
        help="Ruta al JSONL con las predicciones de AttentionRank",
    )
    args = parser.parse_args()

    gold_file = Path(args.gold_path)
    pred_file = Path(args.pred_path)

    if not gold_file.exists():
        raise FileNotFoundError(f"No se encuentra el archivo gold: {gold_file}")
    if not pred_file.exists():
        raise FileNotFoundError(f"No se encuentra el archivo de predicciones: {pred_file}")

    print(f"Cargando GOLD desde: {gold_file}")
    gold_data = list(load_jsonl(gold_file))
    print(f"Cargando predicciones desde: {pred_file}")
    pred_data = []
    with pred_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            pred_data.append(json.loads(line))

    idx = args.idx

    if idx < 0 or idx >= len(gold_data):
        raise IndexError(
            f"Índice {idx} fuera de rango. El GOLD tiene {len(gold_data)} documentos."
        )

    gold_obj = gold_data[idx]

    # doc_id original por si lo quieres mirar
    print("\n========== GOLD ==========")
    print(f"idx: {idx}")
    print(f"gold.doc_id: {gold_obj.get('doc_id')}")

    text = (
        gold_obj.get("text")
        or gold_obj.get("text_en")
        or gold_obj.get("document")
        or ""
    )
    gold_kw = (
        gold_obj.get("keywords")
        or gold_obj.get("gold_keywords")
        or []
    )

    print("\nTexto (primeros 800 caracteres):\n")
    print(text[:800])
    print("\nGold keywords:")
    print(gold_kw)

    pred_by_id = {str(obj["doc_id"]): obj for obj in pred_data}
    pred_obj = pred_by_id.get(str(idx))

    if pred_obj is None:
        print("\n⚠️ No he encontrado predicciones para este índice.")
    else:
        print("\n========== PREDICCIONES (AttentionRank) ==========")
        print(f"pred.doc_id (índice en predicciones): {pred_obj.get('doc_id')}")
        print("\nPredicted keywords:")
        print(pred_obj.get("predicted_keywords", []))


if __name__ == "__main__":
    main()