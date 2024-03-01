var mmiCli_Out_add = "wss://"+host+":8005/IM/USER1/";
var mmiCli_Out = null;
mmiCli_Out = new MMIClientSocket(mmiCli_Out_add + "APP");
mmiCli_Out.onMessage.on(im1MessageHandler);
mmiCli_Out.onOpen.on(socketOpenHandler);
mmiCli_Out.openSocket();


function socketOpenHandler(event) {
console.log("---------------openSocketHandler---------------")

if(mmiCli_Out.socket.readyState !== WebSocket.OPEN)
{
    return;
}
}

/* UNUSED CODE
let circle = SVG.find('.circle');
let square = SVG.find('.square');
let triangle = SVG.find('.triangle');

circle.animate().attr({fill:'#ccc'});
square.animate().attr({fill:'#ccc'});
triangle.animate().attr({fill:'#ccc'});
*/

function openChatBox() {
$("#chat-box").removeClass("d-none");
}

function closeChatBox() {
    $("#chat-box").addClass("d-none");
}
  
function clearChatMessages() {
$("#chat-messages").empty();
}

function addMsgToChat(user, message){
// Determine the sender
let sender = user;
// Append the message to the chat
$("#chat-messages").append(`<div><strong class="sender">${sender}:</strong> <span class="message">${message}</span></div>`);
}

function clearContent() {
    document.getElementById("title").innerHTML = "";
    document.getElementById("image-container").innerHTML = "";
    document.getElementById("table-container").innerHTML = "";
  }
  

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

/* FUNCTION : GET RANDOM RECIPE
RETURN: 
{
"recipe_id": ,
"recipe_img": ,
"recipe_name": 
}*/
async function getRandRecipe() {
    const response = await fetch('http://127.0.0.1:5000/recipe/random');
    const data = await response.json();
    console.log("DATA INSIDE GET FUNCTION: ", data);
    return data;
}

/* FUNCTION : GET ALL RECIPES
RETURN: 
[
{
    "recipe_name": ,
    "recipe_servings": ,
    "recipe_time":
},
{
    "recipe_name": ,
    "recipe_servings": ,
    "recipe_time":
},
{
    "recipe_name": ,
    "recipe_servings": ,
    "recipe_time":
},
... 
]*/
async function getAllRecipes() {
const response = await fetch('http://127.0.0.1:5000/recipes');
const data = await response.json();
console.log("All Recipes: ", data);
return data;
}

/* FUNCTION : GET RECIPES BY TAG
RETURN: 
{
"recipe_ids": [id]
}*/
async function getRecipesByTag(tag) {
const response = await fetch(`http://127.0.0.1:5000/recipe/tag/${tag}`);
const data = await response.json();
console.log(`Recipes with tag ${tag}: `, data);
return data;
}

/* FUNCTION : GET RECIPES BY NAME - NOT WORKING -
RETURN: 
{
"recipe_id": 
}*/
async function getRecipeByName(name) {
const response = await fetch(`http://127.0.0.1:5000/recipe/name/${encodeURIComponent(name)}`);
const data = await response.json();
console.log(`Recipe named ${name}: `, data);
return data;
}

/* FUNCTION : GET INGREDIENTS BY RECIPE_ID
RETURN: 
[
{
    "name": "ingredient1",
    "quantity": "4.00",
    "unit": "uni"
},
{
    "name": "ingredient2",
    "quantity": "4.00",
    "unit": "uni"
},
... 
]*/
async function getIngredients(recipeId) {
const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/ingredients`);
const data = await response.json();
console.log(`Ingredients for recipe ID ${recipeId}: `, data);
return data;
}

/* FUNCTION : GET TOOLS BY RECIPE_ID
RETURN: 
[
[
    "tool1"
],
[
    "tool2"
],
...
]*/
async function getTools(recipeId) {
const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/tools`);
const data = await response.json();
console.log(`Tools for recipe ID ${recipeId}: `, data);
return data;
}

