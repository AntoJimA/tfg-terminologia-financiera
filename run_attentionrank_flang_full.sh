#!/usr/bin/env bash
set -e

echo "📌 [1/5] Limpiando outputs anteriores de econstor..."
#rm -rf econstor/docsutf8
rm -rf econstor/processed_econstor
rm -rf econstor/res*
rm -f econstor/predictions_top15.jsonl
rm -f econstor/predictions_flang_top15.jsonl

echo "📌 [2/5] Ejecutando AttentionRank (pipeline completa) con FLANG-ELECTRA..."

python attentionrank/main.py \
  --dataset_name econstor \
  --model_name_or_path SALT-NLP/FLANG-ELECTRA \
  --model_type bert \
  --lang en \
  --type_execution exec \
  --k_value 15

echo "📌 [3/5] Exportando top-15 keywords desde processed_econstor/candidate_cross_attn_value..."

python attentionrank/export_attentionrank_predictions.py \
  --dataset_name econstor \
  --top_k 15

if [ -f "econstor/predictions_top15.jsonl" ]; then
  mv econstor/predictions_top15.jsonl econstor/predictions_flang_top15.jsonl
  echo "✅ Predicciones guardadas en econstor/predictions_flang_top15.jsonl"
else
  echo "⚠️ No se ha encontrado econstor/predictions_top15.jsonl. Algo ha fallado en la exportación."
fi

echo "🎉 Pipeline completa para FLANG-ELECTRA finalizada."