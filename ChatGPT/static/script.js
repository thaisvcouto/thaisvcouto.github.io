document.getElementById("formulario").addEventListener("submit", async function(event) {
    event.preventDefault(); //Evita o recarregamento da página

    //Captura os dados do formulário
    let qtd_alunos = document.getElementById("qtd_alunos").value;
    let faixa_etaria = document.getElementById("faixa_etaria").value;
    let grupo = document.getElementById("grupo").value;
    let nivel_experiencia = document.getElementById("nivel_experiencia").value;
    let tipo_tarefa = document.getElementById("tipo_tarefa").value;
    let nivel_dificuldade = document.getElementById("nivel_dificuldade").value;
    let ferramenta = document.getElementById("ferramenta").value;
    let objetivo = document.getElementById("objetivo").value;
    let duracao = document.getElementById("duracao").value;
    let conceitos = document.getElementById("conceitos").value;
    let tema = document.getElementById("tema").value;

    let dados = {
        qtd_alunos: qtd_alunos,
        faixa_etaria: faixa_etaria,
        grupo: grupo,
        nivel_experiencia : nivel_experiencia,
        tipo_tarefa : tipo_tarefa,
        nivel_dificuldade : nivel_dificuldade,
        ferramenta : ferramenta,
        objetivo : objetivo,
        duracao : duracao,
        conceitos : conceitos,
        tema : tema
    };

    try {
        let resposta = await fetch("https://projeta-ai-backend.onrender.com/gerar-projeto", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });

        let resultado = await resposta.json();
        let divResposta = document.getElementById("resposta")
        let jsonResposta = resultado.resposta
        console.log("Resposta bruta do servidor:", resultado.resposta);
        //Formatando resposta do Chat GPT para tirar caracteres não desejados
        jsonResposta = jsonResposta.replace(/\n/g, "<br>"); // Converte /n para quebra de linha
        jsonResposta = jsonResposta.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>"); // Converte **texto** para negrito
        jsonResposta = jsonResposta.replace(/```(.*?)```/g, "<code>$1</code>"); // Converte formatação de código para fonte diferente
        
        divResposta.innerHTML = jsonResposta; // O que está dentro da div recebe o resultado gerado pelo GPT
        
        document.getElementById("resposta-container").style.display = "block";
        document.getElementById("form-container").style.display = "none";

    } catch (erro) {
        console.error("Erro ao conectar com o servidor:", erro);
    }
});

