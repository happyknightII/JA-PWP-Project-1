function loadValues() {
    fetch(window.inputsURL)
        .then(response => {
            response.text().then(text => {
                const t = text.split(" ");
                document.getElementById("hhText").innerHTML = t[0];
                document.getElementById("hlText").innerHTML = t[3];
                $( "#sliderHue" ).slider( "option", "values", [t[3], t[0]] );

                document.getElementById("shText").value = t[1];
                document.getElementById("slText").innerHTML = t[4];
                $( "#sliderSaturation" ).slider( "option", "values", [t[4], t[1]] );

                document.getElementById("vhText").innerHTML = t[2];
                document.getElementById("vlText").innerHTML = t[5];
                $( "#sliderValue" ).slider( "option", "values", [t[5], t[2]] );

                document.getElementById("kpText").innerHTML = t[6];
                $( "#sliderKP" ).slider( "option", "value",  t[6]);

                document.getElementById("kfText").innerHTML = t[7];
                $( "#sliderKF" ).slider( "option", "value",  t[7]);

                document.getElementById("maxTurnText").innerHTML = t[8];
                $( "#sliderMaxTurn" ).slider( "option", "value",  t[8]);

                document.getElementById("offsetText").innerHTML = t[9];
                $( "#sliderOffset" ).slider( "option", "value",  t[9]);

                document.getElementById("speedText").innerHTML = t[10];
                $( "#sliderSpeed" ).slider( "option", "value",  t[10]);
            })
    });
}
$(function() {
    $( "#sliderHue" ).slider({
        range: true,
        min: 0,
        max: 255,
        values: [ 55, 200 ],
        slide: function( event, ui ) {
            document.getElementById("hlText").innerHTML = ui.values[ 0 ];
            document.getElementById("hhText").innerHTML = ui.values[ 1 ];
            fetch(window.parametersURL + "?hl=" + ui.values[ 0 ] + "&hh=" + ui.values[ 1 ])
        }
    });
    $( "#sliderSaturation" ).slider({
        range: true,
        min: 0,
        max: 255,
        values: [ 55, 200 ],
        slide: function( event, ui ) {
            document.getElementById("slText").innerHTML = ui.values[ 0 ];
            document.getElementById("shText").innerHTML = ui.values[ 1 ];
            fetch(window.parametersURL + "?sl=" + ui.values[ 0 ] + "&sh=" + ui.values[ 1 ])
        }
    });
    $( "#sliderValue" ).slider({
        range: true,
        min: 0,
        max: 255,
        values: [ 55, 200 ],
        slide: function( event, ui ) {
            document.getElementById("vlText").innerHTML = ui.values[ 0 ];
            document.getElementById("vhText").innerHTML = ui.values[ 1 ];
            fetch(window.parametersURL + "?vl=" + ui.values[ 0 ] + "&vh=" + ui.values[ 1 ])
        }
    });
    $( "#sliderKP" ).slider({
        orientation: "horizontal",
        min: -0.5,
        max: 0.5,
        step: 0.001,
        values: 0.25,
        slide: function( event, ui ) {
            document.getElementById("kpText").innerHTML = ui.value;
            fetch(window.parametersURL + "?kp=" + ui.value)
        }
    });
    $( "#sliderKF" ).slider({
        orientation: "horizontal",
        min: -20,
        max: 20,
        step: 0.1,
        value: 0,
        slide: function( event, ui ) {
            document.getElementById("kfText").innerHTML = ui.value;
            fetch(window.parametersURL + "?kf=" + ui.value)
        }
    });
    $( "#sliderMaxTurn" ).slider({
        orientation: "horizontal",
        min: -50,
        max: 50,
        step: 1,
        value: 0,
        slide: function( event, ui ) {
            document.getElementById("maxTurnText").innerHTML = ui.value;
            fetch(window.parametersURL + "?maxTurn=" + ui.value)
        }
    });
    $( "#sliderOffset" ).slider({
        orientation: "horizontal",
        min: -200,
        max: 200,
        step: 1,
        value: 0,
        slide: function( event, ui ) {
            document.getElementById("offsetText").innerHTML = ui.value;
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
            document.getElementById("speedText").innerHTML = ui.value;
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
});
