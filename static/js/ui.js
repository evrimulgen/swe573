$(function () {
    var cb = new Chalkboard("chalkboardContainer", 85);
    $("#timeSlider").slider({min: 0, max: 90, value:[0,90], step: 5});

    var awayPlayers = [
        {id: 654, name: 'Hamit Altintop', team_id: 5, jersey_number: 4},
        {id: 181, name: 'Selcuk Inan ', team_id: 5, jersey_number: 8},
        {id: 986, name: 'Wesley Sneijder', team_id: 5, jersey_number: 14},
        {id: 1000, name: 'Didier Drogba', team_id: 5, jersey_number: 12},
        {id: 153, name: 'Aydin Yilmaz ', team_id: 5, jersey_number: 7},
        {id: 617, name: 'Burak Yilmaz', team_id: 5, jersey_number: 17},
        {id: 162, name: 'Emmanuel Eboue ', team_id: 5, jersey_number: 27},
        {id: 163, name: 'Emre Colak ', team_id: 5, jersey_number: 52},
        {id: 164, name: 'Engin Baytar ', team_id: 5, jersey_number: 50},
        {id: 186, name: 'Ufuk Ceylan ', team_id: 5, jersey_number: 86},
        {id: 178, name: 'Nestor Fernando Muslera ', team_id: 5, jersey_number: 25},
        {id: 168, name: 'Gokhan Zan ', team_id: 5, jersey_number: 5},
        {id: 169, name: 'Hakan Kadir Balta ', team_id: 5, jersey_number: 22},
        {id: 171, name: 'Johan Erik Calvin Elmander ', team_id: 5, jersey_number: 9},
        {id: 167, name: 'Felipe Melo de Carvalho ', team_id: 5, jersey_number: 10},
        {id: 781, name: 'Nordin Amrabat', team_id: 5, jersey_number: 53},
        {id: 655, name: 'Dany Achille Nounkeu Tchounkeu', team_id: 5, jersey_number: 13},
        {id: 180, name: 'Sabri Sarioglu ', team_id: 5, jersey_number: 55},
        {id: 152, name: 'Albert Riera Ortega ', team_id: 5, jersey_number: 11},
        {id: 182, name: 'Semih Kaya ', team_id: 5, jersey_number: 26},
        {id: 188, name: 'Yekta Kurtulus ', team_id: 5, jersey_number: 35},
        {id: 688, name: 'Umut Bulut', team_id: 5, jersey_number: 19} 
    ];

    var homePlayers = [
        { team_id: 4, jersey_number: 1, id: 151, name: "Volkan Demirel" },
        { team_id: 4, jersey_number: 2, id: 6, name: "Egemen Korkmaz" },
        { team_id: 4, jersey_number: 3, id: 340, name: "Hasan Ali Kaldirim" },
        { team_id: 4, jersey_number: 4, id: 121, name: "Bekir Irtegun" },
        { team_id: 4, jersey_number: 5, id: 684, name: "Mehmet Topal" },
        { team_id: 4, jersey_number: 6, id: 135, name: "Yobo " },
        { team_id: 4, jersey_number: 7, id: 139, name: "Moussa Sow" },
        { team_id: 4, jersey_number: 9, id: 138, name: "Miroslav Stoch" },
        { team_id: 4, jersey_number: 11, id: 677, name: "Dirk Kuyt" },
        { team_id: 4, jersey_number: 14, id: 784, name: "Raul Meireles" },
        { team_id: 4, jersey_number: 16, id: 119, name: "Cristian Baroni" },
        { team_id: 4, jersey_number: 17, id: 144, name: "Recep Niyaz" },
        { team_id: 4, jersey_number: 20, id: 150, name: "Sezer Ozturk" },
        { team_id: 4, jersey_number: 21, id: 146, name: "Selcuk Sahin" },
        { team_id: 4, jersey_number: 23, id: 147, name: "Semih Senturk" },
        { team_id: 4, jersey_number: 27, id: 678, name: "Milos Krasic" },
        { team_id: 4, jersey_number: 34, id: 128, name: "Mert Gunok" },
        { team_id: 4, jersey_number: 38, id: 137, name: "Mehmet Topuz" },
        { team_id: 4, jersey_number: 48, id: 679, name: "Salih Ucan" },
        { team_id: 4, jersey_number: 53, id: 148, name: "Serdar Kesimal" },
        { team_id: 4, jersey_number: 54, id: 126, name: "Erten Ersu" },
        { team_id: 4, jersey_number: 67, id: 141, name: "Orhan Sam" },
        { team_id: 4, jersey_number: 77, id: 130, name: "Gokhan Gonul" },
        { team_id: 4, jersey_number: 85, id: 149, name: "Serkan Kirintili" },
        { team_id: 4, jersey_number: 88, id: 124, name: "Caner Erkin" },
        { team_id: 4, jersey_number: 99, id: 783, name: "Berk Elitez" }
    ];


    // for dynamically creating elements and binding events to them:
    // $("<p>xdxd</p>").click(function(){ alert("xd"); }).appendTo("#header");
    var homeList = $("#homeTeamJersey");
    _.each(homePlayers, function(player){
        $("<li>"+player.jersey_number+" "+player.name+"</li>").click(function(){
            $(".teamlist li.active").removeClass("active");
            $(this).addClass("active");
            cb.changePlayer(player);
        }).appendTo(homeList);
    });

    var awayList = $("#awayTeamJersey");
    _.each(awayPlayers, function(player){
        $("<li>"+player.jersey_number+" "+player.name+"</li>").click(function(){
            $(".teamlist li.active").removeClass("active");
            $(this).addClass("active");
            cb.changePlayer(player);
        }).appendTo(awayList);
    });
    

    $("#shots").click(function () {
        if (!$(this).hasClass("active")) {
            cb.activateLayer("shots");
        } else {
            cb.deactivateLayer("shots")
        }
    });

    $("#passes").click(function () {
        if (!$(this).hasClass("active")) {
            cb.activateLayer("passes");
        } else {
            cb.deactivateLayer("passes");
        }
    });

    $("#heatmap").click(function () {
        if (!$(this).hasClass("active")) {
            cb.activateLayer("heatmap");
        } else {
            cb.deactivateLayer("heatmap");
        }
    });

    $("#runpaths").click(function () {
        if (!$(this).hasClass("active")) {
            cb.activateLayer("runpaths");
        } else {
            cb.deactivateLayer("runpaths");
        }
    });

    $("#timeSlider").on("slideStop", function(){
        var vals = this.value.split(",");
        cb.applyTimeFilter(parseInt(vals[0]), parseInt(vals[1]));
    });
});

