from ollama import Client

client = Client(host='http://localhost:11434')
historico = [
    {"role": "system", "content": "Você é um assistente que só responde perguntas relacionadas a  futebol"
    "caso o usuário informe algo que não seja relacionado a futebol, responda com 'Desculpe, não posso ajudar com isso.'"}
]

def chat(mensagem):
    # Adiciona a mensagem do usuário ao histórico

   
    historico.append({"role": "user", "content": mensagem})
    
    # Envia todo o histórico para o Ollama
    response = client.chat(
        model='llama3.2',  # ou outro modelo de sua escolha
        messages=historico,
    )
    
    # Obtém a resposta do assistente
    resposta = response['message']['content']
    
    # Adiciona a resposta ao histórico
    historico.append({"role": "assistant", "content": resposta})
    
    return resposta

# Exemplo de uso
while True:
    user_input = input("Você: ")
    if user_input.lower() == 'sair':
        break
    print("Assistente:", chat(user_input))