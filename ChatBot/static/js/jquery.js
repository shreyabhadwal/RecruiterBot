
function getBotResponse() {
    var rawText = $("#textInput").val();
    var text = rawText.replace(/\r|\n/g, "<br>");
    // console.log(text);
    // console.log(rawText);
    var userHtml = '<div class = "textBoxUser"><img  class= "logo" src="../static/images/userLogo.png") }}" alt="userLogo" /><p class="userText">  <span>' + text + "</span></p></div>";
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
    // Reset text box size
    textarea = document.querySelector("#textInput");
    this.style.height = '1.5em';
}

//Get output on pressing enter
$("#textInput").keypress(function (e) {

    if (e.which == 13) {
        if (e.shiftKey) {
            e.preventDefault()
            getBotResponse();
        }
    }
});

textarea = document.querySelector("#textInput");
textarea.addEventListener('input', autoResize, false);

function autoResize() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
}

