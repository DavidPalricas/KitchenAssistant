console.log("Chat está funcionando!");

$(document).ready(function() {
    $("#chat-button").on("click", function() {
        $("#chat-box").toggleClass("d-none");
    });

    $("#chat-close").on("click", function() {
        $("#chat-box").add("d-none");
    });



})