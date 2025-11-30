#!/bin/bash

# --- 1. Moverse a la raíz del repo ---
cd "$(dirname "$0")"

echo "📌 Ejecutando AttentionRank (pipeline completa)..."
echo "--------------------------------------------------"

# --- 2. Activar entorno virtual ---
source venv/bin/activate

# --- 3. Ejecutar pipeline completa ---
python attentionrank/main.py \
  --dataset_name econstor \
  --model_name_or_path bert-base-uncased \
  --model_type bert \
  --lang en \
  --type_execution exec \
  --k_value 15

echo "✅ Pipeline AttentionRank completada"
echo

# --- 4. Ejecutar el script de exportación ---
echo "📌 Exportando top-15 keywords desde candidate_cross_attn_value..."
echo "-----------------------------------------------------------------"

cd attentionrank

python export_attentionrank_predictions.py \
  --dataset_name econstor \
  --top_k 15

echo
echo "🎉 Proceso finalizado."
echo "👉 Archivo generado en attentionrank/econstor/predictions_top15.jsonl"