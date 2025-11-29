import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.utils.class_weight import compute_class_weight
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

# --- 3. VERİ SETİNİ HAZIRLA ---
CSV_DOSYA_ADI = "veri_seti_tum.csv"
TEMEL_MODEL = "hazal/BioBERTurkcased-con-trM"

print(f"'{CSV_DOSYA_ADI}' okunuyor...")
df = pd.read_csv(CSV_DOSYA_ADI)


labels = df['label'].unique().tolist()
labels.sort()
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for i, label in enumerate(labels)}

df['label'] = df['label'].map(label2id)
print(f"Toplam {len(labels)} sınıf bulundu.")

train_df, test_df = train_test_split(df, test_size=0.1, random_state=42, stratify=df['label'])

train_dataset = Dataset.from_pandas(train_df.reset_index(drop=True))
test_dataset = Dataset.from_pandas(test_df.reset_index(drop=True))

print(f"Eğitim Verisi: {len(train_dataset)} | Test Verisi: {len(test_dataset)}")

# --- 4. DENGESİZ VERİ İÇİN AĞIRLIK HESAPLAMA (CRITICAL STEP) ---

print("Sınıf ağırlıkları hesaplanıyor...")
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_df['label']),
    y=train_df['label']
)
weights_tensor = torch.tensor(class_weights, dtype=torch.float)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
weights_tensor = weights_tensor.to(device)
print("Ağırlıklar hazırlandı.")

# --- 5. TOKENIZER VE MODEL ---
tokenizer = AutoTokenizer.from_pretrained(TEMEL_MODEL)

model = AutoModelForSequenceClassification.from_pretrained(
    TEMEL_MODEL,
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True
)
model.to(device)


def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, padding=True, max_length=128)


print("Tokenization işlemi başlıyor (Biraz sürebilir)...")
tokenized_train = train_dataset.map(preprocess_function, batched=True)
tokenized_test = test_dataset.map(preprocess_function, batched=True)


# --- 6. CUSTOM TRAINER (Ağırlıklı Loss Fonksiyonu İçin) ---
class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.get("labels")
        outputs = model(**inputs)
        logits = outputs.get("logits")
        loss_fct = nn.CrossEntropyLoss(weight=weights_tensor)
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='weighted')
    acc = accuracy_score(labels, predictions)
    return {'accuracy': acc, 'f1': f1, 'precision': precision, 'recall': recall}


# --- 7. OPTİMİZE EDİLMİŞ EĞİTİM AYARLARI ---
training_args = TrainingArguments(
    output_dir="./sonuc_model",

    fp16=True,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=2,

    # --- Eğitim Stratejisi ---
    num_train_epochs=2,
    learning_rate=3e-5,
    weight_decay=0.01,

    # --- Kayıt ve Log ---
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    logging_steps=500,
    dataloader_num_workers=2
)

trainer = CustomTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

print("--- EĞİTİM BAŞLIYOR (Tahmini Süre: 2-3 Saat) ---")
trainer.train()

# --- 8. KAYIT ---
KAYIT_YERI = "./final_hastane_modeli"
trainer.save_model(KAYIT_YERI)
tokenizer.save_pretrained(KAYIT_YERI)
print(f"Eğitim Bitti! Model '{KAYIT_YERI}' klasörüne kaydedildi.")

import shutil

shutil.make_archive("final_hastane_modeli", 'zip', KAYIT_YERI)
print("Zip dosyası hazır.")