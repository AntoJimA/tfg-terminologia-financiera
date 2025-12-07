#!/usr/bin/env bash
set -e

# Ir a la raíz del proyecto (por si lo lanzas desde otro sitio)
cd "$(dirname "$0")"

# Activar entorno virtual
source venv/bin/activate

# Lanzar MDERank con BERT base sobre el dataset ECONSTOR (test)
python mderank/MDERank/mderank_main.py \
  --dataset_dir mdeRank/data/econstor_test \
  --dataset_name econstor_test \
  --doc_embed_mode mean \
  --layer_num -1 \
  --batch_size 4 \
  --log_dir mderank/logs/ \
  --model_type bert \
  --lang en \
  --type_execution eval \
  --model_name_or_path bert-base-uncased