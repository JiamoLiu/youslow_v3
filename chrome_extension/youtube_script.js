"use strict";
/*jshint esversion: 9 */
/* jshint -W097 */

// default url where report server is located
const quality_change_url = "http://localhost:34543/quality";
const state_change_url = "http://localhost:34543/state";
const stats_url = "http://localhost:34543/report";
const report_time = 250;
const platform = "youtube"
const extension_loaded_time = Date.now();

function postReport(url, jsonData) {
    // this function sends json data to report server
    // let xhr = new XMLHttpRequest();
    // xhr.open("POST", url, true);
    // xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    // xhr.send(JSON.stringify(jsonData));
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");

    // Define a callback for when the request completes successfully
    // xhr.onload = function () {
    //     if (xhr.status === 200) {
    //         // Successful response
    //         if (successCallback && typeof successCallback === "function") {
    //             successCallback(xhr.responseText);
    //         }
    //     } 
    //     else {
    //     // Error response
    //         if (errorCallback && typeof errorCallback === "function") {
    //             errorCallback(xhr.status, xhr.statusText);
    //         }
    //     }
    // };
    // // Handle network errors
    // xhr.onerror = function () {
    //     if (errorCallback && typeof errorCallback === "function") {
    //         errorCallback(xhr.status, "Network Error");
    //     }
    // };

    // Send the JSON data as the request body
    jsonData.platform = "youtube"
    xhr.send(JSON.stringify(jsonData));
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
    // this function is executed every X ms and reports current statistics
    let stats_for_nerds = player.getStatsForNerds();
    stats_for_nerds.playback_fraction = player.getVideoLoadedFraction();
    stats_for_nerds.current_time = player.getCurrentTime();

    postReport(stats_url, stats_for_nerds);
}

let player= null
const intervalId = setInterval(function () {
    player = document.getElementById("movie_player");
    if (player) {
      clearInterval(intervalId); // Stop the interval once the element is found
      console.log("Video element is now present.");

      player.addEventListener("onStateChange", onStateChange);
      player.addEventListener("onPlaybackQualityChange", onPlaybackQualityChange);

      setInterval(sendStats, report_time);
    }
  }, 100); // Check every 100 milliseconds


