/*jshint esversion: 9 */


var currentURL = window.location.href;
//console.log(currentURL);

console.log(currentURL);
if (currentURL.includes("youtu"))
{
    let s = document.createElement('script');
    s.src = chrome.runtime.getURL('youtube_script.js');
    s.onload = function() {
        "use strict";
        this.remove();
    };
    (document.head || document.documentElement).appendChild(s);
}

if (currentURL.includes("netflix"))
{
    let s = document.createElement('script');
    s.src = chrome.runtime.getURL('netflix_script.js');
    s.onload = function() {
        "use strict";
        this.remove();
    };
    (document.head || document.documentElement).appendChild(s);
}


