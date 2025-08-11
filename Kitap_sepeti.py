import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
import re

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

dosya_adi = "kitapsepeti_edebiyat_verileri.csv"
tum_veriler = pd.DataFrame()

base_url = "https://www.kitapsepeti.com/edebiyat?stock=1"

try:
    print(f"\n{base_url} adresindeki verileri çekmeye başlıyorum.")
    driver.get(base_url)
    time.sleep(5)

    last_product_count = 0
    while True:
        # Sayfanın en altına kaydır
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(3, 5))

        sayfa_kaynagi = driver.page_source
        soup = BeautifulSoup(sayfa_kaynagi, "html.parser")
        urun_listesi = soup.find_all("div", class_="product-item")
        current_product_count = len(urun_listesi)

        if current_product_count > last_product_count:
            # Yeni ürünler yüklendi, kaydırmaya devam et
            print(f"Sayfa kaydırılıyor... (Şu anki ürün sayısı: {current_product_count})")
            last_product_count = current_product_count
        else:
            # Yeni ürün yüklenmedi, kullanıcı müdahalesi için bekle
            print("\nYeni ürün yüklenmedi. Sayfanın sonuna gelmiş veya takılmış olabilir.")
            cevap = input("Daha fazla veri çekmeye devam etmek istiyor musunuz? (evet/hayır): ").lower().strip()
            if cevap != 'evet':
                print("Kullanıcı isteği üzerine veri çekme durduruldu.")
                break

            # Kullanıcı "evet" derse, sayfayı tekrar en alta kaydır
            print("Kaydırmaya devam ediliyor...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(3, 5))

    # Döngü bittiğinde veya durdurulduğunda verileri çek
    sayfa_kaynagi = driver.page_source
    soup = BeautifulSoup(sayfa_kaynagi, "html.parser")
    urun_listesi = soup.find_all("div", class_="product-item")

    if not urun_listesi:
        print("Hata: Sayfada hiç ürün bulamadım.")
    else:
        all_products = []
        for urun_karti in urun_listesi:
            veri = {}

            baslik_div = urun_karti.find("a", class_="product-title")
            veri['Başlık'] = baslik_div.text.strip() if baslik_div else "Yok"

            yayinevi_div = urun_karti.find("a", class_="brand-title")
            veri['Yayınevi'] = yayinevi_div.text.strip() if yayinevi_div else "Yok"

            yazar_div = urun_karti.find("a", class_="model-title")
            veri['Yazar'] = yazar_div.text.strip() if yazar_div else "Yok"

            normal_fiyat_div = urun_karti.find("span", class_="product-price-not-discounted")
            indirimli_fiyat_div = urun_karti.find("span", class_="product-price")
            indirim_orani_span = urun_karti.find("span", class_="product-discount")

            veri['İndirimsiz Fiyat (TL)'] = normal_fiyat_div.text.strip().replace(" TL", "").replace(",", ".") if normal_fiyat_div else "Yok"
            veri['İndirimli Fiyat (TL)'] = indirimli_fiyat_div.text.strip().replace(" TL", "").replace(",", ".") if indirimli_fiyat_div else "Yok"
            veri['İndirim Oranı (%)'] = indirim_orani_span.text.strip() if indirim_orani_span else "Yok"

            puanlama_div = urun_karti.find("span", class_="stars-fill")
            veri['Puanlama (5 üzerinden)'] = "Yok"
            if puanlama_div and "style" in puanlama_div.attrs:
                stil = puanlama_div['style']
                yuzde_eslesme = re.search(r'width:(\d+)%', stil)
                if yuzde_eslesme:
                    yuzde = int(yuzde_eslesme.group(1))
                    puan = (yuzde / 100) * 5
                    veri['Puanlama (5 üzerinden)'] = round(puan, 1)

            all_products.append(veri)
            print(f"  --> {veri['Başlık']} adlı kitap çekildi, fiyatı {veri['İndirimli Fiyat (TL)']} TL.")

        tum_veriler = pd.concat([tum_veriler, pd.DataFrame(all_products)], ignore_index=True)

    tum_veriler.to_csv(dosya_adi, index=False, encoding="utf-8-sig")
    print(f"\nVeri çekme işlemi tamamlandı! Toplam {len(tum_veriler)} ürün '{dosya_adi}' dosyasına kaydedildi.")

except WebDriverException as e:
    print(f"Tarayıcıyla ilgili bir hata çıktı: {e}")
except Exception as e:
    print(f"Bilinmeyen bir hata oluştu: {e}")
finally:
    driver.quit()
    print("\nProgram bitti, tarayıcı kapandı.")