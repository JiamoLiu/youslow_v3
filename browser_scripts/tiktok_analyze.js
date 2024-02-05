var player = null
var currentURL = null
var sendData = {}
var extension_loaded_time = Date.now()

while (!document.getElementsByTagName("video")) {
    (async () => {
        await new Promise(r => setTimeout(r, 100));
    })();
}

const intervalID = setInterval(function () {
    const data = document.getElementsByTagName("video");
    if (data.length > 0){
        currentURL = window.location.href;
        player = document.getElementsByTagName("video");
        console.log(player)
    }
}, 250);