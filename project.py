import requests
import time
import speedtest

def testar_velocidade_url(url, max_seconds=10, chunk_size=1024*32):
    """Testa velocidade usando uma URL fornecida (download + latência)."""
    try:
        print(f"\n=== Teste com URL ({url}) ===")
        
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

        print(f"Latência: {latencia:.2f} ms")
        print(f"Baixado: {total_bytes/1024/1024:.2f} MB em {segundos:.2f} s")
        print(f"Velocidade (download): {mbps:.2f} Mbps")

    except Exception as e:
        print("Erro:", e)


def testar_velocidade_speedtest():
    """Testa velocidade download, upload, ping."""
    print("\n=== Teste com Speedtest.net ===")
    print("")
    print("Resultado do Teste.>>>")
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000  # Mbps
    upload = st.upload() / 1_000_000      # Mbps
    ping = st.results.ping

    print(f"Ping: {ping:.2f} ms")
    print(f"Download: {download:.2f} Mbps")
    print(f"Upload: {upload:.2f} Mbps")


if __name__ == "__main__":
    print("Escolha o tipo de teste:")
    print("1 - Teste manual  (URl)")
    print("2 - Teste automático (Speedtest.net)")
    escolha = input("Digite 1 ou 2: ").strip()
    print("")
    print("-------***-------")
    if escolha == "1":
        url = input("Escreva a URL para testar (ex.:www.google.com, www.youtube.com ): ").strip()
        if not url.startswith("http"):
            url = "https://" + url
        testar_velocidade_url(url)
    elif escolha == "2":
        testar_velocidade_speedtest()
        print("")
    else:
        print("Opção inválida.")
