import mmh3
import requests
import codecs
import sys
import shodan


SHODAN_API_KEY = "Aqui_su_key"

def main():
    if len(sys.argv) < 2:
        print("[!] Error!")
        print(f"[-] Use: python3 {sys.argv[0]} <hostname>")
        sys.exit()

    # Buscar favicon en el host especificado
    favicon_url = f"http://{sys.argv[1]}/favicon.ico"
    favicon_data = get_favicon(favicon_url)

    favicon = codecs.encode(favicon_data, "base64")
    hash_favicon = mmh3.hash(favicon)

    # Realizar consulta a Shodan para encontrar hosts con el mismo favicon
    api = shodan.Shodan(SHODAN_API_KEY)
    query = f"http.favicon.hash:{hash_favicon}"
    results = api.search(query)

    # Obtener dirección IP real del host detrás de Cloudflare
    for result in results["matches"]:
        ip = result["ip_str"]
        headers = {"Host": sys.argv[1]}
        url = f"http://{ip}/favicon.ico"
        try:
            response = requests.get(url, headers=headers, verify=False, proxies={"http": "http://127.0.0.1:8080"})
            if response.status_code == 200 and response.content == favicon_data:
                print(f"[+] Hostname: {sys.argv[1]}")
                print(f"[+] IP address: {ip}")
                break
        except:
            pass

def get_favicon(favicon_url):
    try:
        response = requests.get(favicon_url, verify=False, proxies={"http": "http://127.0.0.1:8080"})
        if response.status_code == 200:
            return response.content
    except:
        pass

if _name_ == '_main_':
    main()
