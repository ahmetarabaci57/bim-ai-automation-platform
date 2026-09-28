# Production Level Stateful Core - app.py (True Two-Step LLM Reasoning)

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import ollama
import requests
import os
import json

app = FastAPI()

class PromptModel(BaseModel):
    prompt: str

EXCEL_PATH = "fiyat_katalogu.xlsx"
OUTPUT_PATH = "Nihai_Hakedis_Raporu.xlsx"

# Tek kullanıcılı durum/hafıza havuzu (State)
CONVERSATION_HISTORY = []

@app.post("/api/ask-ai")
async def ask_ai_maliyet(data: PromptModel):
    global CONVERSATION_HISTORY
    mimar_promptu = data.prompt
    
    # 1. ATOMİK ARAÇ TANIMI: Sadece ham veriyi getiren saf bir kas sistemi.
    # Yapay zekaya artık alt niyet (sub_action) sormuyoruz, kilitleri tamamen kaldırdık!
    atomic_bim_tool = {
        'type': 'function',
        'function': {
            'name': 'fetch_live_bim_elements',
            'description': 'Revit modelindeki aktif projede bulunan elemanlarin (UniqueId, Kat, Tip) canlı listesini ceker.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'category': {'type': 'string', 'description': "BIM kategori kodu. Örn: 'OST_Windows'"}
                },
                'required': ['category']
            }
        }
    }
    
    CONVERSATION_HISTORY.append({'role': 'user', 'content': mimar_promptu})
    
    # 1. ADIM: Modelin veriye ihtiyacı olup olmadığını sorguluyoruz
    response = ollama.chat(
        model='llama3.1',
        messages=CONVERSATION_HISTORY,
        tools=[atomic_bim_tool]
    )
    
    model_message = response['message']
    
    # Yapay zeka Revit verisini çekmek isterse:
    if model_message.get('tool_calls'):
        try:
            print(">> [BIM API]: Canli Revit modelinden 106 pencere verisi anlik cekiliyor...")
            revit_request = requests.get("http://localhost:8080/get-windows", timeout=5)
            live_bim_data = revit_request.json()
        except Exception as e:
            output_text = f"Hata: Canli calisan Revit programina baglanilamadi. Detay: {str(e)}"
            CONVERSATION_HISTORY.append({'role': 'assistant', 'content': output_text})
            return {"ai_response": output_text}
        
        # ── [NİHAİ DÜZELTME - TWO STEP REASONING] ──
        # Revit'ten aldığımız 106 pencerelik ham listeyi yapay zekaya bir 'Context' (Bağlam) olarak geri enjekte ediyoruz.
        # Ayrıca eğer mimar maliyet/hakediş istediyse arka planda Excel tablosunu otonom basıyoruz.
        
        if any(kelime in mimar_promptu.lower() for kelime in ["hakediş", "maliyet", "bütçe", "fiyat", "cost", "budget"]):
            if os.path.exists(EXCEL_PATH):
                df_excel = pd.read_excel(EXCEL_PATH)
                rapor_satirlari = []
                for element in live_bim_data:
                    revit_type_name = str(element['Type'])
                    match = df_excel[df_excel.apply(lambda row: str(row['Ozellik']).lower() in revit_type_name.lower() or revit_type_name.lower() in str(row['Ozellik']).lower(), axis=1)]
                    if not match.empty:
                        rapor_satirlari.append({
                            "UniqueId": element['UniqueId'], "Level": element['Level'], 
                            "PozNo": match.iloc[0]['PozNo'], "Tip": element['Type'], 
                            "Adet": element['Quantity'], "BirimFiyat": int(match.iloc[0]['BirimFiyat']),
                            "Toplam": int(element['Quantity']) * int(match.iloc[0]['BirimFiyat'])
                        })
                if rapor_satirlari:
                    pd.DataFrame(rapor_satirlari).to_excel(OUTPUT_PATH, index=False)
                    print(f">> [Excel Basarili]: '{OUTPUT_PATH}' disk üzerine yazildi.")

        # Şimdi aldığımız ham Revit JSON listesini yapay zekaya "İşte aradığın veri" diyerek teslim ediyoruz.
        # Yapay zekâ artık listeyi kendi gözleriyle görecek ve mimarın promptuna göre listeleme/sayım yapacak.
        CONVERSATION_HISTORY.append(model_message) # Modelin fonksiyon çağrısını geçmişe ekle
        CONVERSATION_HISTORY.append({
            'role': 'tool',
            'content': json.dumps(live_bim_data), # Canlı 106 pencere verisini LLM hafızasına gömdük!
            'name': 'fetch_live_bim_elements'
        })
        
        # 2. ADIM: Yapay zekayı verilerle birlikte tekrar konuşturuyoruz (Final Muhakeme)
        # [KURAL ENJEKSİYONU]: Modeli yazılımcı gibi kod yazmaktan men edip, tamamen mimarın dilinden konuşmaya zorluyoruz.
        
        # Hafıza zincirinin en başına çok güçlü bir Sistem Rolü yerleştiriyoruz
        messages_with_system_role = [
            {
                'role': 'system', 
                'content': (
                    "Sen profesyonel bir BIM ve Hakediş Uzmanısın. Önünde canlı Revit modelinden gelen gerçek veriler duruyor. "
                    "Kesinlikle Python kodu, teknik açıklama veya veri şeması yazma! Mimara doğrudan, net ve Türkçe bir cevap ver. "
                    "Örneğin: 'Canlı Revit modelinden alınan verilere göre projenizde toplam X adet pencere vardır' şeklinde konuş."
                )
            }
        ] + CONVERSATION_HISTORY # Mevcut konuşma geçmişini bu kuralın arkasına ekle

        final_response = ollama.chat(
            model='llama3.1',
            messages=messages_with_system_role # Güncellenmiş sistem kurallı geçmişi gönderiyoruz
        )
        output_text = final_response['message']['content']

        
    else:
        # Veriye ihtiyaç duymayan düz konuşmalar
        output_text = model_message['content']
        
    CONVERSATION_HISTORY.append({'role': 'assistant', 'content': output_text})
    return {"ai_response": output_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
