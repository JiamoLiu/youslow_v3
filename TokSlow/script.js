"use strict";
/*jshint esversion: 9 */
/* jshint -W097 */

// default url where report server is located
const quality_change_url = "http://localhost:34543/quality";
const state_change_url = "http://localhost:34543/state";
const stats_url = "https://a487-169-231-110-155.ngrok-free.app";
const report_time = 250;
var player = null
var currentURL = null
var sendData = {}
var extension_loaded_time = Date.now()

function postReport(url, jsonData) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    // sendData.width = jsonData[0].videoWidth
    // sendData.height = jsonData[0].videoHeight
    // sendData.currentTime = jsonData[0].currentTime
    // sendData.extension_loaded_time = extension_loaded_time,
    // sendData.url = currentURL
    // sendData.player = "tiktok"
    // console.log(jsonData)
    // console.log(sendData)
    sendData.width = 5
    sendData.height = 5
    console.log(sendData)
    jsonData = JSON.stringify(sendData)
    if(sendData.width>0){
        xhr.send(jsonData)
    }
}

function onStateChange(event) {
    // this function catch player state changes and report them
    postReport(
        state_change_url,
        {
            video_id_and_cpn: player.getStatsForNerds().video_id_and_cpn,
            fraction: player.getVideoLoadedFraction(),
            current_time: player.getCurrentTime(),
            new_state: event,
        }
    );
}

function onPlaybackQualityChange(event) {
    // this function post quality changes
    postReport(
        quality_change_url,
        {
            video_id_and_cpn: player.getStatsForNerds().video_id_and_cpn,
            fraction: player.getVideoLoadedFraction(),
            current_time: player.getCurrentTime(),
            new_quality: event,
        }
    );
}

function sendStats() {
    postReport(stats_url, player);
}


// wait until player is ready
while (!document.getElementsByTagName("video")) {
    (async () => {
        await new Promise(r => setTimeout(r, 100));
    })();
}

const intervalID = setInterval(function () {
    const data = document.getElementsByTagName("video");
    if (data.length > 0){
        clearInterval(intervalID);
        currentURL = window.location.href;
        player = document.getElementsByTagName("video");
        player[0].addEventListener("waiting", onStateChange);
        player[0].addEventListener("resize", onPlaybackQualityChange);
        setInterval(sendStats, report_time)
    }
}, 250);