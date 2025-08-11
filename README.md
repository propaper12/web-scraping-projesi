# Python Web Scraping ve Kitap Karşılaştırma Projesi

## Proje Hakkında
Bu projenin temel amacı, farklı online kitap satış platformlarından (Kitapyurdu, BKM Kitap, İdefix) kitap verilerini çekmek, tek bir veri setinde birleştirmek ve kullanıcı dostu bir arayüzle karşılaştırmaktır. Proje, hem web scraping becerilerini hem de  uygulama geliştirme yeteneklerini sergilemektedir.

## Özellikler
Çoklu Site Desteği: Kitapyurdu, BKM Kitap ve İdefix gibi sitelerden veri çekebilme.
Dinamik Veri Çekimi: Sonsuz kaydırma (infinite scroll) ve pagination gibi dinamik sayfa yapılarıyla başa çıkabilme.
Veri Birleştirme: Farklı sitelerden çekilen verileri pandas ile tek bir çatı altında toplama.
Modern Arayüz: PyQt5 ile geliştirilmiş, kullanıcıların veri setlerini yükleyip kolayca arama ve karşılaştırma yapabileceği modern bir grafik arayüzü (GUI).
Akıllı Karşılaştırma: Aynı başlıktaki kitapları bulup fiyat ve diğer özelliklerini karşılaştırma.

## Kullanılan Teknolojiler
Python
Selenium (Tarayıcı otomasyonu için)
BeautifulSoup (HTML ayrıştırma için)
Pandas (Veri analizi ve manipülasyonu için)
PyQt5 (Grafik arayüzü için)

Bu projenin çalışabilmesi için sisteminizde yüklü olan Google Chrome tarayıcısına uygun chromedriver.exe dosyasını indirmeniz gerekmektedir.
Chrome Sürümünüzü Kontrol Edin: Tarayıcınızı açın ve adres çubuğuna chrome://version yazarak Chrome sürüm numaranızı öğrenin.
chromedriver Sürümünü İndirin: (https://developer.chrome.com/docs/chromedriver/downloads?hl=tr) Sürüm numaranıza uygun chromedriver.exe dosyasını indirmek için ChromeDriver resmi indirme sayfasına gidin.
Dosyayı Kopyalayın: İndirdiğiniz chromedriver.exe dosyasını, Python projenizin (.py dosyalarının) bulunduğu aynı klasöre kopyalayın.
Bu adımları tamamladıktan sonra projeniz sorunsuz bir şekilde çalışacaktır.

## Kullanım
1. Veri Çekme (Scraping)
Projenizin bulunduğu klasörde yer alan bkm_kitap.py ve kitapsepeti.py gibi Python dosyalarını çalıştırın.
Bu dosyalar, komut satırında size süreci göstererek ilgili sitelerden verileri çekecektir.
Çekilen veriler, otomatik olarak aynı klasör içinde bkm_kitap_verileri.csv ve kitapsepeti_edebiyat_verileri.csv gibi dosyalar olarak kaydedilecektir.
2. Veri Karşılaştırma (Uygulama)
karsilastirma.py dosyasını çalıştırarak masaüstü uygulamasını başlatın.
Uygulama açıldığında, "Dosyaları Yükle" butonuna tıklayarak az önce çektiğiniz .csv dosyalarını seçin.
Uygulamanın arayüzünde bulunan arama kutusuna bir kitap adı yazın ve "Karşılaştır" butonuna basarak fiyat ve diğer bilgilerini farklı sitelerde karşılaştırın.

"Aynı Başlıklı Kitapları Bul" butonuna tıklayarak, farklı sitelerde bulunan aynı isimli kitapları listeleyebilirsiniz.
