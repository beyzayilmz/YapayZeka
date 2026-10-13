# Robot Süpürge Ajanı - Dönem İçi Proje 1
# Adım 2: çok odalı ortam (satır x sütun ızgara), basit refleks ajan

import random
import time
import tkinter as tk

ADIM_SURESI = 500        # ajan 0.5 sn de bir adım atıyor (ms)
KIRLENME_SURESI = 2000   # 2 sn de bir temiz odalar kirlenebiliyor (ms)
KIRLENME_ORANI = 0.1     # her temiz oda için kirlenme şansı
HUCRE = 50               # bir odanın ekrandaki boyutu (piksel)

# ortam
satir_sayisi = 3
sutun_sayisi = 3
odalar = []              # odalar[satir][sutun] = "Temiz" ya da "Kirli"
ajan_satir = 0
ajan_sutun = 0

adim_sayisi = 0
calisiyor = False
baslangic_zamani = 0
adim_job = None          # after() işlerini iptal edebilmek için tutuyorum
kirlenme_job = None


def ortami_kur():
    # ızgarayı rastgele doldur, ajanı rastgele bir odaya koy
    global odalar, ajan_satir, ajan_sutun, adim_sayisi
    odalar = []
    for i in range(satir_sayisi):
        sira = []
        for j in range(sutun_sayisi):
            sira.append(random.choice(["Temiz", "Kirli"]))
        odalar.append(sira)
    ajan_satir = random.randint(0, satir_sayisi - 1)
    ajan_sutun = random.randint(0, sutun_sayisi - 1)
    adim_sayisi = 0


def algila():
    # ajan sadece bulunduğu odayı (konum) ve o odanın durumunu görüyor
    return ajan_satir, ajan_sutun, odalar[ajan_satir][ajan_sutun]


def karar_ver(satir, sutun, durum):
    # basit refleks ajan: sadece şu anki algıya bakıyor, geçmişi kullanmıyor
    # oda kirliyse temizle, temizse gidebileceği yönlerden birini rastgele seç
    if durum == "Kirli":
        return "Temizle"

    yonler = []
    if satir > 0:
        yonler.append("Yukarı git")
    if satir < satir_sayisi - 1:
        yonler.append("Aşağı git")
    if sutun > 0:
        yonler.append("Sola git")
    if sutun < sutun_sayisi - 1:
        yonler.append("Sağa git")

    if len(yonler) == 0:      # 1x1 ortamda gidecek yer yok
        return "Bekle"
    return random.choice(yonler)


def eylemi_uygula(eylem):
    global ajan_satir, ajan_sutun
    if eylem == "Temizle":
        odalar[ajan_satir][ajan_sutun] = "Temiz"
    elif eylem == "Yukarı git":
        ajan_satir = ajan_satir - 1
    elif eylem == "Aşağı git":
        ajan_satir = ajan_satir + 1
    elif eylem == "Sola git":
        ajan_sutun = ajan_sutun - 1
    elif eylem == "Sağa git":
        ajan_sutun = ajan_sutun + 1


def ciz():
    canvas.delete("all")
    for i in range(satir_sayisi):
        for j in range(sutun_sayisi):
            x = 10 + j * HUCRE
            y = 10 + i * HUCRE
            if odalar[i][j] == "Kirli":
                renk = "brown"
            else:
                renk = "green"
            canvas.create_rectangle(x, y, x + HUCRE, y + HUCRE, fill=renk, outline="black")
            canvas.create_text(x + HUCRE / 2, y + 8, text=odalar[i][j], fill="white", font=("Arial", 8))
    # robot
    rx = 10 + ajan_sutun * HUCRE
    ry = 10 + ajan_satir * HUCRE
    canvas.create_oval(rx + 12, ry + 16, rx + HUCRE - 12, ry + HUCRE - 6, fill="blue")
    canvas.create_text(rx + HUCRE / 2, ry + HUCRE / 2 + 5, text="R", fill="white")


def log_yaz(satir):
    gunluk.config(state="normal")
    gunluk.insert("end", satir + "\n")
    gunluk.see("end")
    gunluk.config(state="disabled")


