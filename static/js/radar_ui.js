$(function(){
    var radar = new Radar(window.matchId);
    var timeline = new Timeline({divId: "slider", matchId: window.matchId, sliderCount: 1});

    $(document).on("radarTimeChange", function(event){
        timeline.moveSlider("left", event.minute, event.second);
    });

    $("#slider").on("timeChanged", function(event){
        radar.changeTime(event.time);
    });

    $("#startMatch").click(function(){
        radar.startMatch();
    });

    $("#pauseMatch").click(function(){
        radar.togglePause();
    });

    $(document).on("radarPlayerClick", function(event){
        var playerId = null;

        $.post("/api/GetPlayerCard", JSON.stringify({leagueId: 1, seasonId: 9064, weekId: event.week, playerId: event.player_id})).done(function(data){
            console.log(data.data);
        });
    });
});