/* FUNCTION : GET NEXT INSTRUCTION BY RECIPE_ID AND STEP
STEP = 0 -> FIRST INSTRUCTION (STEP 1)
STEP = 1 -> SECOND INSTRUCTION (STEP 2)
...
STEP = N -> N+1 INSTRUCTION (STEP N+1) -> RETURN NULL
RETURN: 
{
"next_instruction": "instruction"
}*/
async function getNextInstruction(recipeId, step) {
const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/next-instruction/${step}`);
const data = await response.json();
console.log(`Next instruction for recipe ID ${recipeId} and step ${step}: `, data);
return data;
}

/* FUNCTION : GET PREVIOUS INSTRUCTION BY RECIPE_ID AND STEP
STEP = 0 -> FIRST INSTRUCTION (STEP -1) -> RETURN NULL
STEP = 1 -> SECOND INSTRUCTION (STEP 0) -> RETURN NULL
STEP = 2 -> THIRD INSTRUCTION (STEP 1) -> RETURN FIRST INSTRUCTION
...
STEP = N -> N-1 INSTRUCTION (STEP N) -> RETURN N INSTRUCTION
RETURN: 
{
"previous_instruction": "instruction"
}*/
async function getPreviousInstruction(recipeId, step) {
const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/previous-instruction/${step}`);
const data = await response.json();
console.log(`Previous instruction for recipe ID ${recipeId} and step ${step}: `, data);
return data;
}

/* FUNCTION : GET ACTUAL INSTRUCTION BY RECIPE_ID AND STEP
STEP = 0 -> 0 INSTRUCTION (STEP -1) -> RETURN NULL
STEP = 1 -> FIRST INSTRUCTION (STEP 1) -> RETURN FIRST INSTRUCTION
STEP = 2 -> SECOND INSTRUCTION (STEP 2) -> RETURN SECOND INSTRUCTION
...
STEP = N -> N INSTRUCTION (STEP N) -> RETURN N INSTRUCTION
RETURN: 
{
"previous_instruction": "instruction"
}*/
async function getActualInstruction(recipeId, step) {
const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/actual-instruction/${step}`);
const data = await response.json();
console.log(`Actual instruction for recipe ID ${recipeId} and step ${step}: `, data);
return data;
}

/* FUNCTION : GET RECIPE NAME BY RECIPE_ID
RETURN: 
{
"recipe_name": "name"
}*/
async function getRecipeName(recipeId) {
    const response = await fetch(`http://127.0.0.1:5000/recipe/${recipeId}/name`);
    const data = await response.json();
    console.log("CHEGAMOS AQUIIIII");
    console.log(`Name for recipe ID ${recipeId}: `, data);
    return data;
}

/* FUNCTION : GET RECIPE IMAGE BY RECIPE_ID
RETURN: 
{
"recipe_img": "url"
}*/
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

var recipe_id = 0;
var step = 1;
var voice;