def adim_at():
    global adim_sayisi, adim_job
    if not calisiyor:
        return
    satir, sutun, durum = algila()
    eylem = karar_ver(satir, sutun, durum)
    adim_sayisi += 1
    gecen = time.time() - baslangic_zamani
    log_yaz("Adım %d | Süre: %.1f sn | Oda: (%d,%d) | Algı: %s | Eylem: %s"
            % (adim_sayisi, gecen, satir + 1, sutun + 1, durum, eylem))
    eylemi_uygula(eylem)
    ciz()
    adim_job = pencere.after(ADIM_SURESI, adim_at)


def kirlet():
    # zamanlayıcı: temiz odalar bazen tekrar kirleniyor
    global kirlenme_job
    if not calisiyor:
        return
    kirlenenler = []
    for i in range(satir_sayisi):
        for j in range(sutun_sayisi):
            if odalar[i][j] == "Temiz" and random.random() < KIRLENME_ORANI:
                odalar[i][j] = "Kirli"
                kirlenenler.append("(%d,%d)" % (i + 1, j + 1))
    if len(kirlenenler) > 0:
        log_yaz("[Zamanlayıcı] kirlenen odalar: " + " ".join(kirlenenler))
    ciz()
    kirlenme_job = pencere.after(KIRLENME_SURESI, kirlet)


def baslat():
    global calisiyor, baslangic_zamani
    if calisiyor:
        return
    calisiyor = True
    baslangic_zamani = time.time()
    log_yaz("--- Başladı ---")
    adim_at()
    kirlet()


def durdur(event=None):
    global calisiyor
    if not calisiyor:
        return
    calisiyor = False
    pencere.after_cancel(adim_job)
    pencere.after_cancel(kirlenme_job)
    log_yaz("--- Durduruldu ---")


def ortami_yeniden_kur():
    # "Ortamı Kur" butonu: kutulardaki satır ve sütun sayısıyla yeni ortam kurar
    global satir_sayisi, sutun_sayisi
    if calisiyor:
        log_yaz("Önce Durdur'a basın, sonra ortamı değiştirin.")
        return
    try:
        s = int(satir_kutusu.get())
        c = int(sutun_kutusu.get())
    except ValueError:
        log_yaz("Satır ve sütun için sayı girin.")
        return
    if s < 1 or s > 10 or c < 1 or c > 10:
        log_yaz("Satır ve sütun 1 ile 10 arasında olmalı.")
        return
    satir_sayisi = s
    sutun_sayisi = c
    ortami_kur()
    canvas.config(width=20 + sutun_sayisi * HUCRE, height=20 + satir_sayisi * HUCRE)
    ciz()
    log_yaz("--- Yeni ortam: %d x %d ---" % (satir_sayisi, sutun_sayisi))


def arayuzu_kur():
    global pencere, canvas, gunluk, satir_kutusu, sutun_kutusu
    pencere = tk.Tk()
    pencere.title("Robot Süpürge - Çok Odalı Ortam")

    ust = tk.Frame(pencere)
    ust.pack(pady=5)
    tk.Label(ust, text="Satır:").pack(side="left")
    satir_kutusu = tk.Entry(ust, width=4)
    satir_kutusu.insert(0, str(satir_sayisi))
    satir_kutusu.pack(side="left", padx=5)
    tk.Label(ust, text="Sütun:").pack(side="left")
    sutun_kutusu = tk.Entry(ust, width=4)
    sutun_kutusu.insert(0, str(sutun_sayisi))
    sutun_kutusu.pack(side="left", padx=5)
    tk.Button(ust, text="Ortamı Kur", command=ortami_yeniden_kur).pack(side="left", padx=5)

    canvas = tk.Canvas(pencere, width=20 + sutun_sayisi * HUCRE, height=20 + satir_sayisi * HUCRE)
    canvas.pack()

    alt = tk.Frame(pencere)
    alt.pack(pady=5)
    tk.Button(alt, text="Başlat", command=baslat).pack(side="left", padx=10)
    tk.Button(alt, text="Durdur", command=durdur).pack(side="left")

    gunluk = tk.Text(pencere, height=12, width=75, state="disabled")
    gunluk.pack(padx=10, pady=10)

    pencere.bind("<Escape>", durdur)


if __name__ == "__main__":
    ortami_kur()
    arayuzu_kur()
    ciz()
    pencere.mainloop()
