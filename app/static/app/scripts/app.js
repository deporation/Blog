function encodeSearchParams(obj) {
    const params = []

    Object.keys(obj).forEach((key) => {
        let value = obj[key]
        if (typeof value === 'undefined') {
            value = ''
        }
        params.push([key, encodeURIComponent(value)].join('='))
    })

    return params.join('&')
}

$("#add").click(function () {
    let id = $(this).data('appid') - 1;
    alert(id)
    const obj = {
        article_id: id,
        content: $("#content").val(),

    }
    console.log(encodeSearchParams(obj));
    const finalUrl = "detail/addDis?" + encodeSearchParams(obj)
    $.ajax({
        url: finalUrl,
        type: "post",
        contentType: "application/json;charset=UTF-8",
        dataType: "text",
        success: function (data) {
            window.location.href = 'detail/' + id;
        }
    })
})