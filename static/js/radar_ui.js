$(function(){
    /*
    $.post("/api/GetMatchInfo", JSON.stringify({"matchId": window.matchId})).done(function(data){
        
    });
*/
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
});