async function im1MessageHandler(data) {

console.log("--------------im1MessageHandler---------------");

if(data != null && data!="RENEW" && data!="OK") {
    console.log(data);
    var content = $(data).find("emma\\:interpretation").first().text().trim();
    //console.log("CONTENTE ------> "+content);
    if (typeof content == 'string') {
    try {
        // Try to parse XML
        console.log("INSIDE TRY CATCH: " + content);

        //$("#response").html(content);
        //$("#response").addClass("container");
        //$("#response").addClass("responseText");
        console.log("CONTENT: ", content.intent);
        // Parse JSON from XML content index.htm
        let c = JSON.parse(content);
        //let recipe;
        
        console.log("C : ", c);

        if(c.hasOwnProperty("nlu")){
            console.log("NLU: ", c.nlu);
        //recipe = c.nlu.intent;
        switch(c.nlu.intent){
            case "ask_spefific_recipe":
                console.log("ASK SPECIFIC RECIPE: ");
                //console.log("ASK SPECIFIC RECIPE_VALUE: "+c.nlu.recipe);
                let tag = c.nlu.recipe; // ------------------------------------------------- Get the recipe tag
                let temp_img = await getRecipesByTag(tag); // ---------------------------------- Get the recipe_id for the specific recipe
                recipe_id = temp_img.recipe_ids[0]; // ----------------------------------------- Set the recipe_id for the specific recipe
                console.log("RECIPE_ID: ", recipe_id);
                step = 1; // --------------------------------------------------------------- Set the step to 1 - to reset the var step
                let temp_recipe_name = await getRecipeName(recipe_id); // ------------------- Get the recipe name
                let tag_recipe_name = temp_recipe_name.recipe_name; // ------------------- Get the recipe name
                console.log("TAG RECIPE NAME: ", tag_recipe_name);
                addRecipeName(tag_recipe_name); // ----------------------------- Add the recipe name to the page as <h2>
                let temp_img_url_tag = await getRecipeImage(recipe_id); // ---------------------- Get the recipe image url
                let img_url_tag = temp_img_url_tag.img_url; // --------------------------- Get the recipe image url
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
            case "greet":
                console.log("GREET -----------------------------");
                openChatBox(); // ---------------------------------------------------------- Open the chat box
                addMsgToChat('Assistente','Olá, posso ajudar?'); // ------------------------ Add the Assistent message to the chat
                sendToVoice("Olá, posso ajudar?"); // -------------------------------------- Send the voice to the user saying "Olá, posso ajudar?"
                break;
                case "goodbye":
                clearChatMessages(); // ---------------------------------------------------- Clear the chat messages
                closeChatBox(); // --------------------------------------------------------- Close the chat box
                clearContent(); // --------------------------------------------------------- Clear the content from "conteudo" div
                sendToVoice("Até à próxima"); // ------------------------------------------- Send the voice to the user saying "Até à próxima"
                break;
            case "ask_random_recipe":
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
                case "ask_first_step":
                //console.log("ASK FIRST STEP -----------------------------");
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
            case "ask_repeat_step":
                //console.log("ASK REPEAT STEP -----------------------------");
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
            case "ask_next_step":
                //console.log("ASK NEXT STEP -----------------------------");
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
            case "affirm":
            break;
            case "deny":
            break;
            case "repeat_step":
            break;
            case "confirm_step":
            break;
            case "joke":
                console.log("JOKES");
                openChatBox();
                sendToVoice("Legumes? É isso que minha comida come.");
            break;
            case "default":
            break;
        }


        }
        
        /* UNUSED CODE
        if (c.hasOwnProperty("nlu") && c.nlu.intent=="change_color") {
        switch(c.nlu.shape.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')){
            case 'triangulo': shape = triangle; break;
            case 'quadrado': shape = square; break;
            case 'circulo': shape = circle; break;
        }

        switch(c.nlu.color.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')){
            case 'azul': color = "#3333FF"; break;
            case 'verde': color = "#33FF33"; break;
            case 'cinzento': color = "#aaa"; break;
            case 'vermelho': color = "#FF3333"; break;
            case 'branco': color = "#fff"; break;
            case 'rosa': color = "#ff66b2"; break;
            case 'amarelo': color = "#ffff33"; break;
            case 'preto': color = "#000"; break;
            case 'laranja': color = "#FF9933"; break;
        }
        


        
        shape.animate().attr({ fill: color });
        sendToVoice("Mudei o " + c.nlu.shape + " para a cor " + c.nlu.color);
        }
        */

        
        /* UNUSED CODE
        setTimeout(function(){
        $("#response").html("");
        $("#response").removeClass("container");
        $("#response").removeClass("responseText");
        }, 3000);
        */
    }
    catch (e) { console.log(e); }
    }
}
}


/////

var mmiCli_1 = null;
mmiCli_1 = new MMIClient(null, "https://"+host+":8000/IM/USER1/APPSPEECH");

/* UNUSED CODE TO SEND TO VOICE
circle.on('click', function(){
    console.log("circulo");
    sendToVoice("circulo");
})

square.on('click', function(){
    console.log("quadrado");
    sendToVoice("quadradoç");
})

triangle.on('click', function(){
    console.log("triangulo");
    sendToVoice("triangulo");
})
*/

/*
function speakText(text) {
function setVoiceAndSpeak() {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'pt-PT';
    const voices = speechSynthesis.getVoices();
    const voice = voices.find(voice => voice.lang === 'pt-PT');
    if (voice) {
        utterance.voice = voice;
    }
    speechSynthesis.speak(utterance);
}

if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = setVoiceAndSpeak;
} else {
    setVoiceAndSpeak();
}
}*/

function speakText(text) {
const utterance = new SpeechSynthesisUtterance(text);
speechSynthesis.speak(utterance);
}




function sendToVoice(texto){
//let speak = "&lt;speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.w3.org/2001/10/synthesis http://www.w3.org/TR/speech-synthesis/synthesis.xsd\" xml:lang=\"pt-PT\"&gt;&lt;p&gt;" + "quadrado" + "&lt;/p&gt;&lt;/speak&gt";
//let speak = "<speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.w3.org/2001/10/synthesis http://www.w3.org/TR/speech-synthesis/synthesis.xsd\" xml:lang=\"pt-PT\"><p>"+texto+"</p></speak>";
let speak = `<speak version="1.1" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/TR/speech-synthesis11/synthesis.xsd" xml:lang="pt-PT"><p>${texto}</p></speak>`;

var result = speak;
    mmiCli_1.sendToIM(new LifeCycleEvent("APPSPEECH", "IM", "text-1", "ctx-1").
        doStartRequest(new EMMA("text-", "text", "command", 1, 0).
        setValue(JSON.stringify(result))));
}
      