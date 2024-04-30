/**
 * @file appGui.js
 * @brief Este ficheiro contém o código JavaScript que é executado no lado do cliente. 
 * @details Define funções para manipular a interface do utilizador e interagir com o Assistente.
 * Recebendo a intenção do utilizador e processando o comportamento do Assistente
 * 
 * @note Este ficheiro é utilizado para interagir com o Assistente e a interface do utilizador.
 * Onde é definida toda a lógica de interação com o Assistente e a interface do utilizador.
 * 
 */

/**
 * @var {string} mmiCli_Out_add
 * @brief Endereço para a conexão do socket do cliente MMI.
 * @details Este endereço é utilizado para configurar a conexão WebSocket do cliente MMI, especificando o protocolo, o host e a porta juntamente com o identificador do usuário.
 * 
 * @note Este endereço é utilizado para estabelecer a comunicação entre o cliente e o servidor.
 */
var mmiCli_Out_add = "wss://"+host+":8005/IM/USER1/";
/**
 * @var {MMIClientSocket|null} mmiCli_Out
 * @brief Instância do cliente MMI para gestão de comunicações.
 * @details Esta variável é utilizada para armazenar a instância do MMIClientSocket que gerencia a comunicação entre o cliente e o servidor. Inicialmente é definida como null e configurada posteriormente durante a inicialização.
 * 
 * 
 */
var mmiCli_Out = null;


/**
    * @typedef {Object} Product
    * @brief Um objeto para armazenar informações detalhadas sobre um produto.
    * 
    * @property {string|null} name -  O nome do produto
    * @property {number|null} quantity - A quantidade do produto 
    * @property {string|null} unit - A unidade do produto 
    * @property {Date|string|null} expiration_date - A data de validade do produto
*/


/**
 * @brief Objeto para armazenar informações detalhadas sobre um produto.
 * @details Este objeto é usado para rastrear detalhes do produto em diferentes partes da aplicação.
 * @type {Product}
 * 
 */
let product = {
    name: null,
    quantity: null,
    unit: null,
    expiration_date: null
};

/**
 * @typedef {Object} EmailConfig
 * @brief Configuração de e-mail.
 * 
 * @property {string} from_addr - O endereço de email do remetente.
 * @property {string} to_addr - O endereço de email do destinatário.
 * @property {string|null} subject - O assunto do email.
 * @property {string|null} body - O corpo do email.
 * @property {string} smtp_server - O servidor SMTP para conexão.
 * @property {number} smtp_port - A porta do servidor SMTP.
 * @property {string} password - A senha do email do remetente.
 */

/**
 * @brief Objeto global para armazenar a configuração de e-mail.
 * @details Configurações usadas para enviar e-mails através do servidor SMTP especificado.
 * @type {EmailConfig}
 */
let email = {
    from_addr: "kitchen_assistant@outlook.com",
    to_addr: "inesaguia@ua.pt",
    subject: null,
    body: null,
    smtp_server: "smtp-mail.outlook.com",
    smtp_port: 587,
    password: "kitchen123."
};

/**
 * @brief Inicializa e configura o MMIClientSocket para lidar com mensagens e eventos de conexão.
 * @details Cria uma nova instância de MMIClientSocket, anexa listeners de eventos para
 * manipulação de mensagens e eventos de conexão aberta, e então abre o socket para iniciar a comunicação.
 * @see MMIClientSocket Para mais documentação sobre a classe MMIClientSocket e seus métodos.
 */
mmiCli_Out = new MMIClientSocket(mmiCli_Out_add + "APP");
mmiCli_Out.onMessage.on(im1MessageHandler);
mmiCli_Out.onOpen.on(socketOpenHandler);
mmiCli_Out.openSocket();

/**
 * @brief Manipula o evento de abertura de conexão do socket.
 * @details Chamado quando um evento 'open' é disparado no socket. Verifica se o estado do socket é 'OPEN',
 * evitando ações subsequentes se a conexão não estiver efetivamente aberta.
 * 
 * @param {Event} event - O objeto de evento associado ao evento 'open'.
 * 
 * @note Função Já existente no Assistente/WebAppAssistantV2/index.js
 */
function socketOpenHandler(event) {
    console.log("---------------openSocketHandler---------------")

    if(mmiCli_Out.socket.readyState !== WebSocket.OPEN){
        return;
    }
}

/**
 * @brief Abre a caixa de Ajuda
 * @details Remove a classe 'd-none' da caixa de Ajuda para exibir o conteúdo. 
 * Desta forma, a caixa de Ajuda é exibida na interface do utilizador.
 */
function openHelpBox() {
$("#help-box").removeClass("d-none");
}

/**
 * @brief Fecha a caixa de Ajuda
 * @details Adiciona a classe 'd-none' à caixa de Ajuda para ocultar o conteúdo. 
 * Desta forma, a caixa de Ajuda é ocultada na interface do utilizador.
 */
function closeHelpBox() {
$("#help-box").addClass("d-none");
}

/**
 * @brief Abre a caixa de Chat
 * @details Remove a classe 'd-none' da caixa de Chat para exibir o conteúdo. 
 * Desta forma, a caixa de Chat é exibida na interface do utilizador. 
 * Podendo assim o utilizador ver as messagens escritas do Assistente.
 */
function openChatBox() {
$("#chat-box").removeClass("d-none");
}

/**
 * @brief Fecha a caixa de Chat
 * @details Adiciona a classe 'd-none' à caixa de Chat para ocultar o conteúdo.
 * Desta forma, a caixa de Chat é ocultada na interface do utilizador.
 */
function closeChatBox() {
    $("#chat-box").addClass("d-none");
}

/**
 * @brief Limpa a caixa de Chat.
 * @details Remove todas as mensagens da caixa de Chat, deixando-a vazia.
 */
function clearChatMessages() {
$("#chat-messages").empty();
}

/** 
 * @brief Adiciona uma mensagem ao chat.
 * @details Adiciona uma nova mensagem ao chat, exibindo o remetente e a mensagem na interface do utilizador.
 * 
 * @param {string} user - O utilizador que enviou a mensagem.
 * @param {string} message - A mensagem a ser enviada.
 * 
 * @return {void} É acrescentado um novo elemento de mensagem ao chat com o 'user' e 'message' fornecidos.
*/
function addMsgToChat(user, message){
// Determine the sender
let sender = user;
// Append the message to the chat
$("#chat-messages").append(`<div><strong class="sender">${sender}:</strong> <span class="message">${message}</span></div>`);
}

/**
 * @brief Limpa a homepage do Assistente.
 * @details Remove todo o conteúdo da homepage do Assistente, deixando-a vazia.
 * 
 * @return {void} O conteúdo da homepage é removido.
 */
function clearContent() {
    document.getElementById("title").innerHTML = "";
    document.getElementById("image-container").innerHTML = "";
    document.getElementById("table-container").innerHTML = "";
    }

/** 
 * @brief Adiciona um título à homepage do Assistente.
 * @details Adiciona um novo título à homepage do Assistente, exibindo-o na interface do utilizador.
 * 
 * @param {string} title - O título a ser exibido dentro da homepage num elemento h2.
*/
function addRecipeName(recipe_name) {
let container = document.getElementById("title");
// Verifica se já existe um elemento h2 dentro do contêiner
let existingH2 = container.querySelector("h2");

// Se já existir um h2, atualiza o texto
if (existingH2) {
    existingH2.textContent = recipe_name;
} else {
    // Se não, cria um novo h2 e adiciona ao contêiner
    let name = document.createElement("h2");
    name.textContent = recipe_name;
    container.appendChild(name);
}
}

/** 
 * @brief Adiciona uma imagem à homepage do Assistente.
 * @details Adiciona uma nova imagem à homepage do Assistente, exibindo-a na interface do utilizador.
 * 
 * @param {string} img_url - A URL da imagem a ser exibida.
 * 
 * @return {void} É criada uma nova imagem e adicionada ao container de imagem, substituindo a imagem existente se houver.
*/
function addImage(img_url) {
let container = document.getElementById("image-container");
// Verifica se já existe uma imagem dentro do contêiner
let existingImg = container.querySelector("img");

// Se já existir uma imagem, atualiza o atributo src
if (existingImg) {
    existingImg.src = img_url;
} else {
    // Se não, cria uma nova imagem e adiciona ao contêiner
    let img = document.createElement("img");
    img.src = img_url;
    container.appendChild(img);
}
}

