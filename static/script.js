var log = document.getElementById("log");

            setInterval(() => {
                fetch('logpage')
                .then(response => {
                        response.text().then(t => {log.innerHTML = t})
                    });
                }, 500);


$(function() {
          $('a#forwardButton').on('click', function(e) {
            e.preventDefault()
            $.getJSON('/control?command=Forward&value=' + document.getElementById('distance').value,
                function(data) {
              //do nothing
            });
            return false;
          });
          $('a#leftButton').on('click', function(e) {
            e.preventDefault()
            $.getJSON('/control?command=Turn&value=-' + document.getElementById('distance').value,
                function(data) {
              //do nothing
            });
            return false;
          });
          $('a#rightButton').on('click', function(e) {
            e.preventDefault()
            $.getJSON('/control?command=Turn&value=' + document.getElementById('distance').value,
                function(data) {
              //do nothing
            });
            return false;
          });
          $('a#backwardButton').on('click', function(e) {
            e.preventDefault()
            $.getJSON('/control?command=Forward&value=-' + document.getElementById('distance').value,
                function(data) {
              //do nothing
            });
            return false;
          });
        });
