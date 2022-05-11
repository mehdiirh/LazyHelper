$('#sidebarCollapse').on('click', function () {
    $('#sidebar').toggleClass('active');
});

$("#sidebar button").on("click", () => {
    console.log("clicked on button")
    $("#sidebar").addClass("active")
})

$('button[name="command"]').on("click", (e) => {
    e.preventDefault();
    send_command($(e.target).val());
})

window.alertError = function (text, timeout=1000) {
    let alert = $(".alert-error");
    alert.html(text)
    alert.fadeIn(500)
    setTimeout(function () {
        alert.fadeOut(500)
    }, timeout);
}

window.alertSuccess = function (text, timeout=1000) {
    let alert = $(".alert-success");
    alert.html(text)
    alert.fadeIn(500)
    setTimeout(function () {
        alert.fadeOut(500)
    }, timeout);
}


function send_command(code) {
    $("button[name='command']").prop("disabled", true)
    $("#div-output").css('display', 'none')

    let form = $("#command-form")
    let data = form.serializeArray()
    data.push({'name': 'command', 'value': code})

    $.ajax({
        url: form.attr("action"),
        method: form.attr("method"),
        data: data,
        async: true
    }).then((response) => {
        if (response['meta']['status'] === 'ok') {
            alertSuccess("Success !")

            if (response['data'] && response['data']['output']) {
                $("#div-output").css('display', 'block')
                $("#output").text(response['data']['output']);
            }
        } else {
            alertError('An error occurred')
        }

        $("button[name='command']").prop("disabled", false)
    })
}
