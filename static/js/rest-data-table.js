
function fillPaginatedTableWithData(tableId, page, sortBy, elemCount, endPoint) {
    let url = window.location.hostname + endPoint + '?page=' + page + '&sortBy=' + sortBy + '&elemCount=' + elemCount;
    console.log(url);
}