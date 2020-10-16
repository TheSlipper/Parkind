const URL = "/api/";

/**
 * Requests from the main server's REST API a list of specified entities, and then after receiving a response,
 * executes the passed function and passes the received list into it.
 * @param entityType name of the entity to retrieve.
 * @param finishingFunction function that is executed after a response is received. It should take one
 *  parameter - an array of specified entity objects.
 */
function requestList(entityType, finishingFunction) {
    let request = new XMLHttpRequest();
    request.open('GET', URL + entityType + '/list', true);
    request.onreadystatechange = function () {
        let deviceArr = null;
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            deviceArr = JSON.parse(this.responseText);
        }

        finishingFunction(deviceArr);
    };

    request.send(null);
}