$(document).ready(function() {
    // Toggle help box
    $("#help-button").on("click", function() {
        $("#help-box").toggleClass("d-none");
    });

    // Close help box
    $("#help-close").on("click", function() {
        $("#help-box").addClass("d-none");
    });
});
