#!/usr/bin/python
import threading                            # Çoklu çalışma için kullanılan kütüphane
import os                                   # Console komutlarının çalıştırılması için eklenmiştir.
import RPi.GPIO as GPIO                     # Raspberry'nin portlarının giriş çıkış için kullanılması amacıyla eklenmiştir.
import time                                 # zaman gecikmeleri eklemek amacı ile kullanılmıştır.
import Adafruit_DHT    #DHT11 
from flask import Flask, render_template,request    # Web Tabanlı Kontrol Arayüzü işlemleri için eklenmiştir.
                                            # render_template ile kendi oluşturduğumuz html sayfası kullanılabilecektir.
app = Flask(__name__)                       # Flask tipi nesnesi oluşturma

GPIO.setmode(GPIO.BCM)                      # Pinleri GPIO standardına göre belirle
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
        if mesafe > 5 and mesafe < 20:      # mesafe 5 cm ile 20 cm arasında ise ölçüm yapılır 
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
        servo.ChangeDutyCycle(aciyaCevir(90))       # Servo Motorun acısını 90 derece yap  
    else:
        servo.ChangeDutyCycle(aciyaCevir(0))        # Servo Motoru 0 derece yap
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

    # host = '0.0.0.0' bu ifade ile web sunucu 127.0.0.1 ve cihazın IP si ile ulaşılabilir durumda olacaktır.
    # debug= True programda oluşan hatalar web sayfası üzerinden görüntülenebilir.
    # web sunucusunu için 127.0.0.1:5000 nolu portta aç 
       
 
    
