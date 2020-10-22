const URL = "/api/";

/**
 * Requests from the main server's REST API a list of specified entities, and then after receiving a response,
 * executes the passed function and passes the received list into it.
 * @param entityType name of the entity to retrieve.
 * @param finishingFunction function that is executed after a response is received. It should take one
 *  parameter - an array of specified entity objects.
 */
function requestList(entityType, finishingFunction) {
    let finalUrl = URL + entityType + '/list';
    let request = new XMLHttpRequest();
    request.open('GET', finalUrl, true);
    request.onreadystatechange = function () {
        let deviceArr = null;
        if (this.readyState === XMLHttpRequest.DONE) {
            if (this.status === 200)
                deviceArr = JSON.parse(this.responseText);
            finishingFunction(deviceArr);
        }
    };

    request.send(null);
}

/**
 * Requests a registration of an entity in the main's server database via the REST API.
 * @param entityType type of the entity that is to be created.
 * @param entity new entity object.
 * @param csrftoken csrf token of the logged in user.
 * @param finishingFunction function that is executed after a response is receieved. It should take one parameter - a
 * bool value which signifies a success or failure of the registration.
 */
function requestCreate(entityType, entity, csrftoken, finishingFunction) {
    let finalUrl = URL + entityType + '/create';
    let request = new XMLHttpRequest();
    request.open('POST', finalUrl, true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.onreadystatechange = function () {
        let result = false;
        if (this.readyState === XMLHttpRequest.DONE && this.status === 201)
            result = true;

        finishingFunction(result);
    };
    request.send(JSON.stringify(entity));
}

/**
 * Requests a deletion of an entity with the passed id in the main's server database via the REST API.
 * @param entityType type of the entity that is to be deleted.
 * @param id id of the object.
 * @param csrftoken csrf token of the logged in user.
 * @param finishingFunction function that is executed after a response is receieved. It should take one parameter - a
 * bool value which signifies a success or failure of the deletion.
 */
function requestDelete(entityType, id, csrftoken, finishingFunction) {
    let finalUrl = URL + entityType + '/delete/' + id;
    let request = new XMLHttpRequest();
    request.open('POST', finalUrl, true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.onreadystatechange = function () {
        let result = false;
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200)
            result = true;

        finishingFunction(result);
    }

    request.send();

}