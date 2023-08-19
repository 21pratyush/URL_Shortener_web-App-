var link = document.getElementById("shortened-url");
var url = link.href;
var textArea = document.createElement("textarea");

function copyToClipboard() {
    textArea.value = url;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("copy");
    document.body.removeChild(textArea);

    alert("Shortened URL copied to clipboard!");
}

function openUrl() {
    window.open(link.href, "_blank");
}