$(function(){
    var radar = new Radar(window.matchId);
    var started = false;
    var paused = false;
    var timeline = new Timeline({divId: "slider", matchId: window.matchId, sliderCount: 1});

    $(document).on("radarTimeChange", function(event){
        timeline.moveSlider("left", event.minute, event.second);
        timeline.changeTime(event.minute, event.second);

        var timeString = ''
        if(event.minute < 10){
            timeString += '0';
        }
        timeString += String(event.minute) + ':';
        if(event.second < 10)
            timeString += '0';
        timeString += String(event.second);
        $("#timeDisplay").html(timeString);
    });

    $("#slider").on("timeChanged", function(event){
        radar.changeTime(event.time);
    });

    $("#canvas-play-button").click(function(){
        if(!started){
            radar.startMatch();
            $("#canvas-play-button").hide();
//            $("#pauseMatch i").removeClass("icon-play");
//            $("#pauseMatch i").addClass("icon-pause");
            started = true;
        } else {
//            radar.togglePause();
//            if(paused){
//                paused = false;
//                $("#pauseMatch i").removeClass("icon-play");
//                $("#pauseMatch i").addClass("icon-pause");
//            } else {
//                paused = true;
//                $("#pauseMatch i").removeClass("icon-pause");
//                $("#pauseMatch i").addClass("icon-play");
//            }
        }
    });


    var popCanvasMessage = function(data){
        $(".canvas-message").text(data);
        $("#canvasOverlay").show()
                           .fadeOut(3000);
    };

    $(document).on("radarPlayerClick", function(event){
        $.post("/api/GetPlayerCard", JSON.stringify({leagueId: 1, seasonId: 9064, weekId: event.week, playerId: event.player_id})).done(function(data){
            var info = data.data;
            var $card = (event.homeOrAway==0) ? $("#leftPlayerCard") : $("#rightPlayerCard");

            var imageTag = "<img class='teamLogo' src='/static/images/logo"+info.teamId+".png' />";
            $card.find(".playerName").html(imageTag + info.playerName + " (#"+event.jersey_no+")");
            $card.find(".playerImage").attr("src", "http://sentiotab.blob.core.windows.net/player/"+event.player_id+".png");
            
            var $table = $card.find(".card-table");
            $table.empty();
            $table.append("<tr><th>İstatistik</th><th>Sezon Ortalaması</th><th>Bu Hafta</th></tr>");

            var statNames = {"passes": "Toplam Pas",
                     "shotsOnTarget": "İsabetli",
                     "crosses": "Toplam Orta",
                     "foulsSuffered": "Maruz Kalınan Faul",
                     "totalDistance": "Kat Edilen Mesafe",
                     "yellowCard": "Sarı Kart",
                     "corners": "Korner",
                     "redCard": "Kırmızı Kart",
                     "successfulCross": "İsabetli",
                     "penalty": "Penaltı",
                     "assists": "Asist",
                     "goals": "Gol",
                     "shots": "Şut",
                     "foulsCommitted": "Yapılan Faul",
                     "matchesPlayed": "Oynadığı Maç Sayısı",
                     "successfulPass": "İsabetli",
                     "goalsConceded": "Yediği Gol"}

            console.log(info.statistics);

            var goalkeeperStatistics = new Object();
            goalkeeperStatistics.matchesPlayed = info.statistics.matchesPlayed;
            goalkeeperStatistics.goalsConceded = info.statistics.goalsConceded;
            goalkeeperStatistics.successfulPass = info.statistics.successfulPass;
            goalkeeperStatistics.passes = info.statistics.passes;
            goalkeeperStatistics.yellowCard = info.statistics.yellowCard;
            goalkeeperStatistics.redCard = info.statistics.redCard;

            var flag = 0;
            var statNameHolder;
            var val0Holder;
            var var1Holder;

            _.each(goalkeeperStatistics, function(value, key){

                var statName = statNames[key];
                var val0 = (value[1]%1==0) ? value[1] : value[1].toFixed(2);
                var val1 = (value[0]%1==0) ? value[0] : value[0].toFixed(2);
                if(statName!=null){
                    if(flag == 1){
                        $table.append("<tr><td>"+statNameHolder+" / "+statName+"</td><td>"+val0Holder+" / "+val0+"</td><td>"+var1Holder+" / "+val1+"</td></tr>");
                        flag = 0;
                    }
                    else if(statName === "İsabetli"){
                        statNameHolder = statName;
                        val0Holder = val0;
                        var1Holder = val1;
                        flag = 1;
                    }
                    else{
                        $table.append("<tr><td>"+statName+"</td><td>"+val0+"</td><td>"+val1+"</td></tr>");
                    }
                }

            });
        });
    });
});