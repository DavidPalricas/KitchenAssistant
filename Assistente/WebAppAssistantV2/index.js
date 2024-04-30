/**
 * @file index.js
 * 
 * @brief Este arquivo serve para a comunicação IM ( intermodal ) entre o assistente e o appGui.htm.
 * @details Este arquivo contém funções que permitem a comunicação entre o assistente e o appGui.htm.
 * 
 * @note Este arquivo é um exemplo de como pode ser feita a comunicação entre o assistente e o appGui.htm.
 * O Ficheiro foi fornecido pela equipa do projeto e foi adaptado para o projeto. 
 * As Funções aqui documentadas foram as que foram adicionadas ou alteradas para o projeto.
 */

/**
    * @brief Processa o final_transcript da fala, converte-o(SPEECH TO TEXT - GOOGLE CLOUD) e envia para o cliente MMI.
    * 
    * - 1º: Converte números falados nas suas representações digitais. 
    *
    * - 2º: Cria um objeto para enviar ao servidor, que inclui o final_transcript processado pelo RASA.
    * 
    * - 3º: Constrói diferentes mensagens, dependendo da inteção reconhecida pelo RASA e envia-as para o cliente MMI através do método `sendToIM`.
    * 
    * @param {string} final_transcript - O final_transcript recebido do reconhecimento de voz (SPEECH TO TEXT - GOOGLE CLOUD).
    * @return {Promise} Uma promessa que é resolvida quando a interação MMI é tratada com sucesso.
    * 
    * 
 */
async function sendMMI(final_transcript){
    
}

// como comunicar inversamente com o APPGUI ------------------> TEMOS DE FAZER ISTO DE FORMA A ATIVAR O MICRO

/**
 * @brief Manipula mensagens recebidas do cliente WebSocket MMI, mensgens essas que vêm da interação do appGui.htm.
 * 
 * @function im1MessageHandler1
 * @param {Object} data - Data recebida do servidor.
 * 
 * @code
 * // JavaScript code
 * var mmiCli_Out_add = "wss://"+host+":8005/IM/USER1/"; // Alterar para o endereço do servidor
 * var mmiCli_Out1 = null; // Cria um cliente MMI WebSocket
 * mmiCli_Out1 = new MMIClientSocket(mmiCli_Out_add + "ASSISTANT_ANSWER"); // Cria um cliente MMI WebSocket para comunicar com o appGui.htm
 * mmiCli_Out1.onMessage.on(im1MessageHandler1); Manipula mensagens recebidas do cliente WebSocket MMI.
 * mmiCli_Out1.onOpen.on(socketOpenHandler); // Manipula mensagens recebidas do cliente WebSocket MMI.
 * mmiCli_Out1.openSocket(); // Abre o socket
 * @endcode
 */


/**
 * @brief Manipula mensagens recebidas do cliente WebSocket MMI e adiciona um delay de 5s.
 * - Foi criado este threshold para que o reconhecimento de fala não seja ativado imediatamente após a interação com o appGui.htm.
 * Dando tempo ao assistente de acabar a sua comunicação.
 * 
 * @function im1MessageHandler1
 * @param {Object} data - Data received from the server.
 * 
 */
function im1MessageHandler1(data){
    // Inicia o reconhecimento de fala
    run_delay();
}
// -------------------------------------------------------------------------------------------------------------

/**
 * @brief Atrasa a execução por um número especificado de milissegundos.
 * 
 * @function delay
 * @param {number} ms - O número de milissegundos a aguardar.
 * @return {Promise} Uma promessa que é resolvida após o atraso.
 * 
 * @code
 * // waits 5 s until the next line is executed
 * delay(5000)
 * @endcode
 * 
 */
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * @brief Inicia um processo de atraso, em seguida, inicia o reconhecimento de fala e 
 * atualiza a interface do usuário para saber quando o microfone está ativo.
 *  - Predefinição para 5 segundos.
 * 
 * @async
 * @function run_delay
 * 
 * @code 
 * // Wait for 5 seconds - 5000 ms
 * await delay(5000);
 * @endcode
 * 
 * */
async function run_delay() {
    console.log("Starting delay...");
    await delay(5000); // Wait for 5 seconds
    console.log("Delay finished.");
    recognition.start();
    circle.animate(20, 0, 'now').attr({ fill: '#00a431' });
    transcriptDiv.textContent = "...";
}

/** 
 * @brief Vai buscar o valor associado a uma chave. 
 * 
 * Neste caso é utilizado para ir buscar o valor associado à chave "value" no objeto retornado pelo RASA. 
 * onde podemos ir buscar:
 * - intent (intenção)
 * - entity (entidade)
 * - value (valor)
 * - audioReconized (áudio reconhecido)
 * 
 * @function findValueByKey
 * @param {Object} structure - A estrutura de dados onde procurar.
 * @param {string} keyToFind - A chave a procurar ( entidade: definias no NLU - RASA).
 * 
 * @return {string} O valor associado à chave. 
 * 
 * @code 
 * data.entities = 
 * {
 *  "recognized":["SPEECH","SPEECHIN","APP"],
 *  "text":"T2zDoSBhc3Npc3RlbnRl",
 *  "nlu":
 *    {
 *     "intent":"greet",
 *     "audioReconized":"Olá assistente"
 *    }
 * }
 * var result = findValueByKey(data.entities,"audioReconized");
 * // return: 
 * "Olá assistente"
 * @endcode
 * 
 */
function findValueByKey(structure, keyToFind) {
    for(const sub_dict in structure){
    for(const key in structure[sub_dict]){
        if(structure[sub_dict][key] == keyToFind){
            return structure[sub_dict].value;
        }
    }
    }
}


/**
 * @brief Converte números falados nas suas representações de dígitos 
 * para simplificar o processamento no RASA.
 * 
 * @async
 * @function convert_numbers_into_digits
 * @param {string} transcript - O texto a ser convertido.
 * @returns {data<string>} O texto convertido com números em dígitos.
 * 
 * @code
 * convert_numbers_into_digits("Adiciona quatro ovos à despensa.")
 * // return:
 * "Adiciona 4 ovos à despensa."
 * @endcode
 * 
 */
async function convert_numbers_into_digits(transcript){
    const response = await fetch("http://127.0.0.1:5000/convert-text",
    {
    method : "POST",
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({"text": transcript})
    });
    const data = await response.json();
    console.log("Transcript converted",data);
    return data;
}












