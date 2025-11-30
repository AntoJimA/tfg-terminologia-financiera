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


def normalize_kw_list(kws):
    if isinstance(kws, str):
        # Por si en algún sitio vinieran como cadena separada por |
        parts = [p.strip() for p in kws.split("|")]
    else:
        parts = kws or []
    return {p.lower().strip() for p in parts if p.strip()}


def eval_model(gold_path: Path, pred_path: Path):
    gold_data = list(load_jsonl(gold_path))
    pred_data = list(load_jsonl(pred_path))

    # Mapeamos predicciones por doc_id = índice
    pred_by_id = {str(obj["doc_id"]): obj for obj in pred_data}

    total_p = 0.0
    total_r = 0.0
    total_f1 = 0.0
    count = 0

    for idx, gold_obj in enumerate(gold_data):
        gold_kws = gold_obj.get("keywords") or gold_obj.get("gold_keywords") or []
        gold_set = normalize_kw_list(gold_kws)

        pred_obj = pred_by_id.get(str(idx))
        if pred_obj is None:
            # Sin predicciones -> P=R=F1=0
            count += 1
            continue

        pred_kws = pred_obj.get("predicted_keywords", [])
        pred_set = normalize_kw_list(pred_kws)

        if not pred_set and not gold_set:
            count += 1
            continue

        inter = gold_set & pred_set
        tp = len(inter)
        p = tp / max(len(pred_set), 1)
        r = tp / max(len(gold_set), 1)
        f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0

        total_p += p
        total_r += r
        total_f1 += f1
        count += 1

    if count == 0:
        return 0.0, 0.0, 0.0

    return total_p / count, total_r / count, total_f1 / count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gold_path",
        type=str,
        default="data/test.jsonl",
        help="Ruta al JSONL con el gold estándar (text + keywords).",
    )
    parser.add_argument(
        "--pred_path",
        type=str,
        required=True,
        help="Ruta al JSONL con las predicciones de un modelo.",
    )
    args = parser.parse_args()

    gold = Path(args.gold_path)
    pred = Path(args.pred_path)

    p, r, f1 = eval_model(gold, pred)

    print(f"Evaluación sobre {gold}:")
    print(f"  Predicciones: {pred}")
    print(f"  Precision@K media: {p:.4f}")
    print(f"  Recall@K medio:    {r:.4f}")
    print(f"  F1@K medio:        {f1:.4f}")


if __name__ == "__main__":
    main()