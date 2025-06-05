from ollama import Client

client = Client(host='http://localhost:11434')
historico = [
    {"role": "system", "content": "Você irá ler o que o usuário digitar e extrair somente o nome de um time de futebol, sem mais informações."
    " Apenas responda com o nome do time."
    "exemplo: 'O time do Flamengo venceu o jogo.' responda 'Flamengo'."
    " Responda apenas com o nome do time, sem mais informações. o motivo é que o usuário irá utilizar o nome do time para buscar informações em uma API."
    " Caso não consiga identificar um time, responda 'Não foi possível identificar um time.'"},
]

def chat(mensagem):

    historico.append({"role": "user", "content": mensagem})
    
    # Envia todo o histórico para o Ollama
    response = client.chat(
        model='llama3.2', 
        messages=historico,
    )
    
  
    resposta = response['message']['content']
    
    # Adiciona a resposta ao histórico
    historico.append({"role": "assistant", "content": resposta})
    print (resposta)
    return resposta




# while True:
#     user_input = input("Você: ")
#     if user_input.lower() == 'sair':
#         break
#     print("Assistente:", chat(user_input))