/** 
 * @brief Adiciona uma tabela com 3 colunas à homepage do Assistente.
 * @details Adiciona uma nova tabela com 3 colunas à homepage do Assistente, exibindo-a na interface do utilizador.
 * As 3 colunas são: 
 *  - Ingredientes, 
 *  - Utensílios
 *  - Passos.
 * 
 * @param {array} ingredients - A lista de nomes das colunas a serem exibidas na tabela.
 * 
 * @return {void} É criada uma nova tabela com 3 colunas e os dados fornecidos.
*/
function addIngredientsTable(ingredients) {
    let container = document.getElementById("table-container");
    // Verifica e remove a tabela existente de ingredientes
    let existingTable = container.querySelector("#ingredients-table");
    if (existingTable) {
        container.removeChild(existingTable);
    }

    // Cria a nova tabela de ingredientes
    let table = document.createElement("table");
    table.id = "ingredients-table"; // Adiciona um ID único
    let thead = document.createElement("thead");
    let tbody = document.createElement("tbody");
    let rowHead = document.createElement("tr");

    // Define os títulos das colunas
    let headers = ["Ingrediente", "Valor", "Quantidade"];
    headers.forEach(headerText => {
        let header = document.createElement("th");
        header.textContent = headerText;
        rowHead.appendChild(header);
    });

    thead.appendChild(rowHead);
    table.appendChild(thead);

    // Adiciona os dados dos ingredientes no corpo da tabela
    ingredients.forEach(ingredient => {
        let row = document.createElement("tr");
        
        let nameCell = document.createElement("td");
        nameCell.textContent = ingredient.name;
        row.appendChild(nameCell);
        
        let quantityCell = document.createElement("td");
        quantityCell.textContent = ingredient.quantity;
        row.appendChild(quantityCell);
        
        let unitCell = document.createElement("td");
        unitCell.textContent = ingredient.unit;
        row.appendChild(unitCell);
        
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}

/**
 * @brief Adiciona uma tabela com Utensílios à homepage do Assistente.
 * @details Adiciona uma nova tabela com Utensílios à homepage do Assistente, exibindo-a na interface do utilizador.
 * 
 * @param {array} tools - A lista de utensílios a serem exibidos na tabela.
 * 
 * @return {void} É criada uma nova tabela com os utensílios fornecidos, substituindo a tabela existente se houver.
 * 
 */
function addToolsTable(tools) {
    let container = document.getElementById("table-container");
    // Verifica e remove a tabela existente de utensílios
    let existingTable = container.querySelector("#tools-table");
    if (existingTable) {
        container.removeChild(existingTable);
    }

    // Cria a nova tabela de utensílios
    let table = document.createElement("table");
    table.id = "tools-table"; // Adiciona um ID único
    let thead = document.createElement("thead");
    let tbody = document.createElement("tbody");
    let rowHead = document.createElement("tr");
    let header = document.createElement("th");
    header.textContent = "Utensílios";
    rowHead.appendChild(header);
    thead.appendChild(rowHead);
    table.appendChild(thead);

    // Adiciona os dados dos utensílios no corpo da tabela
    tools.forEach(tool => {
        let row = document.createElement("tr");
        let cell = document.createElement("td");
        cell.textContent = tool[0]; // Considerando que cada ferramenta é um elemento em um array
        row.appendChild(cell);
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}

/**
 * @brief Adiciona uma tabela com a Lista de Compras do utilizador.
 * @details Adiciona uma nova tabela com a Lista de Compras do utilizador à homepage do Assistente, exibindo-a na interface do utilizador.
 * 
 * @param {array} lista - A lista de compras do utilizador.
 * 
 * @return {void} É criada uma nova tabela com a lista de compras fornecida, substituindo a tabela existente se houver.
 * 
 */
function addShoopingListTable(lista) {
    let container = document.getElementById("table-container");
    // Verifica e remove a tabela existente
    let existingTable = container.querySelector("#tools-table");
    if (existingTable) {
        container.removeChild(existingTable);
    }

    // Cria a nova tabela de compras
    let table = document.createElement("table");
    table.id = "tools-table"; // Adiciona um ID único para a tabela de compras
    let thead = document.createElement("thead");
    let tbody = document.createElement("tbody");
    let rowHead = document.createElement("tr");
    let header = document.createElement("th");
    header.textContent = "Lista de Compras"; // Altera o título para Lista de Compras
    rowHead.appendChild(header);
    thead.appendChild(rowHead);
    table.appendChild(thead);

    // Adiciona os itens da lista de compras no corpo da tabela
    lista.forEach(item => {
        let row = document.createElement("tr");
        let cell = document.createElement("td");
        cell.textContent = item; // Adiciona cada item da lista na célula
        row.appendChild(cell);
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}

/**
 * @brief Adiciona uma tabela com os produtos na despensa do utilizador.
 * @details Adiciona uma nova tabela com os produtos na despensa do utilizador à homepage do Assistente, exibindo-a na interface do utilizador.
 * 
 * @param {array} lista - A lista de produtos na despensa do utilizador.
 * 
 * @return {void} É criada uma nova tabela com os produtos na despensa fornecidos, substituindo a tabela existente se houver.
 */
function addPantryTable(lista) {
    let container = document.getElementById("table-container");
    // Verifica e remove a tabela existente da despensa
    let existingTable = container.querySelector("#ingredients-table");
    if (existingTable) {
        container.removeChild(existingTable);
    }

    // Cria a nova tabela da despensa
    let table = document.createElement("table");
    table.id = "ingredients-table"; // Adiciona um ID único
    let thead = document.createElement("thead");
    let tbody = document.createElement("tbody");
    let rowHead = document.createElement("tr");

    // Define os títulos das colunas
    let headers = ["Produto", "Quantidade", "Data de Validade"];
    headers.forEach(headerText => {
        let header = document.createElement("th");
        header.textContent = headerText;
        rowHead.appendChild(header);
    });

    thead.appendChild(rowHead);
    table.appendChild(thead);

    // Adiciona os dados da despensa no corpo da tabela
    lista.forEach(item => {
        let row = document.createElement("tr");

        // Divide a string pelo padrão: ", Data de Validade : "
        let [productQuantity, expirationDate] = item.split(', Data de Validade : ');
        let productDetails = productQuantity.split(' ');
        let quantity = productDetails.pop(); // Último elemento é a quantidade com unidade
        let unit = productDetails.pop(); // Penúltimo elemento é a unidade
        let product = productDetails.join(' '); // O restante é o nome do produto

        // Célula do produto
        let productCell = document.createElement("td");
        productCell.textContent = product;
        row.appendChild(productCell);

        // Célula da quantidade
        let quantityCell = document.createElement("td");
        quantityCell.textContent = ` ${unit} ${quantity}`; // Combina quantidade e unidade
        row.appendChild(quantityCell);

        // Célula da data de validade
        let dateCell = document.createElement("td");
        dateCell.textContent = expirationDate;
        row.appendChild(dateCell);

        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}

/** 
 * @brief Adiciona uma tabela com as receitas disponíveis.
 * @details Adiciona uma nova tabela com as receitas disponíveis à homepage do Assistente, exibindo-a na interface do utilizador.
 * 
 * @param {array} recipes - A lista de receitas disponíveis.
 * 
 * @return {void} É criada uma nova tabela com as receitas fornecidas, substituindo a tabela existente se houver.
*/
function addRecipesTable(recipes) {
    let container = document.getElementById("table-container");
    // Verifica e remove a tabela existente de receitas
    let existingTable = container.querySelector("#recipes-table");
    if (existingTable) {
        container.removeChild(existingTable);
    }

    // Cria a nova tabela de receitas
    let table = document.createElement("table");
    table.id = "recipes-table"; // Adiciona um ID único
    let thead = document.createElement("thead");
    let tbody = document.createElement("tbody");
    let rowHead = document.createElement("tr");

    // Define os títulos das colunas
    let headers = ["Receita", "Serviços", "Tempo de Preparação"];
    headers.forEach(headerText => {
        let header = document.createElement("th");
        header.textContent = headerText;
        rowHead.appendChild(header);
    });

    thead.appendChild(rowHead);
    table.appendChild(thead);

    // Adiciona os dados das receitas no corpo da tabela
    recipes.forEach(recipe => {
        let row = document.createElement("tr");
        
        let nameCell = document.createElement("td");
        nameCell.textContent = recipe.recipe_name;
        row.appendChild(nameCell);
        
        let servingsCell = document.createElement("td");
        servingsCell.textContent = recipe.recipe_servings;
        row.appendChild(servingsCell);
        
        let timeCell = document.createElement("td");
        timeCell.textContent = recipe.recipe_time + ' min';
        row.appendChild(timeCell);
        
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}

/**
 * @brief Reseta o objeto de `product`.
 * @details Reseta o objeto de `product` para os valores iniciais, limpando quaisquer valores anteriores.
 * 
 * @return {void} O objeto de `product` é redefinido com valores nulos.
 */
function reset_product() {
    product = {
        name: null,
        quantity: null,
        unit: null,
        expiration_date: null
    };
}

/**
 * @brief Verifica se o produto é um produto de origem animal ou vegetal.
 * @details Verifica se o nome do produto fornecido corresponde a um produto de origem animal ou vegetal.
 * 
 * @param {string} product_name - O nome do produto a ser verificado.
 * 
 * @return {string} O tipo de produto ("animal", "plant" ou "others").
 */
function checkType(product_name) {
    for(const plant of plant_products){
        if (plant.includes(product_name)){
            return "plant";
        }
    }
    for(const animal of animal_products){
        if (animal.includes(product_name)){
            return "animal";
        }
    }
    return "others"
}

/**
 * @brief Cria uma data no formato ISO 8601.
 * @details Cria uma data no formato ISO 8601 com base no número de dias fornecido a partir da data atual.
 * 
 * @param {number} ndays - O número de dias a serem adicionados à data atual.
 * 
 * @return {string} A data de validade no formato ISO 8601.
 */
function set_expiration_date(ndays){
    let today = new Date();
    let expiration_date = today.setDate(today.getDate() + ndays);

    expiration_date = today.toISOString().slice(0,10) //Obter apenas ano,mês e dia
    
    return expiration_date
}


/**
 * @brief Alerta de produtos no final de validade.
 * @details Verifica se a data de validade do produto fornecida está a 3 dias de distância da data atual.
 * 
 * @param {string} expiration_date - A data de validade do produto.
 * 
 * @return {boolean} True se a data de validade estiver a 3 dias, False caso contrário.
 */
function alert_expiration_date(expiration_date){
    let today = new Date();
    expiration_date = new Date(expiration_date);
    
    let date_dif = Math.abs(today.getTime() - expiration_date.getTime()); //Diferença de datas em millisegundos
    date_dif  = Math.ceil(date_dif  / (1000 * 3600 * 24));//Diferença de datas em dias
    if (date_dif <=3){
        return true;
    }
    return false;
}

/**
 * @brief Obter produtos na despensa que estão perto do fim da validade.
 * @details Verifica a data de validade de cada produto na lista fornecida e retorna os produtos que estão a 3 dias de distância da data atual.
 * 
 * @param {array} product_list - A lista de produtos na despensa.
 * 
 * @return {array} near_expiration_date_products - Lista de produtos perto do fim da validade.
 */
function get_near_expiration_date_products(product_list){
    let near_expiration_date_products = [];
    for (let i = 0; i < product_list.length; i++){
        let product = product_list[i].split(":");
        let product_date = product[product.length-1];
        let near_expired = alert_expiration_date(product_date);
        if (near_expired){
            near_expiration_date_products.push(product_list[i]);
        }
    }
    return near_expiration_date_products;
}

/**
 * @brief Construir o corpo do email.
 * @details Constrói o corpo do email com base no tipo de alerta fornecido e na lista de produtos.
 * 
 * @param {string} alertType - O tipo de alerta ("expiration" ou "shoopinglist").
 * @param {array} list - A lista de produtos.
 * 
 * @return {string} body - O corpo do email formatado em HTML para ser usado no envio de email.
 */
function createEmailBody(alertType, list) {
    let body = `<html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">`;

    if (alertType === 'expiration') {
        body += `
            <h1>Alerta: Produtos Perto do Fim da Validade!</h1>
            <p>Caro cliente, informamos que os seguintes produtos estão próximos da sua data de validade:</p>
            <ul>`;
        list.forEach(item => {
            body += `<li>${item}</li>`;
        });
        body += `</ul>
            <p>Por favor, verifique estes produtos e aproveite-os enquanto estão frescos!</p>`;
    } else if (alertType === 'shoopinglist') {
        body += `
            <h1>Lista de Compras</h1>
            <p>Caro cliente, aqui está a sua lista de compras para que não se esqueça de nada:</p>
            <ul>`;
        list.forEach(item => {
            body += `<li>${item}</li>`;
        });
        body += `</ul>`;
    }

    body += `
        <p>Este email foi enviado automaticamente pelo <strong>Kitchen Assistant</strong>. Não responda a este email.</p>
        <footer><p>Com os melhores cumprimentos,</p><p><strong>Equipa Kitchen Assistant</strong></p></footer>
        </body></html>`;
    
    return body;
    //return body.replace(/"/g, '\\"');
}

/**
 * @brief Verifica se o produto já existe na despensa.
 * @details Verifica se o produto fornecido já existe na despensa e retorna a quantidade e a unidade do produto se existir.
 * 
 * @param {string} product_name - O nome do produto a ser pesquisado.
 * 
 * @return {string} data - A quantidade e a unidade do produto se existir, caso contrário, retorna "0 null".
 * 
 * @see app.check_grocery(`product_name`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function check_shoppingList(product_name) {
    try {
        // URL encode the product_name to ensure it's safe to include in a URL
        const encodedProductName = encodeURIComponent(product_name);
        const url = `http://127.0.0.1:5000/pantry/check-grocery/${encodedProductName}`;

        const response = await fetch(url, {
            method: "GET"
        });
        const data = await response.json();
        if (!response.ok) {
            console.error('Response data for error:', data); // Log the error body for debugging
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log("Product Data: ", data);
        return data;
    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}

/**
 * @brief Adiciona um produto à lista de compras.
 * @details Adiciona um produto à lista de compras, enviando um pedido [POST] para o servidor.
 * O produto é passado através do objeto `product` previamente preenchido.
 * 
 * @return {string} data - A mensagem de sucesso ou erro.
 * 
 * @note o `product` tem de estar previamente preenchido com os valores do produto a adicionar( nome, quantidade, unidade).
 * 
 * @see app.insert_grocery(`name`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function insert_shooping_list(){
    try {
        const response = await fetch("http://127.0.0.1:5000/pantry/insert-grocery", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "name": name })
        });const data = await response.json();
        if (!response.ok) {
            console.error('Response data for error:', data); // Log the error body for debugging
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log("Product Unit: ", data);
        return data;
    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}

/**
 * @brief Remove um produto da lista de compras.
 * @details Remove um produto da lista de compras, enviando um pedido [DELETE] para o servidor com seu o nome.
 * 
 * @param {string} name - O nome do produto a ser removido.
 * 
 * @return {string} data - A mensagem de sucesso ou erro na consola.
 * 
 * @see app.remove_grocery(`name`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function remove_shopping_list(name){
    try {
        const response = await fetch("http://127.0.0.1:5000/pantry/remove-grocery", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "name": name })
        });const data = await response.json();
        if (!response.ok) {
            console.error('Response data for error:', data); // Log the error body for debugging
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log("Product Unit: ", data);
        return data;
    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}

/**
 * @brief Limpa a lista de compras.
 * @details Limpa a lista de compras, enviando um pedido [DELETE] para o servidor.
 * 
 * @return {string} data - A mensagem de sucesso ou erro na consola.
 * 
 * @see app.clear_grocery() Para mais detalhes sobre a função que lida com o pedido.
 */
async function clear_shoppingList(){
    try {
        const response = await fetch('http://127.0.0.1:5000/pantry/clear-grocery', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}

/**
 * @brief Extrair a unidade de uma determinada frase.
 * @details Envia um pedido [POST] para o servidor para extrair a unidade de uma determinada frase.
 * 
 * @param {string} sentence - A frase a ser analisada.
 * 
 * @return {string} data - A unidade do produto {message: "kg"}.
 * 
 * @note A função retorna a unidade do produto com base na frase fornecida.
 * 
 * @see app.get_unit(`sentence`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function get_product_unit(sentence) {
    try {
        const response = await fetch("http://127.0.0.1:5000/get-unit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "sentence": sentence })
        });const data = await response.json();
        if (!response.ok) {
            console.error('Response data for error:', data); // Log the error body for debugging
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log("Product Unit: ", data);
        return data;
    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}

/**
 * @brief Extrair o nome do produto de uma determinada frase.
 * @details Envia um pedido [POST] para o servidor para extrair o nome do produto de uma determinada frase.
 * 
 * @param {string} sentence - A frase a ser analisada.
 * 
 * @return {string} data - O nome do produto {message: "azeite"}.
 * 
 * @see app.get_ingredient(`sentence`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function get_product_name(sentence){
    try {
        const response = await fetch("http://127.0.0.1.:5000/get-ingredient", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "sentence": sentence })
        });
        const data = await response.json();
        if (!response.ok) {
            console.error('Response data for error:', data); // Log the error body for debugging
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log("Product name: ", data);
        return data;
    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}

/**
 * @brief Limpar a despensa.
 * @details Limpa a despensa, enviando um pedido [DELETE] para o servidor.
 * 
 * @return {string} data - A mensagem de sucesso ou erro na consola.
 * 
 * @see app.clear_pantry() Para mais detalhes sobre a função que lida com o pedido.
 */
async function clear_pantry(){
    try {
        const response = await fetch('http://127.0.0.1:5000/pantry/clear', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}

/**
 * @brief Remover um produto da despensa.
 * @details Remove um produto da despensa, enviando um pedido [DELETE] para o servidor com o nome do produto.
 * 
 * @param {string} product_name - O nome do produto a ser removido.
 * 
 * @return {string} data - A mensagem de sucesso ou erro na consola.
 * 
 * @see app.remove_all_stock(`product_name`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function remove_a_product(product_name) {
    try {
        // Need to mount the URL with the product name
        const url = `http://127.0.0.1:5000/pantry/remove-all-stock/${encodeURIComponent(product_name)}`;

        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}

/**
 * @brief Converte a data para o formato {date} (SQL).
 * @details Envia um pedido [POST] para o servidor para converter a data fornecida para o formato {date} (SQL).
 * 
 * @param {string} transcript - A data a ser convertida.
 * 
 * @return {string} data - A mensagem de sucesso ou erro {message: "example message "}
 * 
 * @see app.format_date(`transcript`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function convertDateToSQLFormat(transcript) {
    try {
        const response = await fetch("http://127.0.0.1:5000/format-date", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "text": transcript })
        });
        const data = await response.json(); // Attempt to read response body even if the request is not OK
        if (!response.ok) {
            console.error('Response data for error:', data); // Log the error body for debugging
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log("DATA formatted: ", data);
        return data;
    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}

/**
 * @brief Enviar um email com a lista de produtos a expirar ou a lista de compras.
 * @details Envia um pedido [POST] para o servidor para enviar um email com a lista de produtos a expirar ou a lista de compras.
 * 
 * @param {string} alertType - O tipo de alerta ("expiration" | "shoopinglist").
 * @param {array} list - A lista de produtos.
 * 
 * @return {string} data - A mensagem de sucesso ou erro {message: "example message "}
 * 
 * @see app.send_email(`alertType`,`list`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function send_email(alertType, list){
    if (alertType === "expiration"){
        email["subject"] = "Produtos a expirar - Kitchen Assistant";
        email["body"] = createEmailBody(alertType, list);
        console.log("BODY: ", email["body"]);
    }
    else if (alertType === "shoopinglist"){
        email["subject"] = "Lista de compras - Kitchen Assistant";
        email["body"] = createEmailBody(alertType, list);
        console.log("BODY: ", email["body"]);
    }

    const response = await fetch('http://127.0.0.1:5000/send-email',
    {
        method: 'POST',
        
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(email)
    });

}

/**
 * @brief Obter os produtos na despensa.
 * @details Envia um pedido [GET] para o servidor para obter os produtos na despensa.
 * 
 * @return {array} data - A lista de produtos na despensa.
 * 
 * @see app.get_pantry_stock() Para mais detalhes sobre a função que lida com o pedido.
 */
async function get_pantry_products(){
    const response = await fetch('http://127.0.0.1:5000/pantry/stock');
    const data = await response.json();
    console.log("DATA INSIDE GET FUNCTION: ", data);
    return data;
}

/**
 * @brief Obter a lista de compras.
 * @details Envia um pedido [GET] para o servidor para obter a lista de compras.
 * 
 * @return {array} data - A lista de produtos na lista de compras.
 * 
 * @see app.get_grocery_list() Para mais detalhes sobre a função que lida com o pedido.
 */
async function get_shopping_list(){
    const response = await fetch('http://127.0.0.1:5000/pantry/shopping-list');
    const data = await response.json();
    console.log("DATA INSIDE GET FUNCTION: ", data);
    return data;
}

/**
 * @brief Inserir um produto na despensa.
 * @details Insere um produto na despensa, enviando um pedido [POST] para o servidor com os detalhes do produto.
 * 
 * @return {string} data - A mensagem de sucesso ou erro.
 * 
 * @see app.insert_stock() Para mais detalhes sobre a função que lida com o pedido.
 */
async function insert_stock() {
    
    const response = await fetch('http://127.0.0.1:5000/pantry/insert-stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(product)
    });
    const data = await response.json();
    console.log("DATA INSIDE GET FUNCTION: ", data);
}

/**
 * @brief Remover um produto da despensa.
 * @details Remove um produto da despensa, enviando um pedido [POST] para o servidor com os detalhes do produto.
 * 
 * @return {string} data - A mensagem de sucesso ou erro.
 * 
 * @see app.remove_stock() Para mais detalhes sobre a função que lida com o pedido.
 */
async function remove_stock() {
    const response = await fetch('http://127.0.0.1:5000/pantry/remove-stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(product)
    });
}


/**
 * @brief Obter uma receita aleatória.
 * @details Envia um pedido [GET] para o servidor para obter uma receita aleatória.
 * 
 * @return {array} data - A receita aleatória.
 * 
 * @code
 *  {
 *      'recipe_id': recipe_id,
 *      'recipe_name': recipe_name,
 *      'recipe_img': recipe_img
 *  }
 * @endcode
 * 
 * @see app.fetch_random_recipe() Para mais detalhes sobre a função que lida com o pedido.
 */
async function getRandRecipe() {
    const response = await fetch('http://127.0.0.1:5000/recipe/random');
    const data = await response.json();
    console.log("DATA INSIDE GET FUNCTION: ", data);
    return data;
}

/**
 * @brief Obter um produto do scanner.
 * @details Envia um pedido [POST] para o servidor para obter informações do produto a partir de um frame.
 * 
 * @param {string} frame - O frame a ser analisado.
 * 
 * @return {array} data - As informações do produto {product_name, product_quantity, product_image}.
 * 
 * @see app.get_product_barcode() Para mais detalhes sobre a função que lida com o pedido.
 */
async function getProduct_scanner(frame) {
    // Remove o prefixo de dados da string base64
    const frameData = frame.replace(/^data:image\/\w+;base64,/, "");

    const response = await fetch("http://127.0.0.1:5000/scanner", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ frameData })
    });
    const data = await response.json();
    console.log("DATA INSIDE GET FUNCTION: ", data);
    return data;
}

/**
 * @brief Inicia a captura de vídeo da webcam.
 * @details Inicia a captura de vídeo da webcam, captura frames contínuos para análise.
 * Tentar obter informações do produto de cada frame capturado usando a função `getProduct_scanner`.
 * Se informações válidas do produto são detectadas, elas são usadas para montar um "card" na interface com a imagem e detalhes do produto.
 * 
 * @return {array} product_info - As informações do produto {product_name, product_quantity, product_image}.
 */
async function takeSnapshot() {
    let product_info;
    const webcam_container = document.getElementById("webcam-container");
    // Criar um elemento de vídeo (webcam)
    const video = document.createElement("video");

    //Configuração do video
    video.id = "webcam";
    video.width = 640;
    video.height = 480;
    video.autoplay = true;
    webcam_container.appendChild(video); //Adiciona o video ao container

    const canvas = document.getElementById("canvas");
    const scanner_text = document.createElement("h2");

    //Configuração do texto do scanner
    scanner_text.id = "scanner-text";
    webcam_container.appendChild(scanner_text);


    const context = canvas.getContext("2d");
    
    const product_card = document.createElement("div");




    let stream;
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error('Error accessing the webcam: ', err);
        return;
    }

    return new Promise((resolve, reject) => {
        video.onloadedmetadata = async function() {
            while (true) {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                context.drawImage(video, 0, 0, canvas.width, canvas.height);

                const frame = canvas.toDataURL("image/jpeg", 1); //O 0.8 é a qualidade da imagem e foi usado o formato jpeg para reduzir o tamanho da imagem

    
                try {
                    product_info= await getProduct_scanner(frame); //[product_name, product_quantity, product_image]
                    scanner_text.innerHTML = "Lendo o côdigo de barras do produto... " 
                } catch (err) {
                    console.error('Error getting product scanner: ', err);
                    reject(err);
                    return;
                }
                
                if (product_info) {
                    //const answer = "O produto " + product_info[0]+" com a quantidade " + product_info[1]+ " à despensa";
                    product["name"] = product_info[0];
                    const new_quantity = product_info[1].split(" ",2);
                    product["quantity"] = new_quantity[0];
                    product["unit"] = new_quantity[1];
                    //addMsgToChat("Assistente", "nome : " + product["name"]);
                    //addMsgToChat("Assistente", "Quantidade: " + product["quantity"]);
                    //addMsgToChat("Assistente", "Unidade : " + product["unit"]);
                    
                    const info = "D"
                    
                    //Configuração do card do produto
                    product_card.id = "product-card";
                    webcam_container.appendChild(product_card);
                    
                    //Adiciona a imagem do produto e o nome do produto ao card
                    const product_image = document.createElement("img");
                    const product_name = document.createElement("h2");
                    product_card.appendChild(product_image);
                    product_card.appendChild(product_name);

                    product_image.src = product_info[2]; //Adiciona a imagem do produto ao card
                    product_name.textContent = product_info[0] + " " + product_info[1]; //Adiciona o nome do produto ao card
                    resolve(product_info);
                    return;
                }

                await new Promise(resolve => setTimeout(resolve, 1000)); // Delay
            }
        };
    }).finally(() => {
        if (stream) {
            stream.getTracks()[0].stop(); //Para o video
            video.parentElement.removeChild(video); //Remove o video da página html
            scanner_text.parentElement.removeChild(scanner_text); //Remove o texto do scanner da página html
            
    

        }
    });
}

/**
 * @brief Obter todas as receitas.
 * @details Envia um pedido [GET] para o servidor para obter todas as receitas.
 * 
 * @return {array} data - A lista de receitas.
 * 
 * @code
 * [
 *  {
 *      recipe_id: recipe_id,
 *      recipe_name: recipe_name,
 *      recipe_img: recipe_img
 *  },
 *   ...
 * ]
 * @endcode
 * 
 * @see app.fetch_recipes() Para mais detalhes sobre a função que lida com o pedido.
 */
async function getAllRecipes() {
const response = await fetch('http://127.0.0.1:5000/recipes');
const data = await response.json();
console.log("All Recipes: ", data);
return data;
}


/**
 * @brief Obter receitas por uma tag.
 * @details Envia um pedido [GET] para o servidor para obter receitas por uma tag.
 * 
 * @param {string} tag - A tag da receita.
 * 
 * @return {array} data - A lista de receitas com a tag especificada.
 * 
 * @code
 *  {
 *      recipe_id: recipe_id,
 *      recipe_name: recipe_name,
 *      recipe_img: recipe_img
 *  }
 * @endcode
 * 
 * @see app.fetch_recipe_by_tag(`tag`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function getRecipesByTag(tag) {
const response = await fetch(`http://127.0.0.1:5000/recipe/tag/${tag}`);
const data = await response.json();
console.log(`Recipes with tag ${tag}: `, data);
return data;
}


/**
 * @brief Obter uma receita por um nome.
 * @details Envia um pedido [GET] para o servidor para obter uma receita por um nome.
 * 
 * @param {string} name - O nome da receita.
 * 
 * @return {array} data - A receita com o nome especificado.
 * 
 * @code
 * {
 *     recipe_id: recipe_id
 * }
 * @endcode
 * 
 * @see app.fetch_recipe_by_name(`name`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function getRecipeByName(name) {
const response = await fetch(`http://127.0.0.1:5000/recipe/name/${encodeURIComponent(name)}`);
const data = await response.json();
console.log(`Recipe named ${name}: `, data);
return data;
}


/**
 * @brief Obter ingredientes por um ID de receita
 * @details Envia um pedido [GET] para o servidor para obter ingredientes por um ID de receita.
 * 
 * @param {string} recipeId - O ID da receita.
 * 
 * @return {array} data - A lista de ingredientes da receita.
 * 
 * @code
 * [
 *  {
 *      name: ingredient_name,
 *      quantity: ingredient_quantity,
 *      unit: ingredient_unit
 *  },
 *   ...
 * ]
 * @endcode
 * 
 * @see app.fetch
 */
async function getIngredients(recipeId) {
const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/ingredients`);
const data = await response.json();
console.log(`Ingredients for recipe ID ${recipeId}: `, data);
return data;
}


/**
 * @brief Obter ferramentas por um ID de receita.
 * @details Envia um pedido [GET] para o servidor para obter ferramentas por um ID de receita.
 * 
 * @param {string} recipeId - O ID da receita.
 * 
 * @return {array} data - A lista de ferramentas da receita.
 * 
 * @code
 *  [
 *      ["tool1"],
 *      ["tool2"],
 *    ...
 *  ]
 * @endcode
 * 
 * @see app.fetch_tools(`recipeId`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function getTools(recipeId) {
const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/tools`);
const data = await response.json();
console.log(`Tools for recipe ID ${recipeId}: `, data);
return data;
}


/**
 * @brief Obter a próxima instrução por um ID de receita e passo.
 * @details Envia um pedido [GET] para o servidor para obter a próxima instrução por um ID de receita e passo.
 * 
 *  - STEP = 0 -> FIRST INSTRUCTION (STEP 1)
 *  - STEP = 1 -> SECOND INSTRUCTION (STEP 2)
 *  - ...
 *  - STEP = N -> N+1 INSTRUCTION (STEP N+1) -> RETURN NULL
 * 
 * @param {string} recipeId - O ID da receita.
 * @param {string} step - O passo da receita.
 * 
 * @return {array} data - A próxima instrução da receita.
 * 
 * @code
 *  {
 *      next_instruction: instruction
 *  }
 * @endcode
 * 
 * @see app.fetch_next_instruction(`recipeId`,`step`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function getNextInstruction(recipeId, step) {
const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/next-instruction/${step}`);
const data = await response.json();
console.log(`Next instruction for recipe ID ${recipeId} and step ${step}: `, data);
return data;
}


/**
 * @brief Obter a instrução anterior por um ID de receita e passo.
 * @details Envia um pedido [GET] para o servidor para obter a instrução anterior por um ID de receita e passo.
 * 
 * - STEP = 0 -> FIRST INSTRUCTION (STEP -1) -> RETURN NULL
 * - STEP = 1 -> SECOND INSTRUCTION (STEP 0) -> RETURN NULL
 * - STEP = 2 -> THIRD INSTRUCTION (STEP 1) -> RETURN FIRST INSTRUCTION
 * - ...
 * - STEP = N -> N-1 INSTRUCTION (STEP N) -> RETURN N INSTRUCTION
 * 
 * @param {string} recipeId - O ID da receita.
 * @param {string} step - O passo da receita.
 * 
 * @return {array} data - A instrução anterior da receita.
 * 
 * @code
 * {
 *    previous_instruction: instruction
 * }
 * @endcode
 * 
 * @see app.fetch_previous_instruction(`recipeId`,`step`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function getPreviousInstruction(recipeId, step) {
const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/previous-instruction/${step}`);
const data = await response.json();
console.log(`Previous instruction for recipe ID ${recipeId} and step ${step}: `, data);
return data;
}


/**
 * @brief Obter a instrução atual por um ID de receita e passo.
 * @details Envia um pedido [GET] para o servidor para obter a instrução atual por um ID de receita e passo.
 * 
 * - STEP = 0 -> 0 INSTRUCTION (STEP -1) -> RETURN NULL
 * - STEP = 1 -> FIRST INSTRUCTION (STEP 1) -> RETURN FIRST INSTRUCTION
 * - STEP = 2 -> SECOND INSTRUCTION (STEP 2) -> RETURN SECOND INSTRUCTION
 * - ...
 * - STEP = N -> N INSTRUCTION (STEP N) -> RETURN N INSTRUCTION
 * 
 * @param {string} recipeId - O ID da receita.
 * @param {string} step - O passo da receita.
 * 
 * @return {array} data - A instrução atual da receita.
 * 
 * @code
 * {
 *   actual_instruction: instruction
 * }
 * @endcode
 * 
 * @see app.fetch_actual_instruction(`recipeId`,`step`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function getActualInstruction(recipeId, step) {
const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/actual-instruction/${step}`);
const data = await response.json();
console.log(`Actual instruction for recipe ID ${recipeId} and step ${step}: `, data);
return data;
}


/**
 * @brief Obter o nome da receita por um ID de receita.
 * @details Envia um pedido [GET] para o servidor para obter o nome da receita por um ID de receita.
 * 
 * @param {string} recipeId - O ID da receita.
 * 
 * @return {array} data - O nome da receita.
 * 
 * @code
 * {
 *    recipe_name: recipe_name
 * }
 * @endcode
 * 
 * @see app.fetch_recipe_name(`recipeId`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function getRecipeName(recipeId) {
    const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/name`);
    const data = await response.json();
    console.log("CHEGAMOS AQUIIIII");
    console.log(`Name for recipe ID ${recipeId}: `, data);
    return data;
}


/**
 * @brief Obter a imagem da receita por um ID de receita.
 * @details Envia um pedido [GET] para o servidor para obter a imagem da receita por um ID de receita.
 * 
 * @param {string} recipeId - O ID da receita.
 * 
 * @return {array} data - A imagem da receita.
 * 
 * @code
 * {
 *   recipe_img: "url"
 * }
 * @endcode
 * 
 * @see app.fetch_recipe_image(`recipeId`) Para mais detalhes sobre a função que lida com o pedido.
 */
async function getRecipeImage(recipeId) {
try {
    const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/image`);
    if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(`Image URL for recipe ID ${recipeId}: `, data);
    return data;
} catch (error) {
    console.error("Error fetching recipe image: ", error);
    return null; // Or handle the error as needed
}
}


/**
 * @brief Obter uma piada aleatória.
 * @details Vai buscar uma piada aleatória da lista de piadas (`jokes`).
 * 
 * @return {string} joke - A piada aleatória.
 */
function getRandJoke() {
        let joke = jokes[Math.floor(Math.random() * jokes.length)];
        console.log("Joke: ", joke);
        return joke;
}


/**
 * @var {number} recipe_id
 * @brief Identificador único para cada receita na aplicação.
 * @details Identificador único para cada receita na aplicação para depois ser feita a pesquiza na base de dados.
 */
var recipe_id = 0;

/**
 * @var {number} step
 * @brief Contador de etapas da receita atual.
 * @details Contador de etapas da receita atual, começa com o valor 1 e é incrementado ou decrementado conforme o utilizador avança ou retrocede nas etapas da receita.
 */
var step = 1;


/**
 * @var {VoiceInstance|null} voice
 * @brief Referência para a instância de voz utilizada para comandos de voz.
 */
var voice;


/**
 * @var {boolean} add_pdb_flag
 * @brief Flag para determinar se pordutos novos podem ser inseridos.
 * @details Flag para determinar se pordutos novos podem ser inseridos, se for verdadeiro, os produtos podem ser inseridos, caso contrário, não podem.
 * Começa com o valor falso, só podendo ser alterado pelo utilizador quando o intenção é adicionar um produto.
 */
var add_pdb_flag = false;

/**
 * @var {boolean} remove_pdb_flag
 * @brief Flag para determinar se produtos podem ser removidos.
 * @details Flag para determinar se produtos podem ser removidos, se for verdadeiro, os produtos podem ser removidos, caso contrário, não podem.
 * Começa com o valor falso, só podendo ser alterado pelo utilizador quando o intenção é remover um produto.
 */
var remove_pdb_flag = false;

/**
 * @var {boolean} alerted
 * @brief Indicador se o alerta de produto em fim de validade foi disparado na aplicação.
 * @details Indicador se o alerta de produto em fim de validade foi disparado na aplicação. Se for verdadeiro, o alerta foi disparado, caso contrário, não foi.
 * Começa com o valor falso, sendo alterado quando um produto está em fim de validade, ou seja quando a data de validade é inferior a 3 dias.
 */
var alerted = false;


/**
 * @var {boolean} active_assistant
 * @brief Indicador se o assistente está ativo.
 * @details Indicador se o assistente está ativo. Se for verdadeiro, o assistente está ativo, caso contrário, não está.
 * Começa com o valor falso, sendo alterado quando o assistente é ativado com uma inteção de GREETING.
 */
var active_assistant = false;

/**
 * @var {Array|null} s_list
 * @brief Lista de compras temporária, utilizada para operações pendentes.
 * @details Lista de compras temporária, utilizada para operações pendentes. 
 * Array de objetos com a estrutura {name: "product_name", quantity: "product_quantity", unit: "product_unit"}.
 */
var s_list = null;


/**
 * @var {Array|null} p_list
 * @brief Lista de produtos na despensa temporária, usada para gestão de stock.
 * @details Lista de produtos na despensa temporária, usada para gestão de stock.
 * Array de objetos com a estrutura {name: "product_name", quantity: "product_quantity", unit: "product_unit"}.
 */
var p_list = null;


/**
 * @var {string|null} answer
 * @brief Armazena a resposta do utilizador.
 * @details Armazena a resposta do utilizador para interações que requerem pequenas configurações dependendo da intenção.
 * É onde é armazenada a resposta do Assistente para posterior utilização.
 */
var answer = null;


/**
 * @type {string[]} jokes
 * @brief Lista de piadas relacionadas com comida.
 * @details Lista de piadas relacionadas com comida, que poderão sr utilizadas para entreter o utilizador.
 * As piadas são apresentadas de forma aleatória.
 * 
 * @see getRandJoke() Para mais detalhes sobre a função que obtém uma piada aleatória.
 */
const jokes = [
    'Eu gosto tanto de comida que meu super herói preferido é o super mercado.',
    'O que disse a farinha para o fermento? "Sem ti, a minha vida não cresce."',
    'Legumes?!! É isso que a minha comida come.',
    'Porque é que a manteiga não entrou na discoteca? Porque foi barrada.',
    'Qual o nome do peixe que caiu do vigésimo andar? Aaaaaaaaah, Tum!'
];


/**
* @type {string[]} plant_products
 * 
 * @brief Lista de todos os tipos de produtos vegetais (frutas/vegetais).
 * @details Lista de todos os tipos de produtos vegetais (frutas/vegetais) para que possam ser utilizados para a identificação de produtos.
 * Apos identificação, é gerada uma data de validade com 7 dias para produtos desta lista.
 * 
 * 
 * @code
 *  if(checkType(product_name) == "animal")
 *  {
 *      product["expiration_date"] = set_expiration_date(3);
 *  }
 *  }else if(checkType(product_name) == "plant")
 *  {
 *      product["expiration_date"] = set_expiration_date(3);
 *  }
 * @endcode
 * 
 * @see checkType(`product_name`) Para mais detalhes sobre a função que verifica o tipo de produto.
 * @see set_expiration_date(`days`) Para mais detalhes sobre a função que define a data de validade.
 *
 * 
 */
const plant_products = [
    // Vegetables
    "batata", "cenoura", "tomates", "alho", "cebola", "courgette", "abóbora",
    "espinafres", "pimento", "ervilhas", "beterraba", "alface", "pepino", "brócolos",
    "couve-flor", "couve", "repolho", "nabo", "rabanete", "azeitonas", "milho",
    "feijão verde", "feijão", "feijão preto", "feijão encarnado", "feijão manteiga",
    "feijão frade", "grão de bico", "lentilhas", "favas", "espargos", "beringela",
    "abacate", "couve-de-bruxelas", "chuchu", "funcho", "gengibre", "alho-francês",
    "tremoços", "tomate-cereja", "cenoura baby", "espargos verdes", "espargos brancos",
    "cogumelos", "cogumelos shitake", "cogumelos portobello", "cogumelos paris",
    "cogumelos shimeji", "cogumelos enoki", "cogumelos maitake", "cogumelos chanterelle",
    "cogumelos morel", "grelos", "nabiças", "agrião", "rucula", "rucula selvagem", "mostarda", "alface romana", "alface iceberg",

    // Fruits
    "laranja", "tangerina", "limão", "lima", "maçã", "pera", "figo", "uvas",
    "morangos", "framboesas", "mirtilos", "amoras", "frutos vermelhos",
    "kiwi", "bananas", "ananás", "abacaxi", "maracujá", "manga", "papaia",
    "melão", "meloa", "melancia", "cereja", "nectarina", "pêssego", "damascos",
    "ameixa", "ameixa seca", "passas", "tâmaras", "alperce", "cocos"
];

/**
 * @type {string[]} animal_products
 * @brief Lista de todos os tipos de produtos de origem animal (carne/peixe/lacticínios).
 * @details Lista de todos os tipos de produtos de origem animal (carne/peixe/lacticínios) para que possam ser utilizados para a identificação de produtos.
 * Apos identificação, é gerada uma data de validade com 3 dias para produtos desta lista.
 * 
 * 
 * @code
 * if(checkType(product_name) == "animal")
 *  {
 *     product["expiration_date"] = set_expiration_date(3);
 * }else if(checkType(product_name) == "plant")
 *  {
 *    product["expiration_date"] = set_expiration_date(7);
 *  }
 * @endcode
 * 
 * @see checkType(`product_name`) Para mais detalhes sobre a função que verifica o tipo de produto.
 * @see set_expiration_date(`days`) Para mais detalhes sobre a função que define a data de validade.
 */
const animal_products = [
    // Seafood
    "bacalhau", "sardinhas", "polvo", "amêijoas", "lulas", "robalo", "dourada",
    "truta", "atum", "cavala", "salmão", "peixe-espada", "pescada", "linguado",
    "carapau", "enguias", "lagosta", "camarões", "lagostim", "sapateira",
    "caranguejo", "berbigão", "búzios", "congro", "salmonete", "filetes de pescada",
    "bife de atum", "lombos de salmão", "medalhões de pescada","pescada",
    
    // Meats
    "frango", "peito de frango", "coxa de frango", "perna de frango", "asas de frango",
    "peru", "peito de peru", "coxa de peru", "perna de peru", "lombo de porco",
    "porco", "cachaço", "rojões", "entremeada", "costeleta de porco", "feveras",
    "bife", "bife da vazia", "bife do lombo", "bife da alcatra", "bife da pá",
    "bife de peru", "bife de frango", "bife de vitela", "lombo de vitela", "vitela",
    "lombo de novilho", "novilho", "lombo de vaca", "vaca", "lombo de boi", "boi",
    "lombo de cabrito", "cabrito", "lombo de borrego", "borrego", "chouriço", "presunto",
    "entrecosto", "pato", "coelho", "perdiz", "codorniz", "picanha", "alheira", "farinheira",
    "chouriça", "linguiça",
    

    // Dairy
    "queijo da serra", "queijo flamengo", "queijo de cabra", "queijo de ovelha",
    "queijo fresco", "queijo curado", "queijo ralado", "queijo emmental", "queijo mozzarella",
    "queijo cheddar", "queijo de barrar", "queijo creme", "leite", "manteiga",
    "manteiga de alho", "manteiga de ervas", "manteiga de amendoim", "manteiga de caju",
    "requeijão", "iogurte", "natas", "natas de soja", "mascarpone", "ricotta", "ovos"
];

/**
 * @brief Gere as mensagens recebidas através do WebSocket e responde com ações específicas baseadas na intenção detectada (switch case).
 * @details Esta função processa dados recebidos, verificando o conteúdo de cada mensagem. Dependendo da intenção identificada (`intent`),
 * a função executa operações correspondentes, como manipulação de interface do usuário, consultas de dados,
 * e execução de comandos de voz. Erros durante o processamento são capturados e registrados no console.
 *
 * @param {string} data - Dados recebidos pelo WebSocket. Espera-se que seja um string JSON que representa
 *                        informações de comando e estado.
 * @returns {void} Retorna uma das ações possíveis com base na intenção identificada (switch case).
 * 
 * @remark <b>case "ask_all_recipes":</b> Obter todas as receitas disponíveis 
 * 
 * @remark <b>case "ask_for_tools":</b> Obter todas as ferramentas necessárias para uma receita 
 *  
 * @remark <b>case "ask_for_ingredients":</b> Obter todos os ingredientes necessários para uma receita 
 * 
 * @remark <b>case "ask_specific_recipe":</b>  Obter uma receita específica.
 * 
 * @remark <b>case "ask_help":</b>  Obter ajuda.
 * 
 * @remark <b>case "ask_random_recipe":</b>  Obter uma receita aleatória.
 * 
 * @remark <b>case "ask_repeat_step":</b>  Repetir a etapa atual.
 * 
 * @remark <b>case "ask_first_step":</b>  Ir para a primeira etapa.
 * 
 * @remark <b>case "ask_next_step":</b>  Ir para a próxima etapa.
 * 
 * @remark <b>case "ask_pantry":</b>  Obter a lista de produtos na despensa.
 * 
 * @remark <b>case "add_pantry":</b>  Adicionar um produto à despensa.
 * 
 * @remark <b>case "add_pantry_barcode":</b>  Adicionar um produto à despensa usando um código de barras.
 * 
 * @remark <b>case "remove_pantry_barcode":</b>  Remover um produto da despensa usando um código de barras.
 * 
 * @remark <b>case "remove_pantry":</b>  Remover um produto da despensa.
 * 
 * @remark <b>case "remove_all_pantry":</b>  Remover todos os produtos da despensa/todo o produto especifico.
 * 
 * @remark <b>case "remove_all_shopping_list":</b>  Remover todos os produtos da lista de compras.
 * 
 * @remark <b>case "add_shopping_list":</b>  Adicionar um produto à lista de compras.
 * 
 * @remark <b>case "add_recipe_ingredients_pantry":</b>  Adicionar todos os ingredientes em falta de uma receita à despensa.
 * 
 * @remark <b>case "ask_shopping_list":</b>  Obter a lista de compras.
 * 
 * @remark <b>case "ask_specific_pantry":</b>  Verificar se um produto específico existe na despensa e caso exista a quantidade.
 * 
 * @remark <b>case "send_shopping_list":</b>  Enviar a lista de compras por e-mail.
 * 
 * @remark <b>case "get_quantity_ingredient":</b>  Obter a quantidade de um ingrediente específico (quantidade e unidade).
 * 
 * @remark <b>case "get_expiration_date":</b>  Obter a data de validade de um produto específico.
 * 
 * @remark <b>case "greet":</b>  Cumprimentar o assistente de forma a ativar toda a dinâmica do Assistente.
 * 
 * @remark <b>case "goodbye":</b>  Despedir-se do assistente e com isto encerrar o Assistente.
 * 
 * @remark <b>case "affirm":</b>  Responder afirmativamente a uma pergunta.
 * 
 * @remark <b>case "deny":</b>  Responder negativamente a uma pergunta.
 * 
 * @remark <b>case "joke":</b>  Obter uma piada aleatória.
 * 
 * @remark <b>case "default":</b>  Responder com uma mensagem padrão.
 *  
 * @warning <b>case "ask_for_tools":</b> [NOT IMPLEMENTED]
 * @warning <b>case "ask_for_ingredients":</b> [NOT IMPLEMENTED]
 * @warning <b>case "add_recipe_ingredients_pantry":</b> [NOT IMPLEMENTED]
 * @warning <b>case "add_recipe_ingredients_pantry":</b> [NOT IMPLEMENTED]
 * @warning <b>case "affirm":</b> [NOT IMPLEMENTED]
 * @warning <b>case "deny":</b> [NOT IMPLEMENTED]
 * 
*/
async function im1MessageHandler(data){

    console.log("--------------im1MessageHandler---------------");

    if(data != null && data!="RENEW" && data!="OK"){
        //console.log(data);
        var content = $(data).find("emma\\:interpretation").first().text().trim();
        console.log("CONTENTE ------> "+content);
        if (typeof content == 'string') {
            try {
                // Try to parse XML
                //console.log("INSIDE TRY CATCH: " + content);

                //$("#response").html(content);
                //$("#response").addClass("container");
                //$("#response").addClass("responseText");
                //console.log("CONTENT: ", content.intent);
                // Parse JSON from XML content index.htm
                let c = JSON.parse(content);
                //let recipe;
                
                //console.log("C : ", c);
                closeHelpBox(); // -------------------------------------------------------- Close the help box
                if(c.hasOwnProperty("nlu")){
                    //console.log("NLU: ", c.nlu);
                    //console.log("NLU INTENT: ", c.nlu.intent);

                    const product_card = document.getElementById("product-card");
                    if (product_card) {
                        product_card.parentElement.removeChild(product_card); //Remove o card do produto da página html
                        //Isto deve-se ao facto deste elemento ser criado sempre que é lido um código de barras
                        //E tem de ser removido depois da leitura do código de barras
                    }
                    
                    if(c.nlu.intent == "greet"){
                        active_assistant = true; // ---------------------------------------------------------------- Activate the assistant when the user greets
                    }

                    

                    if (active_assistant){ // ----------------------------------------------------------------------- Check if the assistant is active

                        switch(c.nlu.intent){
                            case "ask_all_recipes":
                                console.log("ASK ALL RECIPES -----------------------------");
                                // MOSTRAR DE TODAS AS RECEITAS
                                closeChatBox(); // -------------------------------------------------------------------- Close the chat box
                                let recipes = await getAllRecipes(); // ----------------------------------------------- Get all the recipes
                                //printRecipes("RECEITAS ", recipes); // ------------------------------------------------ Print the recipes
                                addRecipesTable(recipes); // ---------------------------------------------------------- Add the recipes to the page as <table> id = recipes-table
                                sendToVoice("Segue a lista de todas as receitas disponíveis!"); // -------------------- SEND THE VOICE TO THE USER
                                voice = c.nlu.audioReconized; // ------------------------------------------------------ Get the voice from the user
                                openChatBox(); // --------------------------------------------------------------------- Open the chat box
                                clearChatMessages() // ---------------------------------------------------------------- Clear the chat messages (when asked for a new recipe)
                                addMsgToChat('Você',': ' + voice); // ------------------------------------------------- Add the voice to the chat
                                addMsgToChat('Assistente','Escolha uma receita para começar a preparação'); // -------- Add the Assistent message to the chat
                                break;
                            case "ask_for_tools":
                                console.log("ASK FOR TOOLS -----------------------------");
                                break;
                            case "ask_for_ingredients":
                                console.log("ASK FOR INGREDIENTS -----------------------------");
                                break;
                            case "ask_spefific_recipe":
                                console.log("ASK SPECIFIC RECIPE -----------------------------");
                                closeHelpBox(); // -------------------------------------------------------- Close the help box
                                clearContent(); // -------------------------------------------------------- Clear the content
                                console.log("ASK SPECIFIC RECIPE: ");
                                //console.log("ASK SPECIFIC RECIPE_VALUE: "+c.nlu.recipe);
                                let tag = c.nlu.recipe; // ------------------------------------------------- Get the recipe tag
                                let temp_img = await getRecipesByTag(tag); // ------------------------------ Get the recipe_id for the specific recipe
                                recipe_id = temp_img.recipe_ids[0]; // ------------------------------------- Set the recipe_id for the specific recipe
                                console.log("RECIPE_ID: ", recipe_id);
                                step = 1; // --------------------------------------------------------------- Set the step to 1 - to reset the var step
                                let temp_recipe_name = await getRecipeName(recipe_id); // ------------------ Get the recipe name
                                let tag_recipe_name = temp_recipe_name.recipe_name; // --------------------- Get the recipe name
                                console.log("TAG RECIPE NAME: ", tag_recipe_name);
                                addRecipeName(tag_recipe_name); // ----------------------------------------- Add the recipe name to the page as <h2>
                                let temp_img_url_tag = await getRecipeImage(recipe_id); // ----------------- Get the recipe image url
                                let img_url_tag = temp_img_url_tag.img_url; // ----------------------------- Get the recipe image url
                                addImage(img_url_tag); // -------------------------------------------------- Add the recipe image to the page as <img>
                                let ingredients_tag = await getIngredients(recipe_id); // ------------------ Get the ingredients for the recipe
                                addIngredientsTable(ingredients_tag); // ----------------------------------- Add the ingredients to the page as <table> id = ingredients-table
                                let tools_tag = await getTools(recipe_id); // ------------------------------ Get the tools for the recipe
                                addToolsTable(tools_tag); // ----------------------------------------------- Add the tools to the page as <table> id = tools-table
                                // ------------------------------------------------------------------------- SEND THE VOICE TO THE USER
                                // - THE PUNCTUATION AFFECTS THE TIME BETWEEN THE TWO SENTENCES -
                                sendToVoice("RECEITA ESCOLHIDA : "+ tag_recipe_name + " . Quando estiver pronto podemos começar a receita");
                                voice = c.nlu.audioReconized; // ------------------------------------------- Get the voice from the user
                                openChatBox(); // ---------------------------------------------------------- Open the chat box (for the first interaction)
                                clearChatMessages() // ----------------------------------------------------- Clear the chat messages (when asked for a new recipe)
                                addMsgToChat('Você',': ' + voice); // -------------------------------------- Add the voice to the chat
                                // ------------------------------------------------------------------------- Add the Assistent message to the chat (hint for the user)
                                addMsgToChat('Assistente','INICIAR A PREPARAÇÃO : Vamos começar com a receita');
                                break;
                            case "ask_help":
                                console.log("ASK HELP -----------------------------");
                                closeChatBox();
                                sendToVoice("Segue a lista de comandos aceites para interagir comigo!");
                                openHelpBox();
                                break;
                            case "ask_random_recipe":
                                console.log("ASK RANDOM RECIPE -----------------------------");
                                closeHelpBox(); // -------------------------------------------------------- Close the help box
                                clearContent(); // -------------------------------------------------------- Clear the content
                                //console.log(c.nlu);
                                data = await getRandRecipe() // -------------------------------------------- Get the random recipe
                                recipe_id = data.recipe_id; // --------------------------------------------- Set the recipe_id fer the random recipe
                                step = 1; // --------------------------------------------------------------- Set the step to 1 - to reset the var step
                                //console.log("RECIPE_ID : " , recipe_id); 
                                //console.log("DATA: " , data);
                                //console.log("DATA PARSING" + data.recipe_name);
                                let recipe_name = data.recipe_name; // ------------------------------------- Get the recipe name
                                addRecipeName(recipe_name); // --------------------------------------------- Add the recipe name to the page as <h2>
                                let img_url = data.recipe_img; // ------------------------------------------ Get the recipe image url
                                console.log("IMG URL: " + img_url);
                                addImage(img_url); // ------------------------------------------------------ Add the recipe image to the page as <img>
                                let ingredients = await getIngredients(data.recipe_id); // ----------------- Get the ingredients for the recipe
                                addIngredientsTable(ingredients); // --------------------------------------- Add the ingredients to the page as <table> id = ingredients-table
                                //console.log("INGREDIENTS: ", ingredients);
                                let tools = await getTools(data.recipe_id); // ----------------------------- Get the tools for the recipe
                                addToolsTable(tools); // --------------------------------------------------- Add the tools to the page as <table> id = tools-table
                                //console.log("TOOLS: ", tools);
                                // ------------------------------------------------------------------------- SEND THE VOICE TO THE USER
                                // - THE PUNCTUATION AFFECTS THE TIME BETWEEN THE TWO SENTENCES -
                                sendToVoice("RECEITA ESCOLHIDA : "+ recipe_name + " . Quando estiver pronto podemos começar a receita");
                                voice = c.nlu.audioReconized; // ------------------------------------------- Get the voice from the user
                                openChatBox(); // ---------------------------------------------------------- Open the chat box (for the first interaction)
                                clearChatMessages() // ----------------------------------------------------- Clear the chat messages (when asked for a new recipe)
                                addMsgToChat('Você',': ' + voice); // -------------------------------------- Add the voice to the chat
                                // ------------------------------------------------------------------------- Add the Assistent message to the chat (hint for the user)
                                addMsgToChat('Assistente','INICIAR A PREPARAÇÃO : Vamos começar com a receita');
                                break;
                            case "ask_repeat_step":
                                console.log("ASK REPEAT STEP -----------------------------");
                                let repeat_instruction = await getActualInstruction(recipe_id, step); // --- Get the actual instruction for the recipe
                                //console.log("REPEAT INSTRUCTION: ", repeat_instruction.actual_instruction);
                                voice = c.nlu.audioReconized; // ------------------------------------------- Get the voice from the user
                                //openChatBox();
                                addMsgToChat('Você',': ' + voice); // -------------------------------------- Add the voice to the chat
                                addMsgToChat('Assistente', repeat_instruction.actual_instruction); // ------ Add the actual instruction to the chat
                                sendToVoice("A instrução é: "+ repeat_instruction.actual_instruction); // -- SEND THE VOICE THE ACTUAL INSTRUCTION
                                // ------------------------------------------------------------------------- Add the Assistent message to the chat (hint for the user)
                                addMsgToChat('Assistente','PRÓXIMA INSTRUÇÃO : Avança para o próximo passo');
                                break;
                            case "ask_first_step":
                                console.log("ASK FIRST STEP -----------------------------");
                                let instruction = await getActualInstruction(recipe_id, step); // ---------- Get the first instruction for the recipe
                                //console.log("INSTRUCTION: ", instruction.actual_instruction); 
                                voice = c.nlu.audioReconized; // ------------------------------------------- Get the voice from the user
                                //openChatBox();
                                addMsgToChat('Você',': ' + voice); // -------------------------------------- Add the voice to the chat
                                addMsgToChat('Assistente', instruction.actual_instruction); // ------------- Add the first instruction to the chat
                                // ------------------------------------------------------------------------- SEND THE VOICE THE FIRST INSTRUCTION
                                sendToVoice("A primeira instrução é: "+ instruction.actual_instruction);
                                // ------------------------------------------------------------------------- Add the Assistent message to the chat (hint for the user)
                                addMsgToChat('Assistente','PRÓXIMA INSTRUÇÃO : Avança para o próximo passo');
                                break;
                            case "ask_next_step":
                                console.log("ASK NEXT STEP -----------------------------");
                                let next_instruction = await getNextInstruction(recipe_id, step); // ------- Get the next instruction for the recipe
                                voice = c.nlu.audioReconized;
                                if (next_instruction == null) { // ----------------------------------------- If there are NO MORE instructions
                                    //console.log("NO MORE INSTRUCTIONS");
                                    //openChatBox();
                                    addMsgToChat('Você',': ' + voice);
                                    addMsgToChat('Assistente','FIM DA RECEITA : A receita terminou');
                                    sendToVoice("A receita terminou");
                                    break;
                                }else{ // ------------------------------------------------------------------- If there are MORE instructions
                                    step++; // ---------------------------------------------------------------- Increment the step
                                    //console.log("NEXT INSTRUCTION: ", next_instruction.next_instruction);
                                    //openChatBox();
                                    addMsgToChat('Você',': ' + voice); // ------------------------------------- Add the voice to the chat
                                    addMsgToChat('Assistente', next_instruction.next_instruction); // --------- Add the next instruction to the chat
                                    // ------------------------------------------------------------------------ SEND THE VOICE THE NEXT INSTRUCTION
                                    sendToVoice("A próxima instrução é: "+next_instruction.next_instruction); 
                                    // ------------------------------------------------------------------------ Add the Assistent message to the chat (hint for the user) 
                                    addMsgToChat('Assistente','PROXIMA INSTRUÇÃO : Avança para o próximo passo');
                                }
                            break;
                            case "ask_pantry":
                                console.log("ASK PANTRY -----------------------------");
                                clearContent(); // -------------------------------------------------------- Clear the content
                                let pantry_products = await get_pantry_products(); // ---------------------- Get all the products in the pantry
                                addRecipeName("Produtos na Despensa"); // ------------------------------------ Add the title to the page as <h2>
                                addPantryTable(pantry_products); // ---------------------------------------- Add the pantry products to the page as <table> id = pantry-table
                                // ------------------------------------------------------------------------- SEND THE VOICE TO THE USER
                                sendToVoice("Segue a lista de produtos na despensa!"); // ---------------------- SEND THE VOICE TO THE USER
                                // O que tenho na despensa
                                break;
                            case "add_pantry":
                                // Adiciona [3](quantidade) [ovos](ingrediente) à despensa
                                // Comprei [ovos](ingrediente)
                                console.log("ADD PANTRY -----------------------------");
                                add_pdb_flag = true; // ------------------------------------------------------ Set the flag to true
                                let name = c.nlu.audioReconized; // ---------------------------------------------------- Get the ingredient
                                if(name){
                                    name = await get_product_name(name); // -------------------------------------- Get the type of the product
                                    product["name"] = name["message"]; // ----------------------------------------------- Store the ingredient
                                }
                                let quantity = c.nlu.quantity; // -------------------------------------------- Get the quantity
                                if(quantity)
                                    product["quantity"] = quantity; // ----------------------------------------- Store the quantity
                                let unit = c.nlu.unit; // ------------------------------------------------------ Get the unit
                                if(unit){
                                    unit = await get_product_unit(unit)
                                    product["unit"] = unit["message"]; // --------------------------------------------------- Store the unit
                                }else
                                    product["unit"] = "uni"; // -------------------------------------------------- Default unit
                                // name && quantity
                                // name && unit & quantity
                                // name 
                                //
                                
                                console.log("PRODUCT: ", product);
                                if(product["name"] && !product["quantity"] && product["unit"]){
                                    // ask for the quantity
                                    sendToVoice("Indique a quantidade do produto");
                                    mmiCli_12.sendToIM(new LifeCycleEvent("SPEECH_ANSWER", "IM", "text-1", "ctx-1").
                                        doStartRequest(new EMMA("text-", "text", "command", 1, 0).
                                        setValue(JSON.stringify({text: "Get Quantity Ingredient"})))); // ------------ Call the function to get the quantity
                                }else if(product["name"] && product["quantity"] && product["unit"]){
                                    // ask for the expiration_date
                                    if(checkType(product["name"]) == "animal"){
                                        console.log("ANIMAL PRODUCT -----------------------------");
                                        // add a pre-established expiration_date for animal products : 3 DAYS
                                        product["expiration_date"] = set_expiration_date(3); // ---------------------- Set the expiration date
                                        // --------------------------------------------------------------------------- Create the message to the user
                                        await insert_stock(); // ----------------------------------------------------------- Insert the product to the pantry
                                        await remove_shopping_list(product["name"]); // ------------------------------------------------------ Remove the product from the shopping list
                                        await clearContent(); // -------------------------------------------------------- Clear the content
                                        s_list = await get_shopping_list(); // -------------------------------------- Get the shopping list
                                        p_list = await get_pantry_products(); // -------------------------------------- Get the pantry list
                                        await addPantryTable(p_list); // ------------------------------------------------------ Add the pantry list to the page as <table> id = pantry-table
                                        await addShoopingListTable(s_list); // ---------------------------------------- Add the shopping list to the page as <table> id = shopping-list-table 
                                        answer = "O produto foi inserido com sucesso" // ------------------------ Create the VOICE message to the user
                                        sendToVoice(answer); // ----------------------------------------------------- Send the voice msg to the user
                                        openChatBox(); // ------------------------------------------------------------ Open the chat box
                                        answer = "O produto "+ product["name"] + " com a quantidade " + product["quantity"] + " " + product["unit"] + " foi <span style='color: green;'>ADICIONADO</span> à despensa com a data de validade " + product["expiration_date"];
                                        addMsgToChat("Assistente", answer); // -------------------------------------- Add the message to the chat
                                        reset_product(); // ---------------------------------------------------------- Reset the product dictionary
                                        add_pdb_flag = false; // ----------------------------------------------------- Reset the flag
                                    }else if(checkType(product["name"]) == "plant"){
                                        console.log("PLANT PRODUCT -----------------------------");
                                        // add a pre-established expiration_date for plant products : 7 DAYS ( 1 week )
                                        product["expiration_date"] = set_expiration_date(7); // ---------------------- Set the expiration date
                                        // --------------------------------------------------------------------------- Create the message to the user
                                        await insert_stock(); // ----------------------------------------------------------- Insert the product to the pantry
                                        await remove_shopping_list(product["name"]); // ------------------------------------------------------ Remove the product from the shopping list
                                        await clearContent(); // -------------------------------------------------------- Clear the content
                                        s_list = await get_shopping_list(); // -------------------------------------- Get the shopping list
                                        p_list = await get_pantry_products(); // -------------------------------------- Get the pantry list
                                        await addPantryTable(p_list); // ------------------------------------------------------ Add the pantry list to the page as <table> id = pantry-table
                                        await addShoopingListTable(s_list); // ---------------------------------------- Add the shopping list to the page as <table> id = shopping-list-table 
                                        answer = "O produto foi inserido com sucesso" // ------------------------ Create the VOICE message to the user
                                        sendToVoice(answer); // ----------------------------------------------------- Send the voice msg to the user
                                        openChatBox(); // ------------------------------------------------------------ Open the chat box
                                        answer = "O produto "+ product["name"] + " com a quantidade " + product["quantity"] + " " + product["unit"] + " foi <span style='color: green;'>ADICIONADO</span> à despensa com a data de validade " + product["expiration_date"];
                                        addMsgToChat("Assistente", answer); // -------------------------------------- Add the message to the chat
                                        reset_product(); // ---------------------------------------------------------- Reset the product dictionary
                                        add_pdb_flag = false; // ----------------------------------------------------- Reset the flag
                                    }else{
                                        // ask for the expiration_date
                                        sendToVoice("Indique uma data de validade");
                                        mmiCli_12.sendToIM(new LifeCycleEvent("SPEECH_ANSWER", "IM", "text-1", "ctx-1").
                                            doStartRequest(new EMMA("text-", "text", "command", 1, 0).
                                            setValue(JSON.stringify({text: "Get Expiration Date"})))); // ----- Call the function to get the expiration date
                                    }
                                }
                                break;
                            case "add_pantry_barcode":
                                console.log("ADD PANTRY BARCODE -----------------------------");
                                clearContent(); // -------------------------------------------------------- Clear the content
                                add_pdb_flag = true; // ------------------------------------------------------ Set the flag to true
                                await takeSnapshot(); // ----------------------------------------------------- Read the barcode
                                sendToVoice("O produto foi lido com sucesso, indique a data de validade"); //- SEND THE VOICE TO THE USER
                                mmiCli_12.sendToIM(new LifeCycleEvent("SPEECH_ANSWER", "IM", "text-1", "ctx-1").
                                    doStartRequest(new EMMA("text-", "text", "command", 1, 0).
                                    setValue(JSON.stringify({text: "Get Expiration Date"})))); // ------------ Call the function to get the expiration date
                                break;
                            case "remove_pantry_barcode":
                                console.log("REMOVE PANTRY BARCODE -----------------------------");
                                clearContent(); // -------------------------------------------------------- Clear the content
                                await takeSnapshot(); // ----------------------------------------------------- Read the barcode
                                await remove_stock(); // ----------------------------------------------------------- Insert the product to the pantry
                                const product_card = document.getElementById("product-card");
                                if (product_card) {
                                    product_card.parentElement.removeChild(product_card); //Remove o card do produto da página html
                                    //Isto deve-se ao facto deste elemento ser criado sempre que é lido um código de barras
                                    //E tem de ser removido depois da leitura do código de barras
                                }
                                //clearContent(); // -------------------------------------------------------- Clear the content
                                s_list = await get_shopping_list(); // -------------------------------------- Get the shopping list
                                p_list = await get_pantry_products(); // -------------------------------------- Get the pantry list
                                addPantryTable(p_list); // ------------------------------------------------------ Add the pantry list to the page as <table> id = pantry-table
                                addShoopingListTable(s_list); // ---------------------------------------- Add the shopping list to the page as <table> id = shopping-list-table 
                                sendToVoice("O produto foi removido com sucesso"); //- SEND THE VOICE TO THE USER
                                
                                openChatBox(); // ------------------------------------------------------------ Open the chat box
                                answer = "O produto " + product["name"] + 
                                    " com a quantidade " + product["quantity"] + 
                                    " " + product["unit"] + 
                                    " foi <span style='color: red;'>REMOVIDO</span> ";
                                //answer = "O produto "+ product["name"] + " com a quantidade " + product["quantity"] + " " + product["unit"] + " foi REMOVIDO à despensa com a data de validade ";
                                addMsgToChat("Assistente", answer); // -------------------------------------- Add the message to the chatreset_product(); // ---------------------------------------------------------- Reset the product dictionary
                                reset_product(); // ---------------------------------------------------------- Reset the product dictionary
                                break;
                            case "remove_pantry":
                                console.log("REMOVE PANTRY -----------------------------");
                                let name_rmv = c.nlu.audioReconized; // ---------------------------------------------------- Get the ingredient
                                console.log("NAME TO REMOVE: ", name_rmv);
                                if(name_rmv){
                                    name_rmv = await get_product_name(name_rmv);
                                    console.log("NAME TO REMOVE: ", name_rmv["message"]);
                                    product["name"] = name_rmv["message"]; // --------------------------------------------------- Store the ingredient
                                }
                                let quantity_rmv = c.nlu.quantity; // -------------------------------------------- Get the quantity
                                if(quantity_rmv)
                                    product["quantity"] = quantity_rmv; // ----------------------------------------- Store the quantity
                                let unit_rmv = c.nlu.unit; // ------------------------------------------------------ Get the unit
                                if(unit_rmv){
                                    unit_rmv = await get_product_unit(unit_rmv)
                                    product["unit"] = unit_rmv["message"]; // --------------------------------------------------- Store the unit
                                }else
                                    product["unit"] = "uni"; // -------------------------------------------------- Default unit
                                // name && quantity
                                // name && unit & quantity
                                // name 
                                // 
                                if(product["name"] && !product["quantity"] && product["unit"]){
                                    // ask for the quantity
                                    sendToVoice("Indique a quantidade do produto");
                                    mmiCli_12.sendToIM(new LifeCycleEvent("SPEECH_ANSWER", "IM", "text-1", "ctx-1").
                                        doStartRequest(new EMMA("text-", "text", "command", 1, 0).
                                        setValue(JSON.stringify({text: "Get Quantity Ingredient"})))); // ------------ Call the function to get the quantity
                                }else if(product["name"] && product["quantity"] && product["unit"]){
                                    // ask for the expiration_date
                                    // --------------------------------------------------------------------------- Create the message to the user
                                    await remove_stock(); // ----------------------------------------------------------- Insert the product to the pantry
                                    await clearContent(); // -------------------------------------------------------- Clear the content
                                    s_list = await get_shopping_list(); // -------------------------------------- Get the shopping list
                                    p_list = await get_pantry_products(); // -------------------------------------- Get the pantry list
                                    await addPantryTable(p_list); // ------------------------------------------------------ Add the pantry list to the page as <table> id = pantry-table
                                    await addShoopingListTable(s_list); // ---------------------------------------- Add the shopping list to the page as <table> id = shopping-list-table 
                                    answer = "O produto foi removido com sucesso" // ------------------------ Create the VOICE message to the user
                                    sendToVoice(answer); // ----------------------------------------------------- Send the voice msg to the user
                                    openChatBox(); // ------------------------------------------------------------ Open the chat box
                                    answer = "O produto " + product["name"] + 
                                        " com a quantidade " + product["quantity"] + 
                                        " " + product["unit"] + 
                                        " foi <span style='color: red;'>REMOVIDO</span> ";
                                    //answer = "O produto "+ product["name"] + " com a quantidade " + product["quantity"] + " " + product["unit"] + " foi REMOVIDO à despensa com a data de validade ";
                                    addMsgToChat("Assistente", answer); // -------------------------------------- Add the message to the chat
                                    reset_product(); // ---------------------------------------------------------- Reset the product dictionary
                                }
                                break;
                            case "remove_all_pantry":
                                console.log("REMOVE ALL PANTRY -----------------------------");
                                let pantry_products_rmv = c.nlu.audioReconized; // ---------------------------------------------------- Get the ingredient
                                pantry_products_rmv = await get_product_name(pantry_products_rmv);
                                console.log("PANTRY PRODUCT TO REMOVE: ", pantry_products_rmv["message"]);
                                if(pantry_products_rmv["message"] == null){
                                    console.log("REMOVER TODOS OS PRODUTOS DA DESPENSA");
                                    // apagar toda a dispensa
                                    await clear_pantry(); // ------------------------------------------------------ Clear the pantry
                                    sendToVoice("A despensa foi limpa!"); // ---------------------- SEND THE VOICE TO THE USER
                                }else{
                                    console.log("REMOVER TODAS AS OCORRENCIAS DO PRODUTO");
                                    // remover todas as ocurencias desse produto
                                    await remove_a_product(pantry_products_rmv["message"]); // -------------------------------------- Remove the specific product
                                    sendToVoice("Foi removido o produto " + pantry_products_rmv["message"] + " da despensa!"); // ---------------------- SEND THE VOICE TO THE USER
                                }
                                await clearContent(); // -------------------------------------------------------- Clear the content
                                s_list = await get_shopping_list(); // -------------------------------------- Get the shopping list
                                p_list = await get_pantry_products(); // -------------------------------------- Get the pantry list
                                await addPantryTable(p_list); // ------------------------------------------------------ Add the pantry list to the page as <table> id = pantry-table
                                await addShoopingListTable(s_list); // ---------------------------------------- Add the shopping list to the page as <table> id = shopping-list-table 
                                break;
                            case "remove_all_shopping_list":
                                console.log("REMOVE ALL SHOPPING LIST -----------------------------");
                                await clear_shoppingList(); // ------------------------------------------------------ Clear the pantry
                                sendToVoice("A Lista de compras foi limpa!"); // ---------------------- SEND THE VOICE TO THE USER
                                await clearContent(); // -------------------------------------------------------- Clear the content
                                s_list = await get_shopping_list(); // -------------------------------------- Get the shopping list
                                p_list = await get_pantry_products(); // -------------------------------------- Get the pantry list
                                await addPantryTable(p_list); // ------------------------------------------------------ Add the pantry list to the page as <table> id = pantry-table
                                await addShoopingListTable(s_list); // ---------------------------------------- Add the shopping list to the page as <table> id = shopping-list-table 
                                break;
                            case "add_shopping_list":
                                console.log("ADD SHOPPING LIST -----------------------------");
                                add_pdb_flag = true; // ------------------------------------------------------ Set the flag to true
                                let name_shopping = c.nlu.audioReconized; // ---------------------------------------------------- Get the ingredient
                                console.log("NAME SHOPPING: ", name_shopping);
                                if(name_shopping){
                                    name_shopping = await get_product_name(name); // -------------------------------------- Get the type of the product
                                    console.log("NAME SHOPPING ---> : ", name_shopping["message"]);
                                    product["name"] = name_shopping["message"]; // ----------------------------------------------- Store the ingredient
                                }

                                if (product["name"]){
                                    await insert_shooping_list(product["name"]); // -------------------------------------- Insert the product to the shopping list
                                    await clearContent(); // -------------------------------------------------------- Clear the content
                                    s_list = await get_shopping_list(); // -------------------------------------- Get the shopping list
                                    p_list = await get_pantry_products(); // -------------------------------------- Get the pantry list
                                    await addPantryTable(p_list); // ------------------------------------------------------ Add the pantry list to the page as <table> id = pantry-table
                                    await addShoopingListTable(s_list); // ---------------------------------------- Add the shopping list to the page as <table> id = shopping-list-table 
                                    answer = "O produto foi inserido com sucesso" // ------------------------ Create the VOICE message to the user
                                    sendToVoice(answer); // ----------------------------------------------------- Send the voice msg to the user
                                    openChatBox(); // ------------------------------------------------------------ Open the chat box
                                    answer = "O produto "+ product["name"] + " foi <span style='color: green;'>ADICIONADO</span> à lista de compras";
                                    addMsgToChat("Assistente", answer); // -------------------------------------- Add the message to the chat
                                    reset_product(); // ---------------------------------------------------------- Reset the product dictionary
                                    add_pdb_flag = false; // ----------------------------------------------------- Reset the flag
                                }else{
                                    openChatBox(); // ------------------------------------------------------------ Open the chat box
                                    addMsgToChat("Assistente", "Não percebi qual foi o produto a adicionar"); // --------------- Add the message to the chat
                                    await sendToVoice("Não percebi qual foi o produto a adicionar à lista de compras, repita pff"); // -------------------- SEND THE VOICE TO THE USER
                                    mmiCli_12.sendToIM(new LifeCycleEvent("SPEECH_ANSWER", "IM", "text-1", "ctx-1").
                                    doStartRequest(new EMMA("text-", "text", "command", 1, 0).
                                    setValue(JSON.stringify({text: "Tente adicionar um produto"})))); // --------- Call the function to get the expiration date
                                }
                                break;
                            case "add_recipe_ingredients_pantry":
                                console.log("ADD RECIPE INGREDIENTS PANTRY -----------------------------");
                                break;
                            case "ask_shopping_list":
                                console.log("ASK SHOPPING LIST -----------------------------");
                                clearContent(); // -------------------------------------------------------- Clear the content
                                s_list = await get_shopping_list(); // ------------------------------------- Get the shopping list
                                await addRecipeName("Lista de Compras"); // ---------------------------------------- Add the title to the page as <h2>
                                await addShoopingListTable(s_list); // ------------------------------------------------- Add the shopping list to the page as <table> id = shopping-list-table
                                sendToVoice("Segue a lista de compras!"); // -------------------------------------- SEND THE VOICE TO THE USER
                                break;
                            case "ask_specific_pantry":
                                console.log("ASK SPECIFIC PANTRY -----------------------------");
                                let asp_name = c.nlu.audioreconized; // ---------------------------------------------------- Get the ingredient
                                console.log("NAME TO CHECK: ", asp_name);
                                if(asp_name){
                                    asp_name = await get_product_name(asp_name);
                                    console.log("Audio Recognized: ", asp_name["message"]);
                                    product["name"] = asp_name["message"]; // --------------------------------------------------- Store the ingredient
                                }
                                let asp_value = await check_shoppingList(product["name"]); // -------------------------------------- Check if the product is in the pantry
                                let parts = asp_value["message"].split(" ");
                                console.log("ASP VALUE: ", parts);
                                if(parts[0] == "0"){
                                    sendToVoice("O produto " + product["name"] + " não se encontra na despensa"); // ---------------------- SEND THE VOICE TO THE USER
                                }else{
                                    answer = "Tem "+ parts[0]+ " " + parts[1]+ " de "+ product["name"] + " na despensa";
                                    sendToVoice(answer); // ---------------------- SEND THE VOICE TO THE USER
                                    openChatBox(); // ------------------------------------------------------------ Open the chat box
                                    addMsgToChat("Assistente", answer); // -------------------------------------- Add the message to the chat
                                }
                                reset_product(); // ---------------------------------------------------------- Reset the product dictionary
                                break;
                            case "send_shopping_list":
                                console.log("SEND SHOPPING LIST -----------------------------");
                                s_list = await get_shopping_list(); // ------------------------------------- Get the shopping list 
                                //console.log("SHOPPING LIST: ", s_list);
                                if(s_list.length > 0){
                                    // send the shopping list
                                    await send_email("shoopinglist", s_list); // -------------------------------------- SEND EMAIL
                                    console.log("---------> EMAIL SENT <---------");
                                    sendToVoice("A sua lista de compras foi enviada para o seu email"); // ------------ SEND THE VOICE TO THE USER
                                    openChatBox(); // ------------------------------------------------------------ Open the chat box
                                    addMsgToChat("Assistente", "A sua lista de compras foi enviada para o seu email"); // --- Add the message to the chat
                                }
                                break;
                            case "get_quantity_ingredient":
                                if(add_pdb_flag){
                                    console.log("GET QUANTITY INGREDIENT -----------------------------");
                                    product["quantity"] = c.nlu.quantity; // ------------------------------------- Get & Store the quantity
                                    let unidade = c.nlu.unit; // ------------------------------------------------- Get the unit
                                    if(unidade){
                                        unidade = await get_product_unit(unidade);
                                        product["unit"] = unidade["message"]; // -------------------------------------------- Store the unit
                                    }else
                                        product["unit"] = "uni"; // ---------------------------------------------- Infer & Store the unit
                                    /*let name = c.nlu.audioReconized; // ---------------------------------------------------- Get the ingredient
                                    if(name){
                                        name = await get_product_name(name); // -------------------------------------- Get the type of the product
                                        product["name"] = name["message"]; // ----------------------------------------------- Store the ingredient
                                    }*/
                                    
                                    // --------------------------------------------------------------------------- Check if all the fields are filled
                                    if (product["name"] && product["quantity"] && product["unit"] && !product["expiration_date"]){
                                        // ask for the expiration_date
                                        sendToVoice("Indique uma data de validade");
                                        mmiCli_12.sendToIM(new LifeCycleEvent("SPEECH_ANSWER", "IM", "text-1", "ctx-1").
                                            doStartRequest(new EMMA("text-", "text", "command", 1, 0).
                                            setValue(JSON.stringify({text: "Get Expiration Date"})))); // ----- Call the function to get the expiration date
                                    }else{
                                        // FALTA FAZER A LOGICA::::::::
                                    }
                                    openChatBox(); // ------------------------------------------------------------ Open the chat box
                                    // --------------------------------------------------------------------------- Create the message to the user
                                    addMsgToChat("Você", "Quantidade: " + product["quantity"] + " " + product["unit"] + " de " + product["name"]);
                                }else{
                                    console.log("ADD_PDB_FLAG IS FALSE");
                                    openChatBox(); // ------------------------------------------------------------ Open the chat box
                                    addMsgToChat("Assistente", "Primeiro adicione um produto"); // --------------- Add the message to the chat
                                    mmiCli_12.sendToIM(new LifeCycleEvent("SPEECH_ANSWER", "IM", "text-1", "ctx-1").
                                    doStartRequest(new EMMA("text-", "text", "command", 1, 0).
                                    setValue(JSON.stringify({text: "Tente adicionar um produto"})))); // --------- Call the function to get the expiration date
                                }
                                break;
                            case "get_expiration_date":
                                if (add_pdb_flag){ // ------------------------------------------------------------ Check if already added a product
                                    console.log("GET EXPIRATION DATE -----------------------------");
                                    let expiration_date = c.nlu.audioReconized; // ------------------------------ Get the expiration date
                                    console.log("EXPIRATION DATE - audio: ", expiration_date);
                                    let formated_date = await convertDateToSQLFormat(expiration_date); // ---------------- Convert the date to SQL format
                                    console.log("EXPIRATION DATE - convertDateToSQLFormat: ", formated_date);
                                    product["expiration_date"] = formated_date; // ----- Convert the date to SQL format
                                    console.log("PRODUCT : ", product["expiration_date"]);
                                    // --------------------------------------------------------------------------- Create the message to the user
                                    await insert_stock(); // ----------------------------------------------------------- Insert the product to the pantry
                                    await remove_shopping_list(product["name"]); // ------------------------------------------------------ Remove the product from the shopping list
                                    console.log(" UPDATE PANTRY TABLE"); // -------------------------------------- Update the pantry table
                                    clearContent(); // -------------------------------------------------------- Clear the content
                                    s_list = await get_shopping_list(); // -------------------------------------- Get the shopping list
                                    p_list = await get_pantry_products(); // -------------------------------------- Get the pantry list
                                    await addPantryTable(p_list); // ------------------------------------------------------ Add the pantry list to the page as <table> id = pantry-table
                                    await addShoopingListTable(s_list); // ---------------------------------------- Add the shopping list to the page as <table> id = shopping-list-table 
                                    answer = "O produto foi inserido com sucesso" // ------------------------ Create the VOICE message to the user
                                    sendToVoice(answer); // ----------------------------------------------------- Send the voice msg to the user
                                    openChatBox(); // ------------------------------------------------------------ Open the chat box
                                    answer = "O produto "+ product["name"] + " com a quantidade " + product["quantity"] + " " + product["unit"] + " foi <span style='color: green;'>ADICIONADO</span> à despensa com a data de validade " + product["expiration_date"];
                                    addMsgToChat("Assistente", answer); // -------------------------------------- Add the message to the chat
                                    reset_product(); // ---------------------------------------------------------- Reset the product dictionary
                                    add_pdb_flag = false; // ----------------------------------------------------- Reset the flag
                                }else{ // ------------------------------------------------------------------------ If the product was NOT added open Mic to add one
                                    console.log("ADD_PDB_FLAG IS FALSE");
                                    openChatBox(); // ------------------------------------------------------------ Open the chat box
                                    addMsgToChat("Assistente", "Primeiro adicione um produto"); // --------------- Add the message to the chat
                                    mmiCli_12.sendToIM(new LifeCycleEvent("SPEECH_ANSWER", "IM", "text-1", "ctx-1").
                                    doStartRequest(new EMMA("text-", "text", "command", 1, 0).
                                    setValue(JSON.stringify({text: "Tente adicionar um produto"})))); // --------- Call the function to get the expiration date
                                }
                                break;
                            case "greet":
                                closeHelpBox(); // -------------------------------------------------------- Close the help box
                                console.log("GREET -----------------------------");
                                active_assistant = true; // ------------------------------------------------ Activate the assistant
                                openChatBox(); // ---------------------------------------------------------- Open the chat box
                                addMsgToChat('Assistente','Olá, posso ajudar?'); // ------------------------ Add the Assistent message to the chat
                                await sendToVoice("Olá, posso ajudar?"); // -------------------------------------- Send the voice to the user saying "Olá, posso ajudar?"
                                if (!alerted){ // ------------------------------------------------------------------------------ Check if the email was already sent
                                    // check if the product is near the expiration date
                                    let product_list = await get_pantry_products(); // ----------------------------------------- Get all the products in the pantry
                                    let near_expiration_date_products = get_near_expiration_date_products(product_list); // ---- Get the products that are near the expiration date
                                    // CONSTRUCT EMAIL 
                                    if (near_expiration_date_products.length > 0){
                                        await send_email("expiration", near_expiration_date_products); // ---------------------- SEND EMAIL
                                        console.log("---------> EMAIL SENT <---------");
                                        alerted = true;
                                        email["body"] = null; // --------------------------------------------------------------- Reset the email body
                                        email["subject"] = null; // ------------------------------------------------------------ Reset the email subject
                                    }
                                    alerted = true;
                                }
                                s_list = await get_shopping_list(); // ------------------------------------------------ Get the shopping list
                                p_list = await get_pantry_products(); // ------------------------------------------------ Get the pantry products
                                await addRecipeName("Despensa"); // ------------------------------------------------------ Add the recipe name to the page as <h2>
                                await addPantryTable(p_list); // ------------------------------------------------------------ Add the pantry table to the page
                                await addShoopingListTable(s_list); // ------------------------------------------------------ Add the shopping list table to the page
                                break;
                            case "goodbye":
                                console.log("GOODBYE -----------------------------");
                                closeHelpBox(); // -------------------------------------------------------- Close the help box
                                clearChatMessages(); // ---------------------------------------------------- Clear the chat messages
                                closeChatBox(); // --------------------------------------------------------- Close the chat box
                                clearContent(); // --------------------------------------------------------- Clear the content from "conteudo" div
                                sendToVoice("Espero ter ajudado, até à próxima!!"); // ------------------------------------------- Send the voice to the user saying "Até à próxima"
                                active_assistant = false; // ------------------------------------------------ Deactivate the assistant
                                reset_product(); // ---------------------------------------------------------- Reset the product dictionary
                                break;
                            case "affirm":
                                break;
                            case "deny":
                                break;
                            case "joke":
                                console.log("JOKES -----------------------------");
                                openChatBox();
                                let joke_selected = getRandJoke();
                                addMsgToChat('Assistente',joke_selected); // --------- Add the joke to the chat
                                sendToVoice(joke_selected);
                                break;
                            case "default":
                                console.log("DEFAULT -----------------------------");
                                break;
                        }
                        // end switch

                    }else{
                        sendToVoice("Para ativar o Assistente diga: Olá Assistente");
                        mmiCli_12.sendToIM(new LifeCycleEvent("SPEECH_ANSWER", "IM", "text-1", "ctx-1").
                                doStartRequest(new EMMA("text-", "text", "command", 1, 0).
                                setValue(JSON.stringify({text: "GREET ASSISTANT TO INICIATE"})))); // ------------ Call the function to get the expiration da
                    }

                }
            }catch (e) {
                    console.log(e); 
            }
        }
    }
}


/////

/**
 * @var {MMIClient} mmiCli_1 - variável que guarda a instância do cliente MMI
 */
var mmiCli_1 = null;

/**
 * @brief Cria uma instância do cliente MMI
 * @details Cria uma instância do cliente MMI, que é responsável por enviar mensagens para o IM,
 * e guarda essa instância na variável mmiCli_1
 */
mmiCli_1 = new MMIClient(null, "https://"+host+":8000/IM/USER1/APPSPEECH");

/**
 * @brief Função que envia um texto para ser lido pela voz
 * @details Função que envia um texto para ser lido pela voz, utilizando a API de SpeechSynthesis da Google Cloud
 * 
 * @param {String} text - texto a ser lido
 * 
 */
function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
}

/**
 * @brief Função que envia um texto para ser lido pela voz
 * @details Função que envia um texto para ser lido pela voz, utilizando a API de SpeechSynthesis da Google Cloud
 * 
 * @param {String} texto - texto a ser lido
 * 
 * @returns {void} o Assitente lê o texto enviado
 */
function sendToVoice(texto){
    //console.log("TESTE SEND TO VOICE: ", texto);
    //let speak = "&lt;speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.w3.org/2001/10/synthesis http://www.w3.org/TR/speech-synthesis/synthesis.xsd\" xml:lang=\"pt-PT\"&gt;&lt;p&gt;" + "quadrado" + "&lt;/p&gt;&lt;/speak&gt";
    //let speak = "<speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.w3.org/2001/10/synthesis http://www.w3.org/TR/speech-synthesis/synthesis.xsd\" xml:lang=\"pt-PT\"><p>"+texto+"</p></speak>";
    //let speak = `<speak version="1.1" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/TR/speech-synthesis11/synthesis.xsd" xml:lang="pt-PT"><p>${texto}</p></speak>`;

    //var result = speak;
    //mmiCli_1 = new MMIClient(null, "https://"+host+":8000/IM/USER1/APPSPEECH");
    
    // WORKING SPEECH 
    var synth = window.speechSynthesis;
    var utterance = new SpeechSynthesisUtterance(texto);
    utterance.lang = 'pt-PT'; // Set the language to Portuguese (Portugal)
    synth.speak(utterance);
}



// code to send a message to the IM -------------------------------------------------------------------

/**
 * @var {MMIClient} mmiCli_12 - variável que guarda a instância do cliente MMI
 * @brief variável que guarda a instância do cliente MMI
 * @details variável que guarda a instância do cliente MMI, que é responsável por enviar mensagens para o IM, 
 * de forma a poder interagir com o modulo index.htm
 */
var mmiCli_12 = new MMIClient(null, "https://"+host+":8000/IM/USER1/SPEECH_ANSWER");


//mmiCli_12.sendToIM(new LifeCycleEvent("SPEECH_ANSWER", "IM", "text-1", "ctx-1").
//        doStartRequest(new EMMA("text-", "text", "command", 1, 0).
//        setValue(JSON.stringify({text: "TESTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"}))));

// -----------------------------------------------------------------------------------------------------
