import openai
import requests
import time

openai.api_key = "INSERTA_TOKEN"
TOKEN = "INSERTA_TOKEN_TELEGRAM"

def get_updates(offset):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()["result"]

def send_messages(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response

def get_openai_response(prompt):
    system = '''
        Eres un asistente de atencion a clientes 
        y estudiantes de la plataforma de educación online en tecnología,  
        inglés y liderazgo llamada Platzi
        '''
    response = openai.chat.completions.create(
		model='NOMBRE_MODELO_FINE_TUNING',
		messages=[
            {"role": "system", "content" :f'{system}'},
            {"role": "user", "content" : f'{prompt}'}],
		max_tokens=150,
		n=1,
		temperature=0.2)
    return response.choices[0].message.content.strip()

def main():
    print("Starting bot...")
    offset = 0
    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] +1
                chat_id = update["message"]["chat"]['id']
                user_message = update["message"]["text"]
                print(f"Received message: {user_message}")
                GPT = get_openai_response(user_message)
                send_messages(chat_id, GPT)
        else:
            time.sleep(1)
if __name__ == '__main__':
    main()