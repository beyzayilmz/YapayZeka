# Pacman: Utility-Based Rational Agent

Yapay Zekâya Giriş dersi, Pacman projesi. Grafik arayüzlü bir Pacman oyunu ile bu oyunu kendi başına oynayan, fayda (utility) tabanlı bir rasyonel ajan içerir. Amaç, tüm yemekleri kısa sürede ve olabildiğince yüksek puanla toplamaktır. Proje kılavuzu `docs/Pacman_Proje_Kilavuzu.pdf` dosyasındadır.

## Oyun

İnsan ve AI aynı haritada, ayrı ayrı ve sırayla oynar. Menüde seviye ve önce kimin oynayacağı seçilir. İkinci oyuncu için oyun sıfırlanır: harita, başlangıç konumları, yemekler, enerji topları, ayarlar ve hayaletlerin rastgele sayı üreticisinin tohumu (seed) aynıdır. Her tur başlamadan önce 3 saniyelik geri sayım yapılır, süre geri sayım bittikten sonra işlemeye başlar. İnsan ve AI aynı hızda hareket eder (her 150 ms'de bir hamle).

Ekranda harita, Pacman, hayaletler, güncel puan, süre, kalan yemek sayısı ve (etkinse) kalan enerji süresi gösterilir.

**Kurallar**

- Hareketler yalnızca sağ, sol, yukarı ve aşağıdır. Duvarlardan geçilemez.
- Enerji yokken hayalete çarpmak oyunu bitirir (game over). Hayaletle yer değiştirip yanından geçmek de çarpma sayılır.
- Enerji topu 20 hamle boyunca güç verir. Bu sürede hayaletler korkar ve rastgele kaçar. Yakalanan hayalet ek puan kazandırır ve başlangıç noktasına döner.
- Tüm yemekleri ve enerji toplarını toplamak seviyeyi tamamlar.

**Puanlama** (`settings.py`)

| Olay | Puan |
|---|---|
| Her hareket | -1 |
| Yemek | +10 |
| Enerji topu | +50 |
| Enerji etkinken hayalet yakalamak | +200 |

**Hayaletler**: Çift sıradaki hayaletler (%70 olasılıkla) BFS ile Pacman'e giden en kısa yolu izler, diğerleri rastgele gezer. Başlangıçta ve yakalandıktan sonra 5 hamle beklerler.

**Seviyeler**: Üç seviye vardır, her birinin haritası farklıdır ve engel düzeni giderek zorlaşır. Haritadaki tüm yemeklerin Pacman'in başlangıç noktasından erişilebilir olduğu oyun başlarken BFS ile kontrol edilir.

| Seviye | Duvar | Yemek | Enerji topu | Hayalet |
|---|---|---|---|---|
| 1 | 142 | 166 | 4 | 2 |
| 2 | 151 | 157 | 4 | 2 |
| 3 | 157 | 150 | 4 | 3 |

**Kazanan**: İki tur sonunda önce oyunu tamamlama durumuna, sonra toplam puana, eşitlikte daha kısa süreye bakılır. Tüm ölçütler eşitse beraberlik gösterilir. Sonuç ekranında iki oyuncunun durumu, puanı, süresi, hamle sayısı ve kalan yemeği ile kazanan yer alır.

## AI Ajanı

Ajan (`ai.py`) her hamlede geçerli yönlerin hepsini oyunun bir kopyasında dener. Kopyada hayaletler en kötü ihtimalle, yani hepsi Pacman'e doğru hareket ettirilir. Ajan iki hamle ileriye bakar ve ortaya çıkan durumları bir fayda fonksiyonuyla puanlayarak en yüksek faydalı yönü seçer. Fayda fonksiyonu şu bileşenlerden oluşur:

- **Oyun puanı**: yemek, enerji topu ve hayalet puanları ile her hareketin maliyeti.
- **Yemeğe uzaklık** ve **kalan yemek sayısı**: yemeklere ulaşmayı ödüllendirir.
- **Hayalet riski**: yakındaki hayaletler için uzaklığın karesiyle artan ceza.
- **Güvenli alan**: Pacman'in hayaletlerden önce ulaşabildiği hücre sayısı. Çıkmaz yerlere sıkışmayı önler.
- **Enerji etkisi**: enerji varken yetişilebilecek hayaletlere gitmek ödüllendirilir, enerji yokken hayalet yaklaşırsa enerji topuna gitmek ödüllendirilir.
- **Tekrar cezası** ve **sabır**: ileri geri gidip gelmeyi engeller, uzun süre yemek yiyemezse ajan daha fazla risk almaya başlar.

Formül, bileşenler ve ağırlıklar `ai.py` dosyasının başında yorum olarak açıklanmıştır.

## Çalıştırma

Python 3 ve pygame gerekir.

```
pip install -r requirements.txt
python main.py
```

**Tuşlar**

| Ekran | Tuş |
|---|---|
| Menü | `1` `2` `3` veya `←` `→`: seviye, `H` / `A`: önce İnsan / AI, `ENTER`: başla |
| Oyun (insan) | Ok tuşları veya `WASD` |
| Tur sonu | `ENTER`: sıradaki oyuncu / sonuçlar |
| Sonuçlar | `ENTER`: menüye dön |
| Her yerde | `ESC`: çıkış |

## Dosyalar

- `main.py`: giriş noktası, ekran akışı (menü, geri sayım, oyun, tur sonu, sonuçlar).
- `game.py`: oyun durumu ve kuralları (hareket, puan, enerji, çarpışma).
- `ai.py`: utility-based ajan ve fayda fonksiyonu.
- `ghosts.py`: hayalet stratejileri.
- `levels.py`: haritalar ve erişilebilirlik kontrolü.
- `results.py`: iki oyuncunun sonuçlarının karşılaştırılması ve kazananın belirlenmesi.
- `render.py`: çizim işlemleri.
- `settings.py`: puanlar, süreler, renkler ve diğer sabitler.
