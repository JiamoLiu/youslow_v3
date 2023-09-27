"use strict";
/*jshint esversion: 9 */
/* jshint -W097 */

// default url where report server is located
const quality_change_url = "http://localhost:34543/quality";
const state_change_url = "http://localhost:34543/state";
const stats_url = "http://localhost:34543/report";
const report_time = 250;
var currentURL=null;
var player = null;

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
    jsonData.platform = "netflix"
    xhr.send(JSON.stringify(jsonData));
}

function onStateChange(event) {
    // this function catch player state changes and report them
    postReport(
        state_change_url,
        {
            url: currentURL,
            current_time: player.currentTime,
            new_state: event,
        }
    );
}

function onPlaybackQualityChange(event) {
    // this function post quality changes
    postReport(
        quality_change_url,
        {
            url: currentURL,
            current_time: player.currentTime,
            new_quality: event,
        }
    );
}




function sendStats() {
    // For netflix, u need to press ctrl+shift+alt+Q to get that screen


    // this function is executed every X ms and reports current statistics
    let stats_for_nerds = {
        videoHeight : player.videoHeight,
        videoWidth : player.videoWidth,
        current_time: player.currentTime,
        url: currentURL,
    }

    postReport(stats_url, stats_for_nerds);
}

// wait until player is ready
function waitForVideoElement() {
    const intervalId = setInterval(function () {
      const videoElements = document.getElementsByTagName("video");
      if (videoElements.length > 0) {
        clearInterval(intervalId); // Stop the interval once the element is found
        console.log("Video element is now present.");
        // You can now work with the video element(s)
      }
    }, 100); // Check every 100 milliseconds
  }
  

const intervalId = setInterval(function () {
    const videoElements = document.getElementsByTagName("video");
    if (videoElements.length > 0) {
      clearInterval(intervalId); // Stop the interval once the element is found
      console.log("Video element is now present.");
      currentURL = window.location.href;
      // You can now work with the video element(s)
      player = document.getElementsByTagName("video")[0];
      player.addEventListener("waiting", onStateChange);
      player.addEventListener("resize", onPlaybackQualityChange);
      setInterval(sendStats, report_time);
    }
  }, 100); // Check every 100 milliseconds
