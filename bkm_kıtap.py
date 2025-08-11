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

dosya_adi = "bkm_kitap_verileri.csv"
tum_veriler = pd.DataFrame()

url = "https://www.bkmkitap.com/edebiyat-kitaplari"
print(f"Veriler bu adresten çekiliyor: {url}")

try:
    driver.get(url)
    time.sleep(5)

    last_product_count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(3, 5))

        sayfa_kaynagi = driver.page_source
        soup = BeautifulSoup(sayfa_kaynagi, "html.parser")
        urun_listesi = soup.find_all("div", class_="product-item-catalog")
        current_product_count = len(urun_listesi)

        if current_product_count > last_product_count:
            print(f"Sayfa kaydırılıyor... (Şu anki çekilen veri sayısı: {current_product_count})")
            last_product_count = current_product_count
        else:
            print("\nSayfanın sonuna ulaşıldı.")
            cevap = input("Daha fazla veri çekmek için elle sayfayı kaydırdıysanız 'evet' yazın, durdurmak için 'hayır': ").lower().strip()
            if cevap != 'evet':
                print("Kullanıcı isteği üzerine veri çekme durduruldu.")
                break

            print("Kaydırmaya devam ediliyor...")

    sayfa_kaynagi = driver.page_source
    soup = BeautifulSoup(sayfa_kaynagi, "html.parser")
    urun_listesi = soup.find_all("div", class_="product-item-catalog")

    if not urun_listesi:
        print("Hata: Sayfada hiç ürün bulamadım.")
    else:
        all_products = []
        for urun in urun_listesi:
            veri = {}

            baslik_div = urun.find("a", class_="product-title")
            veri['Başlık'] = baslik_div.text.strip() if baslik_div else "Yok"

            yayinevi_div = urun.find("a", class_="brand-title")
            veri['Yayınevi'] = yayinevi_div.text.strip() if yayinevi_div else "Yok"

            yazar_div = urun.find("a", class_="model-title")
            veri['Yazar'] = yazar_div.text.strip() if yazar_div else "Yok"

            indirimli_div = urun.find("div", class_="current-price")
            indirimsiz_span = urun.find("span", class_="product-price-not-discounted")

            veri['İndirimli Fiyat (TL)'] = "Yok"
            veri['İndirimsiz Fiyat (TL)'] = "Yok"

            if indirimsiz_span and indirimli_div:
                veri['İndirimsiz Fiyat (TL)'] = indirimsiz_span.text.strip().replace(" TL", "").replace(",", ".") if indirimsiz_span else "Yok"
                veri['İndirimli Fiyat (TL)'] = indirimli_div.find("span", class_="product-price").text.strip().replace(" TL", "").replace(",", ".") if indirimli_div and indirimli_div.find("span", class_="product-price") else "Yok"
            elif indirimli_div:
                fiyat_metni = indirimli_div.find("span", class_="product-price").text.strip().replace(" TL", "").replace(",", ".") if indirimli_div and indirimli_div.find("span", class_="product-price") else "Yok"
                veri['İndirimsiz Fiyat (TL)'] = fiyat_metni
                veri['İndirimli Fiyat (TL)'] = fiyat_metni

            indirim_div = urun.find("span", class_="product-discount")
            veri['İndirim Oranı (%)'] = indirim_div.text.strip() if indirim_div else "Yok"

            puanlama_div = urun.find("span", class_="stars-fill")
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