from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS
from openai import OpenAI
from config import OPENAI_API_KEY  #Aquivo que contém a chave particular do OpenAI
from datetime import datetime

import os
app = Flask(__name__, template_folder=os.path.join("templates"), static_folder=os.path.join("static"))
CORS(app)  #Permite que o frontend acesse o backend

client = OpenAI(api_key=OPENAI_API_KEY)

data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime("%d-%m-%Y %H:%M")

@app.route('/')
def index():
    return render_template("index.html")

#Função para enviar prompt para o ChatGPT e retornar a sua resposta (gerar o projeto)
def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um especialista em ensino de programação e propõe boas ideias para professores que querem criar novos projetos para seus alunos."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    return response.choices[0].message.content

#Função para salvar as respostas do ChatGPT em um documento txt
def salvar_log(write_file, data_e_hora_em_texto):
    with open("log.txt", "a", encoding="utf-8") as arquivo:  #"a" para adicionar sem apagar o conteúdo anterior
        arquivo.write("\n---------NOVA RESPOSTA---------\n" + "\n" + data_e_hora_em_texto + "\n" + write_file + "\n") 

@app.route('/gerar-projeto', methods=['POST']) #Rota para o HTML
def gerar_projeto():
    dados = request.json  #Recebe os dados enviados pelo frontend

    #Criando o prompt com as respostas do formulário
    prompt = (
        "Sou um professor e quero que você gere um projeto "
        f"que será realizado por {dados['qtd_alunos']} alunos de {dados['faixa_etaria']}, {dados['grupo']}. "
        f"Os alunos têm o seguinte nível de experiência em tecnologia: {dados['nivel_experiencia']}. "
        f"Esse projeto será passado como {dados['tipo_tarefa']} e deverá ter um nível "
        f"{dados['nivel_dificuldade']}. A ferramenta usada pelos alunos será {dados['ferramenta']}. "
        f"O projeto tem o seguinte objetivo: {dados['objetivo']}. Ele deverá durar {dados['duracao']} "
        f"e abordar os seguintes conceitos: {dados['conceitos']}. Use o seguinte tema como base para a sua resposta: {dados['tema']}."
        "Na sua resposta, não inclua saudações ou falas direcionadas a mim e inclua somente as informações que pedi."
        "Siga o seguinte formato na sua resposta: Nome do Projeto, Descrição, Objetivo, Lista de Atividades (em detalhes)"
        "e Código Base (nessa parte, forneça um código de programação em português que faça o projeto que você criou, funcionar)."
    )

    resposta = chat_with_gpt(prompt)  #Envia o prompt para o ChatGPT

    salvar_log(resposta, data_e_hora_em_texto)  #Salva a resposta no arquivo

    return jsonify({"resposta": resposta})  #Retorna a resposta para o frontend


if __name__ == '__main__':
    app.run(debug=True)  #Inicia o servidor Flask

