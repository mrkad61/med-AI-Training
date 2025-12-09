import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "./model"


def main():
    print("=================================================")
    print("   HASTANE YAPAY ZEKA ASİSTANI - LOCAL TEST")
    print("=================================================")

    print(f"Model yükleniyor: {MODEL_PATH} ...")
    try:
        device = torch.device("cpu")

        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        model.to(device)
        model.eval()
        print("Model başarıyla yüklendi! Hazır.\n")
    except Exception as e:
        print(f"HATA: Model yüklenemedi. Klasör yolunu kontrol et.\nDetay: {e}")
        return

    id2label = model.config.id2label

    while True:
        text = input("\nŞikayetiniz nedir? (Çıkış için 'q'): ")

        if text.lower() == 'q':
            print("Çıkış yapılıyor...")
            break

        if not text.strip():
            continue

        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128).to(device)

        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits

        probs = F.softmax(logits, dim=1)[0]

        top_probs, top_indices = torch.topk(probs, 3)

        print("\n---------------------------------")
        print(f"Girdi: '{text}'")
        print("---------------------------------")

        for i in range(3):
            score = top_probs[i].item() * 100  # Yüzdeye çevir
            label_index = top_indices[i].item()
            label_name = id2label[label_index]

            bar = "▓" * int(score / 5)  # Her %5 için bir blok

            print(f"{i + 1}. {label_name:<25} : %{score:.2f}  {bar}")

        en_yuksek_skor = top_probs[0].item()
        if en_yuksek_skor < 0.60:
            print("\n⚠️  UYARI: Model tam emin olamadı. Hastaya ek soru sorulmalı.")
        else:
            print(f"\n✅ Yönlendirme: {id2label[top_indices[0].item()]}")


if __name__ == "__main__":
    main()