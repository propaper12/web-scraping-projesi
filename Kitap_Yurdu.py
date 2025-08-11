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

dosya_adi = "kitap_verileri.csv"
tum_veriler = pd.DataFrame()

cekilecek_sayfa_sayisi = 36

ana_url = "https://www.kitapyurdu.com/index.php?route=product/bargain&category=0&discount=50&filter_in_stock=1&limit=100"

try:
    for sayfa_numarasi in range(1, cekilecek_sayfa_sayisi + 1):
        sayfa_url = f"{ana_url}&page={sayfa_numarasi}"
        print(f"\n{sayfa_numarasi}. sayfaya gidiliyor: {sayfa_url}")

        driver.get(sayfa_url)
        time.sleep(random.uniform(4, 7))

        sayfa_kaynagi = driver.page_source
        soup = BeautifulSoup(sayfa_kaynagi, "html.parser")

        urun_listesi_divi = soup.find_all("div", class_="product-cr")

        if not urun_listesi_divi:
            print(f"Hata: {sayfa_numarasi}. sayfada ürünler bulunamadı. Belki sayfa bitti?")
            continue

        for kitap_karti in urun_listesi_divi:
            kitap_bilgileri = {}

            baslik_div = kitap_karti.find("div", class_="name ellipsis")
            kitap_bilgileri['Baslik'] = baslik_div.text.strip() if baslik_div else "Yok"

            yazar_div = kitap_karti.find("div", class_="author")
            yazar_adi = yazar_div.find("a").text.strip() if yazar_div and yazar_div.find("a") else "Yok"
            kitap_bilgileri['Yazar'] = yazar_adi

            yayinevi_div = kitap_karti.find("div", class_="publisher")
            kitap_bilgileri['Yayinevi'] = yayinevi_div.text.strip() if yayinevi_div else "Yok"

            fiyat_div = kitap_karti.find("div", class_="price-new")
            kitap_bilgileri['Fiyat (TL)'] = fiyat_div.find("span", class_="value").text.strip().replace(",", ".") if fiyat_div and fiyat_div.find("span", class_="value") else "Yok"

            urun_detay_div = kitap_karti.find("div", class_="product-info")
            kitap_bilgileri['Sayfa Sayisi'] = 'Yok'
            kitap_bilgileri['Kitap Dili'] = 'Yok'
            kitap_bilgileri['Yayin Tarihi'] = 'Yok'

            if urun_detay_div:
                detay_metni = urun_detay_div.text.strip().replace("\n", "").replace("\t", "").replace("\r", "")

                if "TÜRKÇE" in detay_metni:
                    kitap_bilgileri['Kitap Dili'] = 'TÜRKÇE'
                elif "İNGİLİZCE" in detay_metni:
                    kitap_bilgileri['Kitap Dili'] = 'İNGİLİZCE'

                metin_parcalari = detay_metni.split('|')
                if len(metin_parcalari) > 2:
                    sayfa_metni = metin_parcalari[2].strip()
                    sayi_bul = re.search(r'\d+', sayfa_metni)
                    if sayi_bul:
                        kitap_bilgileri['Sayfa Sayisi'] = sayi_bul.group(0)

                tarih_bul = re.search(r'\d{4}-\d{2}-\d{2}', detay_metni)
                if tarih_bul:
                    kitap_bilgileri['Yayin Tarihi'] = tarih_bul.group(0)

            tum_veriler = pd.concat([tum_veriler, pd.DataFrame([kitap_bilgileri])], ignore_index=True)

            print(f"  {kitap_bilgileri['Baslik']} çekildi. Yazar: {kitap_bilgileri['Yazar']}")

    tum_veriler.to_csv(dosya_adi, index=False, encoding="utf-8-sig")
    print(f"\n{cekilecek_sayfa_sayisi} sayfadan toplam {len(tum_veriler)} ürün verisi '{dosya_adi}' dosyasına kaydedildi.")

except WebDriverException as e:
    print(f"Tarayıcıyla ilgili bir hata oluştu: {e}")
    print("İşlem durduruldu. Lütfen daha sonra tekrar deneyin.")
except Exception as e:
    print(f"Genel bir hata oluştu: {e}")
    print("İşlem durduruldu. Lütfen daha sonra tekrar deneyin.")
finally:
    driver.quit()
    print("\nVeri çekme işlemi tamamlandı.")