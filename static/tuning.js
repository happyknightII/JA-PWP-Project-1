function loadValues() {
    fetch(window.inputsURL)
        .then(response => {
            response.text().then(text => {
                const t = text.split(" ");
                document.getElementById("hhText").value = t[0];
                document.getElementById("hlText").value = t[3];
                $( "#sliderHue" ).slider( "option", "values", [t[3], t[0]] );

                document.getElementById("shText").value = t[1];
                document.getElementById("slText").value = t[4];
                $( "#sliderSaturation" ).slider( "option", "values", [t[4], t[1]] );

                document.getElementById("vhText").value = t[2];
                document.getElementById("vlText").value = t[5];
                $( "#sliderValue" ).slider( "option", "values", [t[5], t[2]] );

                document.getElementById("kpText").value = t[6];
                $( "#sliderKP" ).slider( "option", "value",  t[6]);

                document.getElementById("kfText").value = t[7];
                $( "#sliderKF" ).slider( "option", "value",  t[7]);

                document.getElementById("maxTurnText").value = t[8];
                $( "#sliderMaxTurn" ).slider( "option", "value",  t[8]);

                document.getElementById("offsetText").value = t[9];
                $( "#sliderOffset" ).slider( "option", "value",  t[9]);

                document.getElementById("speedText").value = t[10];
                $( "#sliderSpeed" ).slider( "option", "value",  t[10]);
            })
    });
}
$(document).ready(function() {
    $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
    $( "#sliderHue" ).slider({
        range: true,
        min: 0,
        max: 255,
        values: [ 55, 200 ],
        slide: function( event, ui ) {
            document.getElementById("hlText").value = ui.values[ 0 ];
            document.getElementById("hhText").value = ui.values[ 1 ];
            fetch(window.parametersURL + "?hl=" + ui.values[ 0 ] + "&hh=" + ui.values[ 1 ])
        }
    });
    $( "#sliderSaturation" ).slider({
        range: true,
        min: 0,
        max: 255,
        values: [ 55, 200 ],
        slide: function( event, ui ) {
            document.getElementById("slText").value = ui.values[ 0 ];
            document.getElementById("shText").value = ui.values[ 1 ];
            fetch(window.parametersURL + "?sl=" + ui.values[ 0 ] + "&sh=" + ui.values[ 1 ])
        }
    });
    $( "#sliderValue" ).slider({
        range: true,
        min: 0,
        max: 255,
        values: [ 55, 200 ],
        slide: function( event, ui ) {
            document.getElementById("vlText").value = ui.values[ 0 ];
            document.getElementById("vhText").value = ui.values[ 1 ];
            fetch(window.parametersURL + "?vl=" + ui.values[ 0 ] + "&vh=" + ui.values[ 1 ])
        }
    });
    $( "#sliderKP" ).slider({
        orientation: "horizontal",
        min: 0,
        max: 0.5,
        step: 0.001,
        values: 0.25,
        slide: function( event, ui ) {
            document.getElementById("kpText").value = ui.value;
            fetch(window.parametersURL + "?kp=" + ui.value)
        }
    });
    $( "#sliderKF" ).slider({
        orientation: "horizontal",
        min: 0,
        max: 20,
        step: 0.1,
        value: 0,
        slide: function( event, ui ) {
            document.getElementById("kfText").value = ui.value;
            fetch(window.parametersURL + "?kf=" + ui.value)
        }
    });
    $( "#sliderMaxTurn" ).slider({
        orientation: "horizontal",
        min: 0,
        max: 50,
        step: 1,
        value: 0,
        slide: function( event, ui ) {
            document.getElementById("maxTurnText").value = ui.value;
            fetch(window.parametersURL + "?maxTurn=" + ui.value)
        }
    });
    $( "#sliderOffset" ).slider({
        orientation: "horizontal",
        min: 0,
        max: 1,
        step: 0.01,
        value: 0,
        slide: function( event, ui ) {
            document.getElementById("offsetText").value = ui.value;
            fetch(window.parametersURL + "?offset=" + ui.value)
        }
    });
    $( "#sliderSpeed" ).slider({
        orientation: "horizontal",
        min: 0,
        max: 70,
        step: 1,
        value: 0,
        slide: function( event, ui ) {
            document.getElementById("speedText").value = ui.value;
            fetch(window.parametersURL + "?speed=" + ui.value)
        }
    });
    $('a#resetButton').on('click', function(e) {
        e.preventDefault();
        fetch(window.resetURL);
        loadValues();
        return false;
    });
    $('a#saveButton').on('click', function(e) {
        e.preventDefault();
        fetch(window.saveURL);
        return false;
    });
    $("#hlText").change(function() {
        $("#sliderHue").slider("option", "values", [this.value, $("#sliderHue").slider("option", "values")[1]]);
        fetch(window.parametersURL + "?hl=" + this.value)
    });
    $("#hhText").change(function() {
        $("#sliderHue").slider("option", "values", [$("#sliderHue").slider("option", "values")[0], this.value]);
        fetch(window.parametersURL + "?hh=" + this.value)
    });
    $("#slText").change(function() {
        $("#sliderSaturation").slider("option", "values", [this.value, $("#sliderSaturation").slider("option", "values")[1]]);
        fetch(window.parametersURL + "?sl=" + this.value)
    });
    $("#shText").change(function() {
        $("#sliderSaturation").slider("option", "values", [$("#sliderSaturation").slider("option", "values")[0], this.value]);
        fetch(window.parametersURL + "?sh=" + this.value)
    });
    $("#vlText").change(function() {
        $("#sliderValue").slider("option", "values", [this.value, $("#sliderValue").slider("option", "values")[1]]);
        fetch(window.parametersURL + "?vl=" + this.value)
    });
    $("#vhText").change(function() {
        $("#sliderValue").slider("option", "values", [$("#sliderValue").slider("option", "values")[0], this.value]);
        fetch(window.parametersURL + "?vh=" + this.value)
    });
    $("#kpText").change(function() {
        $("#sliderKP").slider("option", "value", this.value);
        fetch(window.parametersURL + "?kp=" + this.value)
    });
    $("#kfText").change(function() {
        $("#sliderKF").slider("option", "value", this.value);
        fetch(window.parametersURL + "?kf=" + this.value)
    });
    $("#maxTurnText").change(function() {
        $("#sliderMaxTurn").slider("option", "value", this.value);
        fetch(window.parametersURL + "?maxTurn=" + this.value)
    });
    $("#offsetText").change(function() {
        $("#sliderOffset").slider("option", "value", this.value);
        fetch(window.parametersURL + "?offset=" + this.value)
    });
    $("#speedText").change(function() {
        $("#sliderSpeed").slider("option", "value", this.value);
        fetch(window.parametersURL + "?speed=" + this.value)
    });
});
