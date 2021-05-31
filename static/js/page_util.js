$('#page_id').blur(function () {
    var to_page_index = Number($('#page_id').val());
    var max_page = Number($('#max_page_index').val());
    var min_page = Number($('#min_page_index').val());

    console.log(max_page, min_page, to_page_index);
    if (to_page_index > max_page) {
        $('#page_id').val(max_page);
    } else if (to_page_index < min_page) {
        $('#page_id').val(min_page);
    } else {

    }
})
function page_util(user_url) {

    $('#to_page').click(function () {
        console.log(url)
        var url = user_url + '?page=' + Number($('#page_id').val()) + '&count=' +
            Number($('#to_page').val());
        window.location.replace(url)
    })
    $('#next_page_to').click(function () {
        var page = Number($('#page_id').val());
        if (page + 1 > Number($('#max_page_index').val())) {
            console.log(page)
        } else {
            page += 1;
            var url = user_url + '?page=' + page + '&count=' +
                Number($('#to_page').val());
            window.location.replace(url)
        }
        console.log('to_next_page');
    })
    $('#last_page_to').click(function () {
        var page = Number($('#page_id').val());
        if (page - 1 < Number($('#min_page_index').val())) {
            console.log(page)
        } else {
            page -= 1;
            var url = user_url + '?page=' + page + '&count=' +
                Number($('#to_page').val());
            window.location.replace(url)
        }
    })
}
function get_url_path() {
    var curPath = window.location.href
    var pathNmae = window.location.pathname
    var pos = curPath.indexOf(pathNmae)
    url_path = curPath.substring(0, pos) + pathNmae
    return url_path
}
