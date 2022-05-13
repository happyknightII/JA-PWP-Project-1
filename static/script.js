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
          $('a#threshold').on('click', function(e) {
            e.preventDefault()
            $.getJSON('/thresholdparameters?hh='
            + document.getElementById('hh').value
            + '&vh='
            + document.getElementById('vh').value
            + '&sh='
            + document.getElementById('sh').value
            + '&hl='
            + document.getElementById('hl').value
            + '&vl='
            + document.getElementById('vl').value
            + '&sl='
            + document.getElementById('sl').value,
                function(data) {});
            return false;
          });
        });
