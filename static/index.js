var log = document.getElementById("log");

            setInterval(() => {
                fetch('logpage')
                .then(response => {
                        response.text().then(t => {log.innerHTML = t})
                    });
                }, 500);


$(function() {
    $('a#autonomousButton').on('click', function(e) {
    e.preventDefault()
    $.getJSON('/control?mode=True',
        function(data) {});
    return false;
    });
    $('a#manualButton').on('click', function(e) {
    e.preventDefault()
    $.getJSON('/control?mode=False',
        function(data) {});
    return false;
    });
    $('a#forwardButton').on('click', function(e) {
    e.preventDefault()
    $.getJSON('/control?command=Forward&value=' + document.getElementById('distance').value,
        function(data) {});
    return false;
    });
    $('a#leftButton').on('click', function(e) {
    e.preventDefault()
    $.getJSON('/control?command=Turn&value=-' + document.getElementById('distance').value,
        function(data) {});
    return false;
    });
    $('a#rightButton').on('click', function(e) {
    e.preventDefault()
    $.getJSON('/control?command=Turn&value=' + document.getElementById('distance').value,
        function(data) {});
    return false;
    });
    $('a#backwardButton').on('click', function(e) {
    e.preventDefault()
    $.getJSON('/control?command=Forward&value=-' + document.getElementById('distance').value,
        function(data) {});
    return false;
    });
});
