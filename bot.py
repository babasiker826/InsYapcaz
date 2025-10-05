from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

def google_arama_bot(aranacak_kelime):
    print(f"🔍 Google'da aranıyor: {aranacak_kelime}")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,720')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Google'a git
        driver.get("https://www.google.com")
        time.sleep(2)
        
        # Arama kutusunu bul
        arama_kutusu = driver.find_element(By.NAME, "q")
        arama_kutusu.send_keys(aranacak_kelime)
        arama_kutusu.send_keys(Keys.RETURN)
        time.sleep(3)
        
        # Sonuçları al
        sonuclar = driver.find_elements(By.CSS_SELECTOR, "h3")[:5]
        sonuc_listesi = [sonuc.text for sonuc in sonuclar if sonuc.text]
        
        driver.quit()
        
        return {
            "status": "success",
            "aranan": aranacak_kelime,
            "sonuclar": sonuc_listesi
        }
        
    except Exception as e:
        driver.quit()
        return {"status": "error", "message": str(e)}

@app.route('/')
def home():
    return """
    <h1>🤖 Selenium Bot Aktif!</h1>
    <p><strong>Kullanabileceğin Endpointler:</strong></p>
    <ul>
        <li><a href="/google?q=selenium">Google Arama Botu</a></li>
        <li><a href="/bot">Basit Bot Testi</a></li>
    </ul>
    """

@app.route('/google')
def google_arama():
    kelime = request.args.get('q', 'Selenium Render')
    sonuc = google_arama_bot(kelime)
    return jsonify(sonuc)

@app.route('/bot')
def bot_test():
    sonuc = google_arama_bot("Render Selenium Bot")
    return f"""
    <h2>Bot Test Sonucu:</h2>
    <pre>{sonuc}</pre>
    <p>Hocam bot çalışıyor! 🎉</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
