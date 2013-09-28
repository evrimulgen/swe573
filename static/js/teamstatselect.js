
$(document).ready(function() {

    $("#teamsideselect").on("change", function() {
        $.ajax("/ns/partial_teamstats/",{
                type: "POST",
                data: JSON.stringify({"stat":  $("#teamsideselect option:selected").data("option")}),
                success: function(d){
                    $("#teamsidedata").html(d);
                }
            });
    })

})