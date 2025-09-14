from flask import Flask, render_template, request, jsonify
import requests
import time
import speedtest

app = Flask(__name__)

def testar_velocidade_url(url, max_seconds=10, chunk_size=1024*32):
    try:
        # Latência
        t0 = time.perf_counter()
        requests.head(url, timeout=5, allow_redirects=True)
        t1 = time.perf_counter()
        latencia = (t1 - t0) * 1000  # ms

        # Download
        total_bytes = 0
        inicio = time.perf_counter()
        with requests.get(url, stream=True, timeout=10, allow_redirects=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=chunk_size):
                if not chunk:
                    break
                total_bytes += len(chunk)
                if time.perf_counter() - inicio > max_seconds:
                    break
        fim = time.perf_counter()

        segundos = fim - inicio
        mbps = (total_bytes * 8) / (segundos * 1_000_000)

        return {
            "tipo": "URL",
            "url": url,
            "latencia_ms": round(latencia, 2),
            "tamanho_mb": round(total_bytes/1024/1024, 2),
            "tempo_s": round(segundos, 2),
            "download_mbps": round(mbps, 2)
        }

    except Exception as e:
        return {"erro": str(e)}

def testar_velocidade_speedtest():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping

        return {
            "tipo": "Speedtest.net",
            "ping_ms": round(ping, 2),
            "download_mbps": round(download, 2),
            "upload_mbps": round(upload, 2)
        }
    except Exception as e:
        return {"erro": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/teste", methods=["POST"])
def teste():
    tipo = request.form.get("tipo")
    url = request.form.get("url")

    if tipo == "1" and url:
        resultado = testar_velocidade_url(url)
    elif tipo == "2":
        resultado = testar_velocidade_speedtest()
    else:
        resultado = {"erro": "Opção inválida."}

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
