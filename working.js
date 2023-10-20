function testReport(url, jsonData) {
    // this function sends json data to report server
    // let xhr = new XMLHttpRequest();
    // xhr.open("POST", url, true);
    // xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    // xhr.send(JSON.stringify(jsonData));
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");

    xhr.onload = function () {
        if (xhr.status === 200) {
            // Successful response
            // if (successCallback && typeof successCallback === "function") {
            //     successCallback(xhr.responseText);
            // }
        } 
        else {
        // Error response
            if (errorCallback && typeof errorCallback === "function") {
                errorCallback(xhr.status, xhr.statusText);
            }
        }
    };
    // Handle network errors
    xhr.onerror = function () {
        if (errorCallback && typeof errorCallback === "function") {
            errorCallback(xhr.status, "Network Error");
        }
    };

    // Send the JSON data as the request body
    xhr.send("PLEASEEEEE");    
}