#  Python ile Raspberry Pi 3 Kontrollu Akıllı Ev Sistemi 

Bu proje Cisco Networking Academy NETACAD - MEB Öğretmen Yetiştirme Genel Müdürlüğü İşbirliği ile gerçekleştirilmiş olan PYTHON EĞİTİCİ EĞİTİMİ (2020000497) kursu eğitimleri kapsamında Robokod_Python Takımı tarafından geliştirilmiştir.

Projenin amacı Python dili, mikrodenetleyiciler, akıllı ev sistemleri derslerine giren öğretmenlerin, sınıf içinde kullabilecekleri ve öğrencilerin  yaparak öğrenebilecekleri bir eğitim materyeli geliştirmektir. 
Ayrıca meslek liselerinde Elektrik-Elektronik, Bilişim Teknolojileri Alanlarındaki ,Anadolu liselerinde robotik ve kodlamaya ilgili,  üniversite yüksek okul, lisans ve yüksek lisans öğrencilerinin faydalanması için geliştirilmiştir.

# Projede Kullanılan Donanımlar

* Raspberry Pi 3 - Raspbian İşletim Sistemi Kurulu
* Akıllı Ev Maketi
* Ultrasonik Sensör HC-SR04
* Servo Motor SG-90
* Buzzer (Aktif)
* 12 Volt Fan (Bilgisayar Kasalarından Çıkma- Geri Dönüşüm)
* HC-SR501 Ayarlanabilir IR Hareket Algılama Sensörü - Pir
* Tek Kanallı 5V Röle Modülü  (3Adet)
* 12V Şerit LED  50cm
* 12V Güç Kaynağı
* 5V Güç Kaynağı
* BreadBoard
* Dişi-Dişi , Dişi Erkek Jumper Kablo


