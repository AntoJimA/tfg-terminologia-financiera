#!/usr/bin/env bash
set -e

# Ir a la raíz del proyecto (por si lo lanzas desde otro sitio)
cd "$(dirname "$0")"

# Activar entorno virtual
source venv/bin/activate

# Lanzar MDERank con FinBERT sobre el dataset SemEval2017 incluido en mderank/data
python mderank/MDERank/mderank_main.py \
  --dataset_dir mderank/data/SemEval2017 \
  --dataset_name SemEval2017 \
  --doc_embed_mode mean \
  --layer_num -1 \
  --batch_size 4 \
  --log_dir mderank/logs/ \
  --model_type bert \
  --lang en \
  --type_execution eval \
  --model_name_or_path ProsusAI/finbert