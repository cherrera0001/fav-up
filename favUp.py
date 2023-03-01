import shodan

# Configurar la clave de API de Shodan
SHODAN_API_KEY = "TU_SHODAN_API_KEY"
api = shodan.Shodan(SHODAN_API_KEY)

# Consultar el hash de un sitio web
def get_favicon_hash(site_url):
    try:
        # Definir la cadena de consulta
        query = f"http.favicon.hash:<hash> {site_url}"
        # Buscar el hash del favicon en la base de datos de Shodan
        results = api.search(query)
        # Extraer el hash del favicon del primer resultado (si existe)
        if len(results['matches']) > 0:
            favicon_hash = results['matches'][0]['http']['favicon']['hash']
            return favicon_hash
        else:
            return None
    except shodan.exception.APIError as e:
        print(f"Error al consultar la API de Shodan: {e}")
        print("Sugerencia: asegúrate de que tu clave de API sea válida y que la cadena de consulta sea correcta.")

# Ejemplo de uso
site_url = "https://controltrafico-staging.falabella.com/shiftmanager"
favicon_hash = get_favicon_hash(site_url)
if favicon_hash is not None:
    print(f"Hash del favicon de {site_url}: {favicon_hash}")
else:
    print(f"No se pudo encontrar el hash del favicon de {site_url}.")
