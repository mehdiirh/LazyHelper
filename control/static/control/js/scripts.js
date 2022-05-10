$('#sidebarCollapse').on('click', function () {
    $('#sidebar').toggleClass('active');
});

window.alertError = function (text, timeout=2000) {
    let alert = $(".alert-error");
    alert.html(text)
    alert.fadeIn(500)
    setTimeout(function () {
        alert.fadeOut(500)
    }, timeout);
}

window.alertSuccess = function (text, timeout=2000) {
    let alert = $(".alert-success");
    alert.html(text)
    alert.fadeIn(500)
    setTimeout(function () {
        alert.fadeOut(500)
    }, timeout);
}
