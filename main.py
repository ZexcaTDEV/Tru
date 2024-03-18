import discord
from discord import SyncWebhook
from flask import Flask, request, jsonify, render_template
import requests
import urllib.parse
import json

app = Flask(__name__)

# Claves predefinidas
keys = [
    "Further_A1BCD3FGHIJKLM7NOPQR",
    "Further_UVWXY0Z12345E6FGHIJ",
    "Further_KLMNO8PQRSTU9VWXYZA2",
    "Further_678BCDEF4GHIJKM1LNO2",
    "Further_PQ3RSTUVW4XYZ567890",
    "Further_A1BCD3FGHIJKLM7NOPQR",
    "Further_9UVWXY0Z12345E6FGHIJ",
    "Further_KLMNO8PQRSTU9VWXYZA2",
    "Further_678BCDEF4GHIJKM1LNO2",
    "Further_PQ3RSTUVW4XYZ567890",
    "Further_A1BCD3FGHIJKLM7NOPQR",
    "Further_9UVWXY0Z12345E6FGHIJ",
    "Further_KLMNO8PQRSTU9VWXYZA2",
    "Further_678BCDEF4GHIJKM1LNO2",
    "Further_PQ3RSTUVW4XYZ567890",
    "Further_A1BCD3FGHIJKLM7NOPQR",
    "Further_9UVWXY0Z12345E6FGHIJ",
    "Further_KLMNO8PQRSTU9VWXYZA2",
    "Further_678BCDEF4GHIJKM1LNO2",
    "Further_PQ3RSTUVW4XYZ567890"
]

# Palabras clave para detectar el soporte
keywords = ['spdmteam', 'mobile.codex.lol', 'vegax', 'loot', 'linkvertise', 'platoboost']

# Endpoint para realizar el bypass
@app.route('/api/bypass', methods=['GET'])
def bypass():
    # Obtener la clave del parámetro 'key' en el query string
    key = request.args.get('key', '')

    # Verificar si la clave es válida
    if key not in keys:
        return jsonify({'error': 'Clave inválida'}), 401

    # Obtener la URL codificada del parámetro 'url' en el query string
    encoded_url = request.args.get('url', '')
    decoded_url = urllib.parse.unquote(encoded_url)

    # Verificar si la URL contiene alguna palabra clave
    supported = any(keyword in decoded_url for keyword in keywords)

    # Hacer un request a la API externa para obtener la URL del bypass
    response = requests.get("https://dlr-api-w.vercel.app")
    if response.status_code == 200:
        data = response.json()
        api_url = data.get('api_url', '')
    else:
        return jsonify({'error': 'No se pudo obtener la API URL'}), 500

    # Construir la URL final para hacer el segundo request
    final_url = f"{api_url}/api/bypass?url={encoded_url}"

    # Hacer el segundo request con el header 'Bearer'
    headers = {'Authorization': 'Bearer Delorean_T90151130355702199092780928792828907U'}
    second_response = requests.get(final_url, headers=headers)

    # Modificar la respuesta según las condiciones especificadas
    result = second_response.json().get('result', 'No result')
    if "Bypassed! open Arceus x! (insta bypass)" in result:
        result = 'Wait 5 seconds and open ArceusX'
    elif "Bypassed! wait 60s and open codex!" in result:
        result = 'Wait 40 seconds and open Codex'
    elif "Bypass detected! please get a new url to bypass this instance!" in result:
        result = 'Please get a new delta link.'

    # Crear el embed para enviar a Discord
    owner = request.remote_addr
    embed = discord.Embed(
        title="API Request",
        color=discord.Color.green()
    )
    embed.add_field(name="Ip", value=owner)
    embed.add_field(name="Requested Url", value=decoded_url)
    embed.add_field(name="Response", value=result)

    # Enviar el embed a Discord
    webhook_url = "https://discord.com/api/webhooks/1218850890308521994/75cJsf0aMeg96zioXTnZIynPhIbB3VWcUN-N4DQzREXbEm_9z03vFZbn4ijNJgMYaRCd"
    webhook = SyncWebhook.from_url(webhook_url) # Initializing webhook
    webhook.send(embed=embed)

    if supported:
        return jsonify({'result': result, 'server': "https://discord.com/invite/v24dEh3H", 'Created': "Further Staff Team"})
    else:
        return jsonify({'result': 'Not supported'}), 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
