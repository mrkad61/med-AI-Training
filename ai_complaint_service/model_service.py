import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from safetensors.torch import load_file
import os

class ModelService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.tokenizer = None
            cls._instance.model_path = "C:/Users/asdha/PycharmProjects/TestAIApp/ai_complaint_service/model_v2" # Modelin bulanacağı klasör
        return cls._instance

    def load_model(self):
        """
        Modeli ve tokenizer'ı yükler.
        Eğer model dosyaları yoksa mock (taklit) modunda çalışabilir veya hata fırlatabilir.
        Şimdilik user'ın model dosyasını 'model/' klasörüne koyacağını varsayıyoruz.
        """
        if os.path.exists(self.model_path):
            try:
                print(f"Model yükleniyor: {self.model_path}...")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
                # Safetensors formatını otomatik algılar
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path, use_safetensors=True)
                self.model.eval()
                print("Model başarıyla yüklendi.")
            except Exception as e:
                print(f"Model yüklenirken hata oluştu: {e}")
                print("Lütfen 'model/' klasöründe 'model.safetensors', 'config.json' ve 'tokenizer.json' olduğundan emin olun.")
        else:
            print(f"UYARI: Model klasörü bulunamadı ({self.model_path}).")
            print("Lütfen model dosyanızı (model.safetensors ve config dosyaları) proje içine 'model' klasörüne kopyalayın.")

    def predict(self, text: str):
        if not self.model or not self.tokenizer:
            # Model yüklenemediyse mock cevap dönelim (Test amaçlı)
            return {"label": "MOCK_RESULT", "score": 0.0}

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Top-K (örneğin Top 5) skorları al
        top_k_scores, top_k_indices = torch.topk(probabilities, k=min(5, probabilities.shape[-1]), dim=-1)
        
        predictions_list = []
        for score, idx in zip(top_k_scores[0], top_k_indices[0]):
            label_text = str(idx.item())
            if hasattr(self.model.config, 'id2label') and self.model.config.id2label:
                 label_text = self.model.config.id2label[idx.item()]
            
            predictions_list.append({
                "label": label_text,
                "score": float(score)
            })

        # En yüksek skorlu olanı ana cevap olarak da dönelim (geriye uyumluluk için)
        best_prediction = predictions_list[0]
        
        return {
            "label": best_prediction["label"], 
            "score": best_prediction["score"],
            "predictions": predictions_list
        }
