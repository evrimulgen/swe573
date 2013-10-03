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

    $("#popMessage").click(function(){
       radar.popMessage('caner');
    });

    $(document).on("radarPlayerClick", function(event){
        $.post("/api/GetPlayerCard", JSON.stringify({leagueId: 1, seasonId: 9064, weekId: event.week, playerId: event.player_id})).done(function(data){
            var info = data.data;
            var $card = (event.homeOrAway==0) ? $("#leftPlayerCard") : $("#rightPlayerCard");

            var imageTag = "<img class='teamLogo' src='/static/images/logo"+info.teamId+".png' />";
            $card.find(".playerName").html(imageTag + info.playerName + " (#"+event.jersey_no+")");
            $card.find(".playerImage").attr("src", "/static/images/players/"+event.player_id+".jpg");
            
            var $table = $card.find(".card-table");
            $table.empty();
            $table.append("<tr><th>İstatistik</th><th>Bu Sezon</th><th>Bu Hafta</th></tr>");

            var statNames = {"passes": "Toplam Pas",
                     "shotsOnTarget": "İsabetli Şut",
                     "crosses": "Toplam Orta",
                     "foulsSuffered": "Maruz Kalınan Faul",
                     "totalDistance": "Kat Edilen Mesafe",
                     "yellowCard": "Sarı Kart",
                     "corners": "Korner",
                     "redCard": "Kırmızı Kart",
                     "successfulCross": "İsabetli Orta",
                     "penalty": "Penaltı",
                     "assists": "Asist",
                     "goals": "Gol",
                     "shots": "Şut",
                     "foulsCommitted": "Yapılan Faul",
                     "matchesPlayed": "Oynadığı Maç Sayısı",
                     "successfulPass": "İsabetli Pas"};
            _.each(info.statistics, function(value, key){
                var statName = statNames[key];

                var val0 = (value[0]%1==0) ? value[0] : value[0].toFixed(2);
                var val1 = (value[1]%1==0) ? value[1] : value[1].toFixed(2);

                $table.append("<tr><td>"+statName+"</td><td>"+val0+"</td><td>"+val1+"</td></tr>");
            });
        });
    });
});