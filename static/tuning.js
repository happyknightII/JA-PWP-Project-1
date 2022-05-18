var log = document.getElementById("log");

setInterval(() => {
    fetch(window.logPageURL)
        .then(response => {
            response.text().then(t => {log.innerHTML = t})
        });
}, 500);

// Update the current slider value (each time you drag the slider handle)
document.getElementById("hh").oninput = function() {
  document.getElementById("hhText").innerHTML = this.value;
  $.getJSON('/thresholdparameters?hh=' + document.getElementById('hh').value, function(data) {});
}
document.getElementById("sh").oninput = function() {
  document.getElementById("shText").innerHTML = this.value;
  $.getJSON('/thresholdparameters?sh=' + document.getElementById('sh').value, function(data) {});
}
document.getElementById("vh").oninput = function() {
  document.getElementById("vhText").innerHTML = this.value;
  $.getJSON('/thresholdparameters?vh=' + document.getElementById('vh').value, function(data) {});
}
document.getElementById("hl").oninput = function() {
  document.getElementById("hlText").innerHTML = this.value;
  $.getJSON('/thresholdparameters?hl=' + document.getElementById('hl').value, function(data) {});
}
document.getElementById("sl").oninput = function() {
  document.getElementById("slText").innerHTML = this.value;
  $.getJSON('/thresholdparameters?sl=' + document.getElementById('sl').value, function(data) {});
}
document.getElementById("vl").oninput = function() {
  document.getElementById("vlText").innerHTML = this.value;
  $.getJSON('/thresholdparameters?vl=' + document.getElementById('vl').value, function(data) {});
}

function load() {

    fetch(window.hsvFilterURL)
        .then(response => {
            response.text().then(text => {
                const t = text.split(" ");
                document.getElementById("hhText").innerHTML = t[0];
                document.getElementById("hh").value = t[0];
                document.getElementById("shText").innerHTML = t[1];
                document.getElementById("sh").value = t[1];
                document.getElementById("vhText").innerHTML = t[2];
                document.getElementById("vh").value = t[2];
                document.getElementById("hlText").innerHTML = t[3];
                document.getElementById("hl").value = t[3];
                document.getElementById("slText").innerHTML = t[4];
                document.getElementById("sl").value = t[4];
                document.getElementById("vlText").innerHTML = t[5];
                document.getElementById("vl").value = t[5];
            })
        });
}
