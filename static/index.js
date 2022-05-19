var log = document.getElementById("log");

            setInterval(() => {
                fetch('logpage')
                .then(response => {
                        response.text().then(t => {log.innerHTML = t})
                    });
                }, 1000);


$(function() {
    $('a#autonomousButton').on('click', function(e) {
        e.preventDefault()
        fetch('/control?mode=True');
        return false;
    });
    $('a#manualButton').on('click', function(e) {
        e.preventDefault()
        fetch('/control?mode=False');
        return false;
    });
    $('a#forwardButton').on('click', function(e) {
        e.preventDefault()
        fetch('/control?command=Forward&value=' + document.getElementById('distance').value);
        return false;
    });
    $('a#leftButton').on('click', function(e) {
        e.preventDefault()
        fetch'/control?command=Turn&value=-' + document.getElementById('distance').value);
        return false;
    });
    $('a#rightButton').on('click', function(e) {
        e.preventDefault()
        fetch('/control?command=Turn&value=' + document.getElementById('distance').value);
        return false;
    });
    $('a#backwardButton').on('click', function(e) {
        e.preventDefault()
        fetch('/control?command=Forward&value=-' + document.getElementById('distance').value)
        return false;
    });
});
