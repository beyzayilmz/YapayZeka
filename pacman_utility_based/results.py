# iki oyuncunun sonuçlarını karşılaştırma
# sıralama: 1) oyunu tamamlama durumu 2) toplam puan 3) eşitse daha kısa süre
# hepsi eşitse beraberlik


def make_result(name, game, elapsed):
    # süreyi ekranda gösterdiğimiz gibi 0.1 saniyeye yuvarlıyoruz,
    # yoksa ekranda aynı görünen iki süre farklı sayılabilirdi
    return {
        "name": name,
        "completed": game.completed,
        "score": game.score,
        "time": round(elapsed, 1),
        "steps": game.steps,
        "food_left": game.food_left(),
    }


def find_winner(a, b):
    # kazananın sonucunu döndürür, beraberlikte None
    # ikinci değer hangi ölçütle kazanıldığı
    if a["completed"] != b["completed"]:
        if a["completed"]:
            return a, "oyunu tamamladı"
        return b, "oyunu tamamladı"
    if a["score"] != b["score"]:
        if a["score"] > b["score"]:
            return a, "daha yüksek puan"
        return b, "daha yüksek puan"
    if a["time"] != b["time"]:
        if a["time"] < b["time"]:
            return a, "daha kısa süre"
        return b, "daha kısa süre"
    return None, "tüm ölçütler eşit"
