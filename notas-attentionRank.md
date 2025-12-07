Fichero main.oy lineas 86 a 92 tenemos automode y tokenizer

He cambiado para que use el AutoModel 

comandos para correr esto:

# Baseline
python main.py --dataset_name example --model_type bert --lang en --type_execution exec --k_value 15 --model_name_or_path bert-base-uncased

# FinBERT
python main.py --dataset_name example --model_type bert --lang en --type_execution exec --k_value 15 --model_name_or_path yiyanghkust/finbert-pretrain

# FLANG
python main.py --dataset_name example --model_type bert --lang en --type_execution exec --k_value 15 --model_name_or_path SALT-NLP/FLANG-BERT