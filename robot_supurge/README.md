# Robot Süpürge Ajanı

Yapay Zekâya Giriş dersi Dönem İçi Proje 1. Bu projede algı, eylem ve ajan türleri arasındaki ilişki, çalışan bir program üzerinde incelenir.

## Proje Hakkında

Ortam, yan yana duran A ve B adlı iki odadan oluşur. Her oda temiz ya da kirli olabilir. Robot süpürge, bu odalarda dolaşan ve kirli odaları temizleyen bir basit refleks ajandır. Ajanın başlangıç odası ve odaların başlangıç durumları programın her çalışmasında rastgele belirlenir.

Ajan kararını yalnızca bulunduğu odaya ve o odanın temiz ya da kirli olmasına bakarak verir. Geçmiş algıları karar vermek için kullanmaz. Eylemleri temizle, sağa git ve sola git olarak üçtür. Oda kirliyse ajan önce temizler, sonraki adımda oda temiz olduğu için diğer odaya geçer. Temizleme ve hareket ayrı eylemlerdir.

| Güncel algı | Seçilen eylem |
|---|---|
| A odası, kirli | Temizle |
| A odası, temiz | Sağa git |
| B odası, kirli | Temizle |
| B odası, temiz | Sola git |

Temiz odalar, bir zamanlayıcı aracılığıyla çalışma sırasında rastgele yeniden kirlenir. İki oda da temiz olduğunda program sonlanmaz, ajan odalar arasında dolaşmaya devam eder. Program kullanıcı durdurana kadar çalışır.

## Algı ve Eylem Günlüğü

Her adım ekrandaki günlük alanına yazılır. Kayıt, adım numarasını, geçen süreyi, ajanın bulunduğu odayı, algılanan durumu ve gerçekleştirilen eylemi içerir. Zamanlayıcı bir odayı kirlettiğinde bu da günlüğe eklenir.

```
Adım 6 | Süre: 4.0 sn | Oda: A | Algı: Kirli | Eylem: Temizle
[Zamanlayıcı] A odası kirlendi
```

## Çalıştırma

Program Python ile yazılmıştır ve grafik arayüz için standart kütüphanedeki tkinter'ı kullanır. Ek paket kurmak gerekmez.

```
python robot_supurge.py
```

Açılan pencerede **Başlat** butonuna basınca simülasyon başlar. Simülasyon **Durdur** butonuyla ya da klavyeden **Esc** tuşuyla durdurulur. Pencerede odaların durumu (temiz: yeşil, kirli: kahverengi), robotun konumu ve günlük görünür.

## Dosyalar

`robot_supurge.py`: programın tüm kaynak kodu.
