
function getBotResponse() {
    var rawText = $("#textInput").val();
    var userHtml = '<div class = "textBoxUser"><img  class= "logo" src="../static/images/userLogo.png") }}" alt="userLogo" /><p class="userText">  <span>' + rawText + "</span></p></div>";
    // var userHtml = '<div class = "textBoxUser"><img  class= "logo" src="../static/images/userLogo.png" alt="userLogo" /><p class="userText">  <span>' + rawText + "</span></p></div>";
    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document
        .getElementById("userInput")
        .scrollIntoView({ block: "start", behavior: "smooth" });
    $.get("/get", { msg: rawText }).done(function (data) {
        var botHtml = '<div class = "textBoxBot"><img  class= "logo" src="../static/images/botLogo.png") }}" /><p class="botText">  <span>' + data + "</span></p></div>";
        // var botHtml = '<div class = "textBoxBot"><img  class= "logo" src="../static/images/botLogo.png" alt="botLogo" /><p class="botText">  <span>' + data + "</span></p></div>";
        $("#chatbox").append(botHtml);
        document
            .getElementById("userInput")
            .scrollIntoView({ block: "start", behavior: "smooth" });
    });
}

//Get output on pressing enter
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getBotResponse();
    }
});