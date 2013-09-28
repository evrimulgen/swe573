
$(document).ready(function() {

    var SERVICE_LOOKUP = {
        "Gol": "gol"
    };
    $("#teamsideselect").on("change", function() {
        $("#teamsidedata").html("changed!" + $(this).val());
    })

})