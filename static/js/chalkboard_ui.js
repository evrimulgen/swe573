$(function () {
    var timelineScope = new paper.PaperScope();
    var tl = new Timeline({divId: "slider", "matchId": window.matchId, sliderCount: 2, paperScope: timelineScope});

    var cb = new Chalkboard("chalkboardContainer", window.matchId);

    //$("#timeSlider").slider({min: 0, max: 90, value:[0,90], step: 5});

    var homeTeam = {};
    var awayTeam = {};

    $.post("/api/GetMatchInfo", JSON.stringify({"matchId": window.matchId})).done(function(data){
        var res = data.data[0];
        homeTeam.name = res[3];
        awayTeam.name = res[4];
        homeTeam.id = res[5];
        awayTeam.id = res[6];

        $.post("/api/GetMatchSquad", JSON.stringify({"matchId": window.matchId})).done(function(data){
            homeTeam.players = [];
            awayTeam.players = [];

            var res = data.data;

            _.each(res, function(x){
                var info = x.data;

                var player = {id: info[5], name: info[0], jersey_number: info[1], team_id: info[3], position_id: info[4]};
                if(info[16]==1){
                    if(info[3]==homeTeam.id){
                        homeTeam.players.push(player);
                    } else if(info[3]==awayTeam.id){
                        awayTeam.players.push(player);
                    } else {
                        console.log("player belongs to neither home nor away team");
                        console.log(info);
                    } 
                }
            });

            homeTeam.players = _.sortBy(homeTeam.players, "position_id");
            awayTeam.players = _.sortBy(awayTeam.players, "position_id");

            // for dynamically creating elements and binding events to them:
            // $("<p>xdxd</p>").click(function(){ alert("xd"); }).appendTo("#header");

            $(".teamlist-container .homeTeamName").html(homeTeam.name);
            $(".teamlist-container .awayTeamName").html(awayTeam.name);
            var homeList = $("#homeTeamJersey");
            _.each(homeTeam.players, function(player){
                $("<li><input type='radio' id='player.name' name='player.name' value='player.jersey_number'/>"+"&nbsp "+player.jersey_number+" "+player.name+"</li>").click(function(){
                    $(".teamlist li.active").removeClass("active");
                    $(this).addClass("active");
                    cb.changePlayer(player);
                }).appendTo(homeList);
            });

            var awayList = $("#awayTeamJersey");
            _.each(awayTeam.players, function(player){
                $("<li><input type='radio' name='player.name' value='player.jersey_number'/>"+"&nbsp "+player.jersey_number+" "+player.name+"</li>").click(function(){
                    $(".teamlist li.active").removeClass("active");
                    $(this).addClass("active");
                    cb.changePlayer(player);
                }).appendTo(awayList);
            });
        });
    }); 

    $("#shots").click(function () {
        if (this.checked) {
            cb.activateLayer("shots");
            $("input[id=runpaths]:checked").removeAttr("checked");
            $("input[id=passes]:checked").removeAttr("checked");
            $("input[id=heatmap]:checked").removeAttr("checked");
            cb.deactivateLayer("heatmap");
            cb.deactivateLayer("runpaths");
            cb.deactivateLayer("passes");
        } else {
            cb.deactivateLayer("shots")
        }
    });

    $("#passes").click(function () {
        if (this.checked) {
            cb.activateLayer("passes");
            cb.activateLayer("shots");
            $("input[id=runpaths]:checked").removeAttr("checked");
            $("input[id=shots]:checked").removeAttr("checked");
            $("input[id=heatmap]:checked").removeAttr("checked");
            cb.deactivateLayer("heatmap");
            cb.deactivateLayer("shots");
            cb.deactivateLayer("runpaths");
        } else {
            cb.deactivateLayer("passes");
        }
    });

    $("#heatmap").click(function () {
        if (this.checked) {
            cb.activateLayer("heatmap");
            cb.activateLayer("shots");
            $("input[id=runpaths]:checked").removeAttr("checked");
            $("input[id=shots]:checked").removeAttr("checked");
            $("input[id=passes]:checked").removeAttr("checked");
            cb.deactivateLayer("runpaths");
            cb.deactivateLayer("shots");
            cb.deactivateLayer("passes");
        }else {
            $(this).attr("checked", "");
            cb.deactivateLayer("heatmap");
        }
    });

    $("#runpaths").click(function () {
        if (this.checked) {
            cb.activateLayer("runpaths");
            $("input[id=passes]:checked").removeAttr("checked");
            $("input[id=shots]:checked").removeAttr("checked");
            $("input[id=heatmap]:checked").removeAttr("checked");
            cb.deactivateLayer("heatmap");
            cb.deactivateLayer("shots");
            cb.deactivateLayer("passes");
        } else {
            cb.deactivateLayer("runpaths");
        }
    });

    $("#slider").on("timeChanged", function(event){
        cb.applyTimeFilter(event.time[0][0], event.time[1][0]);
    });
});

