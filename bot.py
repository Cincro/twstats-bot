import requests
import time
from bs4 import BeautifulSoup

# ======================
# CONFIGURACIÓN
# ======================

URL = "https://es.twstats.com/es96/index.php?page=tribe&mode=conquers&id=30&type=gain&oldtribe=0"
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1460291286480326706/niksO5ztIDqFkIlDxk3pZCDKRHSOCOy3LCkwz91G9Uc-RMFIRndElP90mWaciMqSquLO"
CHECK_INTERVAL = 30

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TWStatsBot/1.0)"
}

vistos = set()

# ======================
# FUNCIÓN DISCORD
# ======================

def enviar_discord(mensaje):
    r = requests.post(WEBHOOK_URL, json={"content": mensaje})
    if r.status_code != 204:
        print("❌ ERROR enviando a Discord:", r.status_code, r.text)
    else:
        print("✅ Mensaje enviado a Discord")

# ======================
# BOT PRINCIPAL
# ======================

print("🤖 Bot iniciado correctamente")
enviar_discord("✅ Prueba: el bot está funcionando correctamente")


while True:
    try:
        r = requests.get(URL, headers=HEADERS, timeout=15)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        tabla = soup.find("table")

        if not tabla:
            print("⚠️ No se encontró la tabla")
            time.sleep(CHECK_INTERVAL)
            continue

        filas = tabla.find_all("tr")[1:]

        for fila in filas[:5]:
            columnas = fila.find_all("td")
            if len(columnas) < 4:
                continue

            pueblo = columnas[0].get_text(strip=True)

            nuevo_jugador = columnas[1].find_all("a")[0].get_text(strip=True)
            nueva_tribu = columnas[1].find_all("a")[1].get_text(strip=True)

            antiguo_jugador = columnas[2].find_all("a")[0].get_text(strip=True)
            antigua_tribu = columnas[2].find_all("a")[1].get_text(strip=True)

            hora = columnas[3].get_text(strip=True)

            id_conquista = f"{pueblo}|{nuevo_jugador}|{antiguo_jugador}|{hora}"

            if id_conquista not in vistos:
                if vistos:
                    enviar_discord(
                        "🏰 **NUEVA CONQUISTA DETECTADA**\n\n"
                        f"🏘️ **Pueblo:** {pueblo}\n\n"
                        f"🟢 **Nuevo dueño:** {nuevo_jugador}\n"
                        f"🟢 **Tribu nueva:** {nueva_tribu}\n\n"
                        f"🔴 **Antiguo dueño:** {antiguo_jugador}\n"
                        f"🔴 **Tribu antigua:** {antigua_tribu}\n\n"
                        f"⏰ **Hora:** {hora}"
                    )

                vistos.add(id_conquista)
                print("✔ Conquista registrada:", id_conquista)

    except Exception as e:
        print("🔥 ERROR GENERAL:", e)

    time.sleep(CHECK_INTERVAL)
