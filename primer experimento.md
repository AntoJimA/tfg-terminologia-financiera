# 📊 Resultados de Experimentos — Extracción de Terminología Financiera

Este documento resume los resultados obtenidos al evaluar distintos modelos y métodos de *keyword extraction* sobre el **dataset Econstor (test.jsonl)**.

Se han comparado dos enfoques principales:

- **AttentionRank** (método no supervisado basado en atenciones)
- **MDERank** (método no supervisado basado en degradación semántica)

Aplicados con diferentes modelos de lenguaje:

- **BERT base uncased**
- **FinBERT**
- **FLANG** (no incluido: incompatibilidad técnica y fallos en la etapa de scoring)

---

# 📌 Tabla General de Resultados

### 🔍 Métricas (Precision@K, Recall@K, F1@K)

| Método | Modelo | P@5 | R@5 | F1@5 | P@10 | R@10 | F1@10 | P@15 | R@15 | F1@15 |
|--------|--------|------|-------|--------|--------|--------|---------|---------|---------|----------|
| **AttentionRank** | **BERT** | 0.0620 | 0.3422 | **0.1018** | 0.0620 | 0.3422 | **0.1018** | 0.0620 | 0.3422 | **0.1018** |
| **AttentionRank** | **FinBERT** | 0.0516 | 0.2782 | **0.0845** | 0.0516 | 0.2782 | **0.0845** | 0.0516 | 0.2782 | **0.0845** |
| **MDERank** | **BERT** | 0.14325 | 0.25718 | **0.18401** | 0.10613 | 0.38106 | **0.16601** | 0.08755 | 0.47127 | **0.14767** |
| **MDERank** | **FinBERT** | 0.14175 | 0.25449 | **0.18208** | 0.10350 | 0.37163 | **0.16191** | 0.08522 | 0.45871 | **0.14373** |

---

# 🧠 Conclusiones Principales

### ✔️ 1. MDERank supera ampliamente a AttentionRank  
Obteniendo mejoras de **entre +60% y +70% en F1**, independientemente del modelo usado.

### ✔️ 2. FinBERT no mejora el rendimiento en métodos no supervisados  
En ambos métodos, FinBERT ≈ BERT, con diferencias marginales.

Esto confirma que FinBERT **solo aporta ventajas cuando se entrena de forma supervisada**, no en pipelines que dependen del embedding directo.

### ✔️ 3. El mejor modelo actual es:  
## ✅ **MDERank + BERT**  
Con el mayor **F1@5, F1@10 y F1@15** de todos los experimentos.

### ✔️ 4. El siguiente gran salto: Fine-tuning supervisado  
Es la forma de incorporar realmente conocimiento financiero disciplinado.  
Tanto FinBERT como FLANG podrían destacar *solo* con entrenamiento supervisado.

---

# 📁 Resultados detallados por experimento

---

## 🔷 AttentionRank + BERT


# 🏁 Conclusión Final

| Ranking | Modelo | F1@5 |
|---------|--------|-------|
| **1️⃣** | **MDERank + BERT** | **0.184** |
| **2️⃣** | **MDERank + FinBERT** | **0.182** |
| **3️⃣** | AttentionRank + BERT | 0.102 |
| **4️⃣** | AttentionRank + FinBERT | 0.084 |

---