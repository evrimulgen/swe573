$(function(){
    var radar = new Radar(window.matchId);
    var started = false;
    var paused = false;
    var timeline = new Timeline({divId: "slider", matchId: window.matchId, sliderCount: 1});

    $(document).on("radarTimeChange", function(event){
        timeline.moveSlider("left", event.minute, event.second);
    });

    $("#slider").on("timeChanged", function(event){
        radar.changeTime(event.time);
    });

    $("#pauseMatch").click(function(){
        if(!started){
            radar.startMatch();
            $("#pauseMatch i").removeClass("icon-play");
            $("#pauseMatch i").addClass("icon-pause");
            started = true;
        } else {
            radar.togglePause();
            if(paused){
                paused = false;
                $("#pauseMatch i").removeClass("icon-play");
                $("#pauseMatch i").addClass("icon-pause");
            } else {
                paused = true;
                $("#pauseMatch i").removeClass("icon-pause");
                $("#pauseMatch i").addClass("icon-play");
            }
        }
    });

    $(document).on("radarPlayerClick", function(event){
        $.post("/api/GetPlayerCard", JSON.stringify({leagueId: 1, seasonId: 9064, weekId: event.week, playerId: event.player_id})).done(function(data){
            var renderedHtml = "<h5><img src='/static/images/logo" + data.data.teamId + ".png' />"
            renderedHtml += data.data.playerName+"</h5>";
            renderedHtml += "<img src='/static/images/players/"+data.data.playerId+".jpg' />";
            renderedHtml += "<ul>";
            _.each(data.data.statistics, function(value, key){
                renderedHtml += "<li>" + key + ": " + JSON.stringify(value) + "</li>";
            });
            renderedHtml += "</ul>";
            console.log(event);
            if(event.homeOrAway==0){
                $("#leftPlayerCard").html(renderedHtml);
                $("#leftPlayerCard").show();
            } else {
                $("#rightPlayerCard").html(renderedHtml);
                $("#rightPlayerCard").show();
            }
        });
    });
});