# Proje Bağlantı Şeması
![](https://i.imgur.com/tHsIuyh.png)


Projede 12V ve 5V harici güç kaynakları kullanışmıştır. Bu sayede olasi bir kısa devre sonucu Raspberry Pi'nin zarar görmesi engellenmiştir. Bağlantılarda dikkat edilmesi gereken en önemli konu Raspberry'nin , 5V  güç kaynaklarının GND (Negatif) uçlarının birbirlerine bağlanarak tek devre olarak çalışmalarını sağlamaktır. 12V Güç kaynağı röle kontaklarına bağlı olduğu için ortak GND olmasına gerek yoktur.
> Devre şemasında Bahçe ve Oda LEDleri SMD Şerit Led olacaktır. Buradaki gösterim semboliktir. Ancak şekildeki  LED'lerde paralel bağlanarak çoğaltılabilir. LEDler ve Fan  Röle çıkışlarına NO( Normally Open) Normalde Açık ve Com - Common Ortak Uçlara bağlanmalıdır.

![](https://i.imgur.com/Vkh0kRv.png)
Kaynak :[https://www.raspberrypi.org/documentation/usage/gpio/](https://)

# Maket Ev Bağlantıları
![](https://i.imgur.com/fXfTy0B.jpg)

> Maket Ev için farklı tasarımlar kullanılabilir. Kullanılan tüm  ekipmanın görünebilmesi amacıyla bağlantılar gizlenmemiştir.


# Projede Kullanılan Yazılım Geliştirme Ortamı ve Kütüphaneler
* Python 3 
* Threading    "Aynı Anda birden çok rutinin çalışması için"
* Os           "Console komutlarının çalıştırılması için" 
* RPi.GPIO     "Raspberry'nin portlarının Giriş/Çıkış amaçlı kullanımı General Pursope Input Output"
* Time         "Zaman gecikmeleri eklemek amaçlı"
* Adafruit_DHT "DHT11 Sıcaklık ve Nem Sensörü Kütüphanesi"
* Flask        Web Tabanlı Kontrol Arayüzü Geliştirme amaçlı
* HTML-CSS  "Web tabanlı Mobil Uyumlu Arayüz Tasarımı amaçlı"

# Raspberry Pi 3'e Flask Kütüphanesinin Kurulması
FLASK kütüphanesi özellikle Python ile web sitesi tasarımı amacıyla kullanılmaktadır. 
Referans Site [https://flask.palletsprojects.com/en/1.1.x/](https://)

Raspberry de terminal penceresine
```
sudo apt-get update
```
yazarak tüm güncelleştirmeler yapılmalıdır. İşlem sonunda

```
sudo apt-get install python3-flask 
```
komutu ile flask kütüphanesi yüklenir.

# Adafruit_DHT Kütüphanesinin Kurulması
Terminal penceresinde 

```
pip3 install adafruit-circuitpython-dht

sudo apt-get install libgpiod2
```
Referans Sitesi [https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup](https://)
# Proje Python Komutları ve Kodların Görevleri
```
#!/usr/bin/python
import threading                            # Çoklu çalışma için kullanılan kütüphane
import os                                   # Console komutlarının çalıştırılması için eklenmiştir.
import RPi.GPIO as GPIO                     # Raspberry'nin portlarının giriş çıkış için kullanılması amacıyla eklenmiştir.
import time                                 # zaman gecikmeleri eklemek amacı ile kullanılmıştır.
import Adafruit_DHT    #DHT11 
from flask import Flask, render_template, request    # Web Tabanlı Kontrol Arayüzü işlemleri için eklenmiştir.
                                            # render_template ile kendi oluşturduğumuz html sayfası kullanılabilecektir.
app = Flask(__name__)                       # Flask tipi nesnesi oluşturma

GPIO.setmode(GPIO.BCM)                      # Pinleri Broadcom SOC channel standardına göre belirle
GPIO.setwarnings(False)                     # Uyarı mesajlarını gösterme


class PinTanimla:                           # sensörlerin ve aktuatorlerin pin numaralalarını ve aynı portların giriş çıkış için ayarlanmaları için kullanılmıştır.
    def __init__ (self,pinNo,giris_cikis):  # pinTanımla class yapıcısı
        self.pin=pinNo
        if (giris_cikis==1):                # yapıcıda ikinci değer 1 verilirse pin giriş olarak ayarlansın
            GPIO.setup(pinNo,GPIO.IN)
        else:
            GPIO.setup(pinNo,GPIO.OUT)      # ikinci değer 0 olarak verilecek ve pin çıkış olacaktır.


trig=PinTanimla(3,0)                        # Ultrasonik sensörün Trig pini 3 nolu port ve  0 = çıkış olarak ayarlandı.
echo=PinTanimla(2,1)                        # Ultrasonik sensör Echo pini 2 nolu port ve 1= giriş olarak ayarlandı. 
hirsizBuzzer=PinTanimla(0,0)                # Hırsız alarmı için kullanılan Buzzer 0 nolu pine çıkış olarak ayarlandı.
servoMotor=PinTanimla(17,0)                 # Kapı girişinde kullanılan sg90 servo motor pini
hirsizPirKontrol=PinTanimla(1,0)            # Hırsız alarmını olarak kullanılan PIR sensöründen çalıştırılması için kullanılan port
hirsizPir=PinTanimla(16,1)                  # Hırsız alarmı için kullanılan PIR sensöründen gelen veri için kullanıldı.
havalandirma=PinTanimla(12,0)               # Havalandırma fanı için kullanıldı
odaAydinlatma=PinTanimla(21,0);             #oda aydınlatması kontrolu için kullanıldı.
bahceAydinlatma=PinTanimla(20,0);           #bahçe aydınlatması kontrolu için kullanıldı.
DHTPin = 24                                 # DHTPin veri girişi için kullanıldı

sicak=23                                    # sicaklik 23 derece goster
garajKapiDurum=0                            # garaj kapısının durumunu kontrol etmek için kullanıldı.

sensor = Adafruit_DHT.DHT11                 # DHT11 sensörüne uyumlu nesne oluştur.
servo = GPIO.PWM(servoMotor.pin, 50)        # 50 Hertzlik PWM sinyal üret
servo.start(0)                              # baslangic degeri 0 derece yap


# Ultrasonik Sensör Veri Okuma

def ultra():
    while True:                             # While Döngüsünün Sürekli Devam Etmesi
        global garajKapiDurum               #Garaj kapısı durumunu saklayan global değişken
        GPIO.output(trig.pin, False)        #Trig pin kapatılır
        #print ("Olculuyor...")
        time.sleep(1)                       # 1 Saniye bekle
        GPIO.output(trig.pin, True)         #Trig Pin'e 5V gönder
        time.sleep(0.00001)                 # 10 mikrosaniye bekle
        GPIO.output(trig.pin, False)        # Trig Pin'e 0V ver ve kapat
        while GPIO.input(echo.pin)==0:      # Echo pin sinyalin gidip geldiği süreyi ölçer.
            pulse_basla = time.time()
        while GPIO.input(echo.pin)==1:      # echo pin'nin 0 dan 1 e geçme süresi sinyalin
                                            # ses hızında gidip gelme süresidir 
            pulse_bitis = time.time()
        pulse_sure = pulse_basla - pulse_bitis  #iki süre arasında fark alınarak süre bulunur

        #------------------------------------------------------------------------
        # ancak bu süre gidip gelme süresidir ve ikiye bölünmesi gerekir        -
        # mesafe = (sure x hız)/ 2     ses hızı  34300 cm/saniyedir bu nedenle  - 
        # mesafe = ( sure x 34300 ) / 2  ==>  sure * 17150 formulu elde edilir. -
        #------------------------------------------------------------------------
        
        mesafe = pulse_sure * 17150    
        mesafe = round(mesafe, 2)           # mesafe ondalık olarak iki basamaklıya çevrilir.
        if mesafe > 2 and mesafe < 50:      # mesafe 2 cm ile 50 cm arasında ise ölçüm yapılır 
            if mesafe>5 and mesafe<10:      # mesafe 5 cm ile 10 arasında ise kapıyı aç  
                garajKapiKontrol("acik")    # garajkapıkontrol fonksiyonunu çalıştır.
                garajKapiDurum=1
                time.sleep(2)
            else:
                garajKapiKontrol("kapali")
                garajKapiDurum=0
            print ("Mesafe:",mesafe,"cm")
        else:
            print ("Menzil asildi")         # Sensörün ölçüm sınırı dışına çıkıldığını gösterir.

def sicaklik():                             # sıcaklık ve havalandırma kontrol fonksiyonu
    while True:                             # sonsuz döngü oluştur.
        global havalandirma                 # havalandırma değişkenini global yap, aksi durumda local değişken olacağından diğer fonksiyonlara kullanılamaz.
        humidity, temperature = Adafruit_DHT.read_retry(sensor, DHTPin) # nem ve sıcaklık değerlerini humidity, temperature deişkenlerine ata
        if humidity is not None and temperature is not None:  #sıcaklık değişkeni boş değil ise ölçüm değerini kullan
            global sicak                    # sicak değişkenini global yap
            if (temperature>22):            # sıcaklık 22 derece üzerinde ise havalandırma fanını çalıştır.
                GPIO.output(havalandirma.pin, True)    
            else:
                GPIO.output(havalandirma.pin, False)
            sicak=('{0:0.1f}'.format(temperature)) #temperature değişkenini ondalık kısmını 1 basamak olarak sıcak değişkenine ata
            print (sicak)     
        else:
            print('Sıcaklık ve Nem Değeri Ölçülemedi')

def alarm():   # Hırsız alarm fonksiyonu
    
    while True: # sonsuz döngü oluştur
        if (GPIO.input(hirsizPir.pin)==1):          #PIR sensöründen 5V geldiğinde aktif olsun
             GPIO.output(hirsizBuzzer.pin,True)     # Buzzer  0.25 Saniye açık
             print("buzzer acik")
             time.sleep(0.25)  
             GPIO.output(hirsizBuzzer.pin,False)    # Buzzer  0.25 Saniye kapalı
             print("buzzer kapalı")
             time.sleep(0.25)
        else:
            GPIO.output(hirsizBuzzer.pin,False)     # PIR hareket algılamadığında Buzzer  kapalı

def aciyaCevir(aci):                                # Açıyı duty değerine çevirir
    return (float(aci) / 12.5 + 2)                  # %12.5 lik PWM sinyali 180 derece , 2 ise 0 dereceye eşittir.


def garajKapiKontrol(durum):                        # Garaj kapı Kontrol Fonksiyonu
    if (durum=="acik"): 
        GPIO.output(servoMotor.pin, True)           # Servo Motor Pinini Aktif Duruma getir
        servo.ChangeDutyCycle(aciyaCevir(60))       # Servo Motorun acısını 60 derece yap  
    else:
        servo.ChangeDutyCycle(aciyaCevir(10))        # Servo Motoru 10 derece yap
        GPIO.output(servoMotor.pin, False)          # Servo Motor Pinini Pasif duruma  getir

# Raspberry'nin pinlerinin değerleri proje açısından önemlidir. Bu değerlere göre
# web arayüzündeki bilgilendirmeler yada butonların durumları değiştirilmektedir.

def portlariKontrolEt():                            # Raspberry Pinlerini okuyarak dictionary oluşturma fonksiyonu
    global garajKapiDurum
    global    sicak
    if (GPIO.input(odaAydinlatma.pin)==1):          #Oda aydınlatma pin 1 ise arayüzdeki aydınlatma ON butonutu yeşil yapan class aktif olsun
        odaAcik = "clsAcik"
        odaKapali="clsNormal"                       # OFF yazan butonu gri yapan Class aktif et.
    else:
        odaKapali="clsKapali"  
        odaAcik= "clsNormal"
        
    if (GPIO.input(bahceAydinlatma.pin)==1):
        bahceAcik = "clsAcik"
        bahceKapali="clsNormal"
    else:
        bahceKapali="clsKapali"
        bahceAcik= "clsNormal"
        
    if (GPIO.input(havalandirma.pin)==1):           # Havalandırma pini 1 ise web arayüzünde havalandırma açık yaz
        havalandirmaDurum = "Açık"     
    else:
        havalandirmaDurum = "Kapalı"                # Havalandırma pini 1 ise web arayüzünde havalandırma kapalı yaz
        
    if (GPIO.input(hirsizPir.pin)==1):              # HırsızPir pini 1 ise web arayüzde hareket algılandı yaz 
        hirsiz = "Hareket Algılandı !"  
    else:
        hirsiz = "Hareket Algılanmıyor."            # HırsızPir pini 1 ise web arayüzde hareket algılanmıyor yaz   
    
    if (garajKapiDurum == 1):                       # garajKapiDurum pini 1 ise web arayüzde garaj kapısı açık yaz
        garaj = "Garaj Kapısı Açık"
        
    else:
        garaj="Garaj Kapısı Kapalı"                 # garajKapiDurum pini 0 ise web arayüzde garaj kapısı kapalı yaz
        
        
    if (GPIO.input(hirsizPirKontrol.pin)==1):       # hirsizPirKontrol pini 1 ise PIR dedektörünü çalıştır
        hirsizAcik = "clsAcik"
        hirsizKapali="clsNormal"
    else:                                           # hirsizPirKontrol pini 0 ise PIR dedektörünü kapat
        hirsizKapali="clsKapali"
        hirsizAcik= "clsNormal"
        
   # Yukarıdaki kontrolller ile elde edilen tüm veriler bir dictionery kutuphane nesnesine aktarıldı 

    datalar = {
    'sicaklik' : sicak,
    'havalandirmaDurum' : havalandirmaDurum,
    'hirsiz' : hirsiz,
    'odaAcik':odaAcik,
    'odaKapali':odaKapali,
    'bahceAcik':bahceAcik,
    'bahceKapali':bahceKapali,
    'garaj':garaj,
    'kapidurum':garajKapiDurum,
    'hirsizAcik':hirsizAcik,
    'hirsizKapali':hirsizKapali
    
    }
    return datalar   
  

@app.route('/')                             # app flask nesnesi ile web arayüzü ana sayfasını oluşturma
def index():                                # ilk sayfa olarak belirlenen index fonksiyonunu
    veriler=portlariKontrolEt()             # portların kontrolü ile elde edilen datalar veriler adında bir kütüphane nesnesine atanır.
    return render_template('index.html', **veriler)     # index.html sayfasına veriler nesnesini gönder.


@app.route('/<cihaz>-<durum>')              # Web arayüzünden oluşturulan linklerde değişkenleri cihaz ve durum nesneleri olarak belirle    
def do(cihaz, gorev):
    global garajKapiDurum
    global sicak
    if cihaz == "bahce":                    # Eğer cihaz bahçe ise gorev e bahceaydinlatma nin pin değerini ata
        gorev = bahceAydinlatma.pin         
    if cihaz == "hirsizalarmkontrol":       # Eğer cihaz hirsizalarmkontrol ise gorev e hirsizPirKontrol nin pin değerini ata
        gorev = hirsizPirKontrol.pin        
    if cihaz == "oda":                      # Eğer cihaz oda ise gorev e odaAydinlatma nın pin değerini ata
        gorev = odaAydinlatma.pin           
    if cihaz == "garaj":                    # Eğer cihaz garaj ise
       if durum=="acik":                    # durum değeri açıksa garaj kapısı açıldı anlamında garajKapiDurum=1 yap
           garajKapiDurum=1
       if durum=="kapali":                  # durum kapali ise garajkapıdurumu nu 0 yap
           garajKapiDurum=0 
    if durum == "acik" and cihaz != "garaj":    # cihazın garaj olmadığı ve durumun açık olduğunda
        GPIO.output(gorev, GPIO.HIGH)           # gorev değişkenine atanan pin değerini aktif yap. Bu pine bağlı olan röleyi çalıştırır.
    if durum == "kapali" and cihaz != "garaj":
        GPIO.output(gorev, GPIO.LOW)            # gorev değişkenine atanan pin değerini pasif yap. Bu pine bağlı olan röleyi kapatır.
        
    veriler=portlariKontrolEt()                 # Bütün portları yine oku ve değeleri veriler adındaki kütüphane nesnesine ata.

    return render_template('index.html', **veriler) # index.html sayfasına verileri gönder.

#------------------------------------------------------------------------------------------------------
# thread nesneleri sıcaklik, ultra ve alarm adındaki fonksiyonlarının birbirinden bağımsız çalışmasını-     -
# sağlar. Bu fonksiyonlardaki sonsuz döngüler birbirini durdurmadan sürekli çalışabilmektedir.        -
#------------------------------------------------------------------------------------------------------

thread1 = threading.Thread(target=sicaklik)     # sicaklik fonksiyonunu hedef olarak seç
thread1.start()                                 # thread i başlat 

thread2 = threading.Thread(target=ultra)        # ultra fonksiyonunu hedef olarak seç
thread2.start()                                 # thread i başlat

thread3 = threading.Thread(target=alarm)        # ultra fonksiyonunu alarm olarak seç
thread3.start()                                 # thread i başlat

os.system("fuser -n tcp -k 5000")               # tcp protokolünde 5000 nolu Portu  kapatma colsole komutu

# fuser linux komutudur ve verilen komutta
# -n tcp  tcp protokolunu seç
# -k = kill sonlandır
# 5000 websunucu için seçilen port no

if __name__ == "__main__":
    
    app.run(host = '0.0.0.0', debug=True,port=5000)     # app isimli flask nesnesini çalıştır.

    # host = '0.0.0.0' bu ifade ile web sunucuna ağdaki tüm  cihazlar ulaşabilsin .
    # debug= True programda oluşan hatalar web sayfası üzerinden görüntülenebilir.
    # web sunucusunu için 127.0.0.1:5000 nolu portta aç 
          
```

# Proje HTML Arayüz Kodları
```
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Akıllı Ev Sistemi</title>
<meta http-equiv="refresh" content="2">
<link href="static/stil.css" type="text/css" rel="stylesheet" >
</head>

<body>
<div class="container">
  <div class="banner">
  
    <h2>Akıllı Ev Sistemi Kontrol Uygulaması</h2>

<br>
<br>
<br>
<br>
<br>
<br>
<br>
  </div>
  <div class="col-4 floatleft databox mavibg1 padsag beyazyazi">Ortam Sıcaklığı : </div>  
  <!--  {{sicaklik}} ifadesi python üzerinden gönderilmektedir.  -->
  <div class="col-8 floatleft databox saribg mleft1">{{sicaklik}}<sup>o</sup>C</div> 
	
  <div class="col-4 floatleft databox mavibg1 padsag beyazyazi">Havalandırma : </div>
<!--  {{havalandirmaDurum}} ifadesi python üzerinden gönderilmektedir.  -->	
  <div class="col-8 floatleft databox saribg mleft1">{{havalandirmaDurum}}</div>
  <div class="col-4 floatleft databox mavibg1 padsag beyazyazi">Hırsız Alarmı : </div>
<!--  {{hirsiz}} ifadesi python üzerinden gönderilmektedir.  -->	
  <div class="col-8 floatleft databox saribg mleft1">{{hirsiz}}</div>
  <div class="col-4 floatleft databox mavibg1 padsag beyazyazi">Garaj Kapısı: </div>
<!--  {{garaj}} ifadesi python üzerinden gönderilmektedir.  -->	
  <div class="col-8 floatleft databox saribg mleft1">{{garaj}}</div>
  
<!--  {{hirsizAcik}} ifadesi python üzerinden gönderilmektedir.  -->		
    <a class="{{hirsizAcik}}" href="/hirsizalarmkontrol-acik"> <div class="col-2 floatleft mright1 {{hirsizAcik}}">ON</div>  </a>
  <div class="col-8 floatleft databox mavibg2"> Hırsız Alarmı Kontrolü</div> 
<!--  {{hirsizKapali}} ifadesi python üzerinden gönderilmektedir.  -->	
  <a class="{{hirsizKapali}}" href="/hirsizalarmkontrol-kapali"> <div class="col-2 floatleft mleft1 {{hirsizKapali}}">OFF</div>  </a> 
  <!--  {{bahceAcik}} ifadesi python üzerinden gönderilmektedir.  -->	

  <a class="{{bahceAcik}}" href="/bahce-acik"> <div class="col-2 floatleft mright1 {{bahceAcik}}">ON</div>  </a>
  <div class="col-8 floatleft databox mavibg2"> Bahçe Aydınlatması</div>
	 <!--  {{bahceKapali}} ifadesi python üzerinden gönderilmektedir.  -->	
  <a class="{{bahceKapali}}" href="/bahce-kapali"> <div class="col-2 floatleft mleft1 {{bahceKapali}}">OFF</div>  </a> 
  <!--  {{odaAcik}} ifadesi python üzerinden gönderilmektedir.  -->  
  <a class="{{odaAcik}}" href="/oda-acik"> <div class="col-2 floatleft mright1 {{odaAcik}}">ON</div>  </a>
  <div class="col-8 floatleft databox mavibg2"> Oda Aydınlatması</div>
	<!--  {{odaKapali}} ifadesi python üzerinden gönderilmektedir.  -->
  <a class="{{odaKapali}}" href="/oda-kapali">  <div class="col-2 floatleft mleft1 {{odaKapali}}">OFF</div>  </a> 
    
    
    
    <div class="col-12 floatleft footer beyazyazi">&copy; RobokodPython Grubu - 2020</div> 
</div>
</body>
</html>

```
# Web Arayüzü CSS kodları

```
@charset "utf-8";
/* CSS Document */
body {
  transition: 0.7s;
  /* background-color: #262626;*/
}
html {
  font-family: Segoe, "Segoe UI", "DejaVu Sans", "Trebuchet MS", Verdana, "sans-serif";
  font-size: 18px;
  font-weight: bold;
}
a {
  text-decoration: none;
}
.banner {
  position: relative;
  width: 100%;
}
h2 {
  position: absolute;
  background-color: rgba(192, 192, 192, 0.7);
  width: 50%;
  padding: 2%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #fff;
  text-shadow: 2px 2px 8px #000;
}
.col-2 {
  width: 16.00%;
}
.col-4 {
  width: 33.00%;
}
.col-8 {
  width: 66.00%;
}
.col-12 {
  width: 100%;
}
.floatleft {
  float: left;
}
.container {
  max-width: 80%;
  margin: auto;
  height: auto;
  background-color: #FFFFFF;
}
.clsAcik {
  height: 80px;
  background-color: #7BF559;
  border-radius: 20px;
  text-align: center;
  line-height: 80px;
  color: #ffffff;
  margin-top: 15px;
  box-shadow: 0 6px 6px -1px #262626;
  transition: 0.6s;
}
.clsKapali {
  height: 80px;
  background-color: #F52E0A;
  border-radius: 20px;
  text-align: center;
  line-height: 80px;
  color: #ffffff;
  font-size: 20px;
  margin-top: 15px;
  box-shadow: 0 6px 6px -1px #262626;
  transition: 0.6s;
}
.clsNormal {
  height: 80px;
  background-color: #DAD9D8;
  border-radius: 20px;
  text-align: center;
  line-height: 80px;
  color: #000;
  font-size: 20px;
  margin-top: 15px;
  text-shadow: 3px 3px 8px #fff;
  box-shadow: 0 6px 6px -1px #262626;
  transition: 0.6s;
}
.clsNormal:hover, .clsKapali:hover, .clsAcik:hover {
  box-shadow: 0 0 10px 2px #F2E205, 0px 6px 6px 2px #000;
  transition: 0.4s;
}
.databox {
  margin-top: 15px;
  height: 80px;
  border-radius: 20px;
  text-align: center;
  line-height: 80px;
  box-shadow: 0 6px 6px -1px #262626;
  transition: 0.6s;
}
.mleft1 {
  margin-left: 1%;
}
.mright1 {
  margin-right: 1%;
}
.saribg {
  background-color: #F9E8D9;
}
.mavibg1 {
  background-color: #03588C;
}
.mavibg2 {
  background-color: #41C0F2;
}
.footer {
  margin: 20px 0px;
  height: 80px;
  background-color: #000;
  text-align: center;
  line-height: 80px;
}
.beyazyazi {
  color: white;
}
.padsag {
  text-align: right;
  padding-right: 1%;
  box-sizing: border-box;
}
@media only screen and (max-width: 960px) {
  /* For mobile phones: */
  .container {
    max-width: 85%;
  }
}
@media only screen and (max-width: 720px) {
  /* For mobile phones: */
  .container {
    max-width: 90%;
  }
  .clsAcik {
    border-radius: 100%;
    height: 60px;
    line-height: 60px;
  }
  .clsKapali {
    border-radius: 100%;
    height: 60px;
    line-height: 60px;
  }
  .clsNormal {
    border-radius: 100%;
    height: 60px;
    line-height: 60px;
  }
  .databox {
    border-radius: 50px;
    height: 60px;
    line-height: 60px;
  }
  h2 {
    font-size: 1em;
  }
}
@media only screen and (max-width: 540px) {
  /* For mobile phones: */
  .container {
    max-width: 100%;
  }
}
```

# Proje Dosyalarının Konumları
Raspberry'de Documents klasörü içine "proje" adında klasör oluşturunuz.
* Verilen python kodlarını akilliev.py adıyla proje klasörüne kaydediniz.
* proje  klasörü içine templates adında klasör oluşturunuz.
* HTML kodlarını index.html adı ile templates klasörüne kaydediniz.
* proje klasörüne static adında klasör oluşurunuz.
* CSS kodlarını stil.css adı ile static klasörüne kaydediniz.

templates ve static klasörleri FLASK kütüphanesi tarafından özel olarak kullanılan isimlerdir. Değişiklik yapılmamalıdır.
templates klasörüne python tarafından veri gönderilen yada veri çekilen sayfalar kaydedilmelidir. render_templates komutu ile bu sayfalar otomatik olarak templates klasörü içinden çağırılmaktadır. static klasöründe ise değişmeyen dosyalar, resimler bulunmaktadır. Projede bu klasörde stil.css dosyası değişmeyecek, python tarafından işleme sokulmayacak olan dosyadır.
 
Dosya ve klasörlerin konumları aşağıdaki gibi olmalıdır.

![](https://i.imgur.com/aH9rk26.png)

# Proje Web Arayüzü Görünümü
![](https://i.imgur.com/eRrEqW4.png)

Arayüz HTML ve CSS sayfaları ile hazırlanmıştır ve mobil uyumludur. Ortam sıcaklığı, havalandırma fanı, hırsız alarmı ve garaj kapısının durumuları gösterilmektedir. Hırsız alarmının çalıştırılması , oda ve bahçe aydınlatmlarının açılıp kapatılması sağlanabilmektedir. HTML sayfası her 2  saniyede bir yenilenmektedir. Böylece sensör verileri ve aydınlatma ve fan durumları yenilenmektedir.  

# Projenin Çalıştırılması
Raspberry Pi'de Raspbian işletim sistemi üzerinde Python editörü IDLE bulunmaktadır. IDLE'i çalıştırmak için sol üst köşedeki Raspberry ikonu tıklanarak programming menüsü altından
Python 3 seçilmelidir.
![](https://i.imgur.com/bwOPL2L.png)

Raspberry'de  Python IDLE ile akilliev.py dosyası açılarak F5 tuşuna basılarak proje çalıştırılabilir.

Ardından Chronium web tarayıcısı açılarak adres çubuğuna 
127.0.0.1:5000 adresi yazılarak çalıştırılmalıdır.

Proje arayüzünü  Raspberry Pi ile aynı ağdaki bir cihaz üzerinden de kontrol etmek mümkündür. 
Örneğin Raspberry IP adresi 192.168.1.48 ise , Chronium tarayıcısında
192.168.1.48:5000 yazılarak arayüz e ulaşılabilir ve raspberry 
kontrol edilebilir. 5000 nolu port Raspberry üzerinde bulunan kullanımda olmayan programcı tarafından seçilen bir porttur. Örneğin 80 nolu HTTP  portu seçilirse hata oluşur.  



