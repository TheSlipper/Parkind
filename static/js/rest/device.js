const URL = "/api/";

/**
 * Sends a REST API request to the main server with the data of the device that is to be registered. If the passed
 * finishingFunction is not null it will invoke it and pass the result of the operation into it for further handling.
 * @param device data on the device that is to be registered
 * @param finishingFunction function that is executed after the request receives a response. It should take one
 *  parameter - a boolean value representing the result of the request.
 */
function deviceCreate(device, token, finishingFunction) {
    // TODO: Test this
    let request = new XMLHttpRequest();
    request.open('POST', URL + 'device/create/' + token + '/', true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.onreadystatechange = function () {
        let result = false;
        if (this.readyState === XMLHttpRequest.DONE && this.status === 201) {
            result = true;
        }

        // if (finishingFunction != null)
        finishingFunction(result);
    };
    request.send(JSON.stringify(device));
}

/**
 * Sends a REST API request to the main server, parses the text into an object and passes it to the
 * received function for further handling.
 * @param id id of the device entity.
 * @param finishingFunction function that is executed after the request receives a response. It should take one
 *  parameter - a single device object.
 */
function deviceDetail(id, finishingFunction) {
    let request = new XMLHttpRequest();
    request.open('GET', URL+'device/detail/'+id, true);
    request.onreadystatechange = function () {
        let device = null;
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            device = JSON.parse(this.responseText);
        }

        finishingFunction(device);
    };

    request.send(null);
}

/**
 * Sends a REST API request to the main server, parses the text into an array of objects and passes it to the
 * received function for further handling.
 * @param finishingFunction function that is executed after the request receives a response. It should take one
 *  parameter - an array of device objects.
 */
function deviceList(finishingFunction) {
    let request = new XMLHttpRequest();
    request.open('GET', URL+'device/list', true);
    request.onreadystatechange = function () {
        let deviceArr = null;
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            deviceArr = JSON.parse(this.responseText);
        }

        finishingFunction(deviceArr);
    };

    request.send(null);
}

function deviceUpdate(device) {

}

function deviceDelete() {

}