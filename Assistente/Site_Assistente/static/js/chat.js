console.log("Chat está funcionando!");

$(document).ready(function() {
    $("#chat-button").on("click", function() {
        $("#chat-box").toggleClass("d-none");
    });

    $("#chat-close").on("click", function() {
        $("#chat-box").add("d-none");
    });

    $("#chat-input").keypress(function(event) {
        if (event.which === 13) { //Se a tecla pressionada for enter
            let message = $(this).val(); //Extrai o valor do campo de texto


            $(this).val(""); //Limpa o campo de texto

            $("#chat-messages").append("<div><strong>Você:</strong>" + message + "</div>"); //Adiciona a mensagem no chat

            $.ajax({
                type: "POST",
                url: "/webhook",
                contentType: "application/json",
                data: JSON.stringify({ message: message }),
                success: function(data) {
                    let rasa_response = data.response;
                    $("#chat-messages").append("<div><strong>Assistente:</strong>" + rasa_response + "</div>");
                }



            });

        }
    });

})