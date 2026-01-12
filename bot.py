import requests
import time
from bs4 import BeautifulSoup

URL = "https://es.twstats.com/es96/index.php?page=tribe&mode=conquers&id=30&type=gain&oldtribe=0"
WEBHOOK_URL = "PEGA_AQUI_TU_WEBHOOK"

CHECK_INTERVAL = 30
vistos = set()

def enviar_discord(texto):
    requests.post(WEBHOOK_URL, json={"content": texto})

while True:
    try:
        r = requests.get(URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        tabla = soup.find("table")
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

            id_conquista = f"{pueblo}-{nuevo_jugador}-{antiguo_jugador}-{hora}"

            if id_conquista not in vistos:
                if vistos:
                    enviar_discord(
                        "🏰 **NUEVA CONQUISTA**\n\n"
                        f"🏘️ Pueblo: {pueblo}\n\n"
                        f"🟢 Nuevo dueño: {nuevo_jugador}\n"
                        f"🟢 Tribu nueva: {nueva_tribu}\n\n"
                        f"🔴 Antiguo dueño: {antiguo_jugador}\n"
                        f"🔴 Tribu antigua: {antigua_tribu}\n\n"
                        f"⏰ Hora: {hora}"
                    )

                vistos.add(id_conquista)

    except Exception as e:
        print("Error:", e)

    time.sleep(CHECK_INTERVAL)
