#Robot Süpürge Ajanı - Dönem İçi Proje 1
# Çalıştırmak için: python robot_supurge.py
# Ek paket gerekmiyor, tkinter Python ile birlikte geliyor.
# Durdurmak için: "Durdur" butonu ya da klavyeden Esc tuşu.

import random
import time
import tkinter as tk

ADIM_SURESI = 800 #ajan 0.8 sn de bir adım atıyor
KIRLENME_SURESI = 3000 # 3 sn de bir temiz odalar kirlenebiliyor

# ortam: iki oda var, başlangıç duvrumları rastgele
odalar = {"A" : random.choice(["Temiz", "Kirli"]),
          "B" : random.choice(["Temiz", "Kirli"])}
ajan_odasi = random.choice(["A", "B"]) # ajan rastgele bir odada başlıyor

adim_sayisi = 0
calisiyor = False
baslangic_zamani = 0
adim_job = None #after() ile kurulan işleri iptal edebilmek için tutuyorum
kirlenme_job = None

def algila():
    #ajan sadece bulunduğu odayı ve o oadanın durumunu görüyor
    return ajan_odasi, odalar[ajan_odasi]

def karar_ver(oda, durum):
    #basit refleks ajan: karar sadece şu anki algıya bağlı, geçmişe bakmıyor
    # A kirli -> temizle
    # A temiz -> sağa git
    # B kirli -> temizle
    # B temiz -> sola git
    if durum == "Kirli":
        return "Temizle"
    if oda == "A":
        return "Sağa git"
    return "Sola git"

def eylemi_uygula(eylem):
    global ajan_odasi
    if eylem == "Temizle":
        odalar[ajan_odasi] = "Temiz"
    elif eylem == "Sağa git":
        ajan_odasi = "B"
    elif eylem == "Sola git":
        ajan_odasi = "A"

def ciz():
    #tkinter ile ortamı çizdiriyorum
    canvas.delete("all")
    x = 20
    for oda in ["A", "B"]:
        if odalar[oda] == "Kirli":
            renk = "brown"
        else:
            renk = "green"
        canvas.create_rectangle(x, 20, x + 200, 160, fill=renk, outline="black")
        canvas.create_text(x + 100, 35, text="Oda " + oda + " - " + odalar[oda])
        if ajan_odasi == oda:
            canvas.create_oval(x + 70, 70, x + 130, 130, fill="blue")
            canvas.create_text(x + 100, 100, text="Robot", fill="white")
        x = x + 220

def log_yaz(satir):
    gunluk.config(state="normal")
    gunluk.insert("end", satir + "\n")
    gunluk.see("end")
    gunluk.config(state="disabled")

def adim_at():
    global adim_sayisi, adim_job
    if not calisiyor:
        return
    oda, durum = algila()
    eylem = karar_ver(oda, durum)
    adim_sayisi += 1
    gecen = time.time() - baslangic_zamani
    log_yaz("Adım %d | Süre: %.1f sn | Oda: %s | Algı: %s | Eylem: %s"
            % (adim_sayisi, gecen, oda, durum, eylem))
    eylemi_uygula(eylem)
    ciz()
    adim_job = pencere.after(ADIM_SURESI, adim_at)

def kirlet():
    #zamanlayıcı : temiz odalar bazen tekrar kirleniyor
    global kirlenme_job
    if not calisiyor:
        return
    for oda in odalar:
        if odalar[oda] == "Temiz" and random.random() < 0.3:
            odalar[oda] = "Kirli"
            log_yaz("[Zamanlayıcı] " + oda + " odası kirlendi")
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


if __name__ == "__main__":
    pencere = tk.Tk()
    pencere.title("Robot Süpürge")

    canvas = tk.Canvas(pencere, width=460, height=180)
    canvas.pack()

    tk.Button(pencere, text="Başlat", command=baslat).pack(side="left", padx=10)
    tk.Button(pencere, text="Durdur", command=durdur).pack(side="left")

    gunluk = tk.Text(pencere, height=15, width=70, state="disabled")
    gunluk.pack(side="bottom", padx=10, pady=10)

    pencere.bind("<Escape>", durdur)
    ciz()
    pencere.mainloop()