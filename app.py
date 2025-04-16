from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Pega o token do bot Telegram e o chat_id das variáveis de ambiente
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Função para enviar uma mensagem para o Telegram
def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
    }
    response = requests.post(url, data=payload)
    return response.json()

# Função para formatar o alerta com os dados do TradingView
def format_alert(data):
    # Extraímos os dados necessários
    price = data.get('price')   # preço de entrada
    tp = data.get('tp')         # valor de Take Profit
    sl = data.get('sl')         # valor de Stop Loss
    message = f"**Nova Oportunidade de Trade:**\n\n"
    message += f"**Entrar em BUY**\n"
    message += f"**Preço de Entrada:** {price}\n"
    message += f"**Take Profit (TP):** {tp}\n"
    message += f"**Stop Loss (SL):** {sl}\n"
    return message

# Rota para receber alertas do TradingView
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        print(f"Recebido alerta: {data}")

        # Verifica se a estrutura de dados está completa
        if 'price' in data and 'tp' in data and 'sl' in data:
            message = format_alert(data)  # Formata a mensagem
            send_message(message)         # Envia a mensagem para o Telegram
            return "Mensagem enviada para o Telegram", 200
        else:
            return "Dados incompletos no alerta", 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
