import json
import random
from pathlib import Path

# Ruta al fichero original
INPUT = Path("econstor_finance_en.jsonl")
OUT_DIR = Path("data")
OUT_DIR.mkdir(exist_ok=True)

TRAIN_PATH = OUT_DIR / "train.jsonl"
DEV_PATH   = OUT_DIR / "dev.jsonl"
TEST_PATH  = OUT_DIR / "test.jsonl"

random.seed(42)  # para que el split sea reproducible

def load_jsonl(path: Path):
    examples = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            examples.append(json.loads(line))
    return examples

def save_jsonl(path: Path, data):
    with path.open("w", encoding="utf-8") as f:
        for obj in data:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def main():
    examples = load_jsonl(INPUT)
    n = len(examples)
    print(f"Total ejemplos: {n}")

    random.shuffle(examples)

    # 80% train, 10% dev, 10% test
    n_train = int(0.8 * n)
    n_dev   = int(0.1 * n)
    n_test  = n - n_train - n_dev

    train_data = examples[:n_train]
    dev_data   = examples[n_train : n_train + n_dev]
    test_data  = examples[n_train + n_dev :]

    print(f"Train: {len(train_data)}")
    print(f"Dev:   {len(dev_data)}")
    print(f"Test:  {len(test_data)}")

    save_jsonl(TRAIN_PATH, train_data)
    save_jsonl(DEV_PATH, dev_data)
    save_jsonl(TEST_PATH, test_data)

    print("Guardados en:", TRAIN_PATH, DEV_PATH, TEST_PATH)

if __name__ == "__main__":
    main()