
$(function() {

    var $gallery = $( "#gallery" );//takım logolarının durduğu kısım
    var $player_img = $( "#player_img" );//carousel de player img ların durduğu kısım

    var $trash_left = $("#trash_left");//soldaki trash, buraya player imageları getirip bırakıcaz.
    var $trash_right = $("#trash_right");//sağdaki trash, buraya player imageları getirip bırakıcaz.


    var trash_left_array = new Array();//soldaki trashe hangi player imageları koydugum.
    var trash_right_array = new Array();//sağdaki trashe hangi player imageları koydugum.

    var trash_left_count = 0; //sol trashe image koyunca 1, bos kalırsa 0 olucak.
    var trash_right_count = 0; //sag trashe image koyunca 1, bos kalırsa 0 olucak.

    var teamId_of_players_trash_left = new Array();//sol trashe koydugum oyuncunun oynadığı takımının team id sini tutuyorum.
    var teamId_of_players_trash_right = new Array();//sag trashe koydugum oyuncunun oynadığı takımının team id sini tutuyorum.


    var loadNew = false;//surekli getPlayersOfTeam i cagırmasın diye bundan faydalanıcam.


    var leftPlayerIsPrinted = false;
    var rightPlayerIsPrinted = false;
    var bothPlayerIsPrintedLeft = false;
    var bothPlayerIsPrintedRight = false;


    // ********************** HERE WE START *************************

    getTeamLogo();//function i cagiriyoruz, databaseden takımları alıyor, logolarını folderdan alıp koyuyor.
    $('#mycarousel').jcarousel();//carousel i çağırıyorum.

    $("#mycarousel .jcarousel-clip").hide();// carouselde normalde boş kutular gözüküyor, onları saklıyorum.
    $("#SelectTeam").show();// carouselin icinde select a team yazısını gösteriyorum.


    $("#player_img").css("overflow","visible");// bunu yapmam lazım yoksa altta player name ler gözükmüyor.


    // database den data cekmek icin kullanıcam bu fonksiyonu.
    function serviceRequest(method, data, callback){
        $.post("/api/" + method, JSON.stringify(data)).done(function(data){
            //console.log(data);
            //console.log(JSON.parse(data));
            callback(data.data);
        });
    }

    var teamId;//secili olan takımın id sini her zaman tutuyorum.
    var element_left;// sol trashte olan item.
    var element_right;//sag trashte olan item.

    var element;

    var playerIdForDetails;



    function getTeamLogo() {// database e request yapıp, takım logolarını alıyorum.



        serviceRequest("GetTeams", {"leagueId": 1, "seasonId": 9064}, function(teamData){
            _.each(teamData, function(value, i){

                var xd = $("<li class=\"ui-widget-content ui-corner-tr\" id=\"" + teamData[i][0] + "\"><h5 class=\"ui-widget-header\">Logo</h5></li>").appendTo("#gallery");


                $('<img src="/static/images/logo' + teamData[i][0] + '.png" />').click(function(){ // takım logosuna tıklandı.

                    $(element_left).fadeTo(400, 1);
                    $(element_right).fadeTo(400, 1);


                    $("#SelectTeam").hide();
                    $("#mycarousel .jcarousel-clip").hide();
                    $("#LoadingImage").show();

                    $(".faded").fadeTo(400, 1);// her image canlı gözüksün diye.
                    $(".faded").removeClass("faded");


                    $(this).addClass("faded");
                    $(this).fadeTo(400, 0.3);// tikladigim takım logosunu soldurdum.

                    teamId = teamData[i][0];
                    console.log(teamId + " is selected.");

                    loadNew = true;

                    // http://stackoverflow.com/questions/14493962/reset-or-reload-jcarousel-on-tab-change
                    $('#mycarousel').data('jcarousel').scroll(0);// carouseli en baştan başlatıyor.

                    $('#mycarousel').jcarousel({itemLoadCallback: getPlayersOfTeam });//carousel e sectigim takımın player image larını koyuyorum.


                    function getPlayersOfTeam(carousel) {//player imagelarını carousel in icine koyuyoruz.

                        if(!loadNew) return;
                        loadNew = false;


                        serviceRequest("GetTeamPlayers", {"leagueId": 1, "seasonId": 9064, "teamId": teamId}, function(playersData){
                            console.log("players data length : " + playersData.length);
                            _.each(playersData, function(val, i){

                                carousel.add(i+1, $('<img src="/static/images/players/' + val[0] + '.jpg" style="width:55px; height:70px; margin-left:10px;" data-player_position=' + val[3] + ' data-player_id=' + val[0] + ' data-name=' + val[1] + ' /><h5 class=\"ui-widget-header\">' + val[1] + '</h5>'));
                            });


                            $(".jcarousel-item").each(function(){
                                var position  = $(this).find("img").data("player_position");

                                $(this).removeClass("goalkeeper");
                                $(this).removeClass("defense");
                                $(this).removeClass("midfield");
                                $(this).removeClass("forward");


                                if(position === 1){
                                    $(this).addClass("goalkeeper");
                                }
                                else if(position === 2){
                                    $(this).addClass("defense");
                                }
                                else if(position === 3){
                                    $(this).addClass("midfield");
                                }
                                else if(position === 4){
                                    $(this).addClass("forward");
                                }
                            });//playerın position ına göre background-color ayarlıyorum.

                            $("#LoadingImage").hide();
                            $("#mycarousel .jcarousel-clip").show();


                            carousel.size(playersData.length + 1);// carousele o kadar kutu koyuyor.
                            $("#player_img").css("left","0");// bunu yapmazsam her seferinde player imagelar sağa kayıyor.


                            // allah stackover flow dan razı olsun: http://stackoverflow.com/questions/5811909/jquery-carousel-with-drag-and-drop.
                            $("li", $player_img).draggable({// player imageların durdugu yeri draggable yapıyoruz.
                                appendTo: "body",
                                cancel: "a.ui-icon",
                                revert: "invalid",
                                helper: "clone",
                                cursor: "move",
                            });

                        });

                    }// end of getPlayersOfTeam function.

                    console.log("su anki team id: " + teamId + ", sol trashtakinin takımı " + teamId_of_players_trash_left[teamId_of_players_trash_left.length - 1]);
                    console.log("su anki team id: " + teamId + ", sağ trashtakinin takımı " + teamId_of_players_trash_right[teamId_of_players_trash_right.length - 1] + "\n");


                    //fenerden webo yu sol trash e attım mesela, sonra galatasaraya tıkladım onun oyuncuları geldi
                    //ama ben hic bisey secmedim. sonra geri fenere tıkladım onun oyuncuları geldi. webo trashte olduğu
                    //icin onu yine soluk yapmam lazım. iste asagıdaki iki tane if bu isi yapıyor.

                    if(trash_left_count > 0){ // first if statement
                        element = trash_left_array[trash_left_array.length-1];//suan sol trashte olan.
                        element.draggable("enable");

                        var current_in_trash = teamId_of_players_trash_left[teamId_of_players_trash_left.length - 1];
                        if(teamId === current_in_trash){
                            console.log("simdi bunu yine soldurucam (left)!");
                            element_left = trash_left_array[trash_left_array.length -1];
                            $(element_left).fadeTo(400, 0.3);
                            $(element_left).draggable("disable");
                        }
                    }


                    if(trash_right_count > 0){// second if statement.
                        element = trash_right_array[trash_right_array.length-1];//suan sağ trashte olan.
                        element.draggable("enable");

                        var current_in_trash = teamId_of_players_trash_right[teamId_of_players_trash_right.length - 1];
                        if(teamId === current_in_trash){
                            console.log("simdi bunu yine soldurucam (right) !");
                            element_right = trash_right_array[trash_right_array.length -1];
                            $(element_right).fadeTo(400, 0.3);
                            $(element_right).draggable("disable");
                        }
                    }


                }).appendTo($(xd));

            });

        });
    }// end of getTeamLogo


    // let the trashes be droppable, accepting the gallery items
    $trash_left.droppable({
        accept: "#player_img > li , #trash_right",
        activeClass: "ui-state-highlight",
        drop: function( event, ui ) {
            //$(ui.draggable).draggable("disable");
            processPlayerImage( ui.draggable , $trash_left, 3);
            showDetailsOfPlayersLeft();
            leftPlayerIsPrinted =true;
            if(leftPlayerIsPrinted && rightPlayerIsPrinted){
                bothPlayerIsPrintedLeft =true;
            }
            getGraphicsSimple3d(leftPlayerIsPrinted,rightPlayerIsPrinted);
        }
    });

    $trash_right.droppable({
        accept: "#player_img > li",
        activeClass: "ui-state-highlight",
        drop: function( event, ui ) {
            //$(ui.draggable).draggable("enable");
            processPlayerImage( ui.draggable , $trash_right, 4);
            showDetailsOfPlayersRight();
            rightPlayerIsPrinted = true;
            getGraphicsSimple3d(leftPlayerIsPrinted,rightPlayerIsPrinted);
            if(leftPlayerIsPrinted && rightPlayerIsPrinted){
                bothPlayerIsPrintedRight =true;
            }
        }
    });



//*********************  Hazır, player img sürükleniyor  ************************************************** 



    function processPlayerImage( $item, $trash, integer) {

        var player_position = $item.find("img").data("player_position");
        var player_id = $item.find("img").data("player_id");
        playerIdForDetails = player_id;

        $item.addClass("faded");
        $item.draggable("disable"); // simdi bu sürüklediğimiz sey artık sürüklenemez olucak.


        $item.fadeTo(400, 0.3, function() {
            if($trash.find("ul").length === 0){

                if(player_position === 1){
                    $list = $( "<ul class='goalkeeper ui-helper-reset'/>" ).appendTo( $trash );
                }else if(player_position === 2){
                    $list = $( "<ul class='defense ui-helper-reset'/>" ).appendTo( $trash );
                }else if(player_position === 3){
                    $list = $( "<ul class='midfield ui-helper-reset'/>" ).appendTo( $trash );
                }else if(player_position === 4){
                    $list = $( "<ul class='forward ui-helper-reset'/>" ).appendTo( $trash );
                }

            } else {
                $list = $trash.find("ul");
            }
        });//sectigim item ı soldurdum ve drop ettigim kutuda arka planın color ını player_position a göre ayarladım.


        console.log($item.find("img").data("name") + " is selected :))\n ");



        if(integer === 3){// 3 -> soldaki trashlar demek.
            trash_left_array.push($item);//sectigim itemi, sola atmak istiyosam, solun arrayine koyuyorum.
            teamId_of_players_trash_left.push(teamId);// kutulara konanların team id lerini de tutuyorum.
            trash_left_count += 1;//şimdi, kutuda bir img oldugu icin count unu 1 yaptım.

        }else if(integer === 4){// 4 -> sağdaki trashlar demek.
            trash_right_array.push($item);//sectigim itemi, sağa atmak istiyosam, sağın arrayine koyuyorum.
            teamId_of_players_trash_right.push(teamId);// kutulara konanların team id lerini de tutuyorum.
            trash_right_count += 1;//şimdi, kutuda bir img oldugu icin count unu 1 yaptım.
        }

        var newItem = $item.clone();//gercekte olan-> item, trashın icindeki-> onun clone u yani newItem.

        if(trash_left_count > 1 || trash_right_count > 1){// 2. image i koymaya calisiyorum demek oluyor.
            $trash.empty();


            if(integer === 3){
                trash_left_count -= 1;
                element = trash_left_array[trash_left_array.length-2];//suan sol trashte olan,benim üstüne koymaya calıstıgım.

            }else if(integer === 4){
                trash_right_count -= 1;
                element = trash_right_array[trash_right_array.length-2];//suan sag trashte olan,benim üstüne koymaya calıstıgım.


            }

            if(trash_left_count > 0){
                if((teamId_of_players_trash_left[teamId_of_players_trash_left.length - 1] === teamId_of_players_trash_left[teamId_of_players_trash_left.length - 2]) && (teamId_of_players_trash_left[teamId_of_players_trash_left.length - 1] === teamId)){// üstüne koyduğumla aynı takımda ise
                    element.fadeTo(400, 1, function(){});
                }
            }

            if(trash_right_count > 0){
                if((teamId_of_players_trash_right[teamId_of_players_trash_right.length - 1] === teamId_of_players_trash_right[teamId_of_players_trash_right.length - 2]) && (teamId_of_players_trash_right[teamId_of_players_trash_right.length - 1] === teamId)){// üstüne koyduğumla aynı takımda ise
                    element.fadeTo(400, 1, function(){});
                }
            }

            element.draggable("enable");//ve onu tekrar draggable yaptım.

        }

        newItem.fadeTo(400, 1, function(){//trashın icindeki bu clone un  boyutunu büyütüyorum.
            newItem.appendTo( $list ).fadeIn(function() {
                newItem.animate({ width: "92px", margin: 0 }).find( "img" ).animate({ height: "130px",  width: "90px", margin:"0px"});
            });

            newItem.click(function(){//bu trashtakine tıklarlarsa, geri gidicek.
                console.log($item.find("img").data("name") + " is sent back!");
                $item.draggable("enable");//tekrar sürüklenebilir oldu.

                $item.fadeTo(400, 1, function(){//dolayısıyle de trash boşalıcak.
                    $trash.empty();
                });

                if(integer === 3){
                    trash_left_count = 0;//solsa trash ta img olmadıgı icin sol countu 0 yapıyorum.
                }else if(integer === 4){
                    trash_right_count = 0;//sag ise trash ta img olmadıgı icin sag countu 0 yapıyorum.
                }


            }).appendTo(newItem);

        });

    }


    function loadPlayerStats(data,pos){

        if(pos === "left"){
            $('#chartLeft > div').remove();
            var chart = d3.select("div #chartLeft").append("div").attr("class", "chart");

        }
        else if(pos === "right"){
            $('#chartRight > div').remove();
            var chart = d3.select("div #chartRight").append("div").attr("class", "chart");

        }

        chart.selectAll("div")
            .data(data)
            .enter()
            .append("div")
            .style("width", function(d) {
                return d * 1 + "px"; })
            .text(function(d) {
                return d;
            });

    }
    var dataLeft;
    var dataRight;

    function getGraphicsSimple3d(leftGraphicsPrinted, rightGraphicsPrinted){
        console.log(playerIdForDetails);
        serviceRequest("GetPlayerCard", {"leagueId": 1, "seasonId": 9064,"weekId": 1, "playerId": playerIdForDetails}, function(playerCardDetails) {


            var pref = {
                "homefill": "c60000",
                "awayfill": "000000",
                "homestroke": "ffffff",
                "awaystroke": "0000cd",
                "width": 800
            };
            var teamStats ;

            if(leftGraphicsPrinted === true && rightGraphicsPrinted === false){
                dataLeft  = [playerCardDetails.statistics.passes[0],playerCardDetails.statistics.passes[1],playerCardDetails.statistics.shotsOnTarget[0],playerCardDetails.statistics.shotsOnTarget[1]];
                teamStats = [
                    {"name": "Toplam Pas", "awayValue": 0, "homeValue": dataLeft[0], "homePercent": 100, "addition": "", "awayPercent": 0},
                    {"name": "Ortalama Pas", "awayValue": 0, "homeValue": dataLeft[1], "homePercent": 100, "addition": "", "awayPercent": 0},
                    {"name": "\u015eut", "awayValue": 0, "homeValue": dataLeft[2], "homePercent": 100, "addition": "", "awayPercent": 0},
                    {"name": "\u0130sabetli \u015eut", "awayValue": 0, "homeValue": dataLeft[3], "homePercent": 100, "addition": "", "awayPercent": 0},
                ];
            }
            else if(leftGraphicsPrinted === false && rightGraphicsPrinted === true){
                dataRight  = [playerCardDetails.statistics.passes[0],playerCardDetails.statistics.passes[1],playerCardDetails.statistics.shotsOnTarget[0],playerCardDetails.statistics.shotsOnTarget[1]];
                teamStats = [
                    {"name": "Toplam Pas", "homeValue": 0, "awayValue": data[0], "homePercent": 0, "addition": "", "awayPercent": 100},
                    {"name": "Ortalama Pas", "homeValue": 0, "awayValue": data[1], "homePercent": 0, "addition": "", "awayPercent": 100},
                    {"name": "\u015eut", "homeValue": 0, "awayValue": data[2], "homePercent": 0, "addition": "", "awayPercent": 100},
                    {"name": "\u0130sabetli \u015eut", "homeValue": 0, "awayValue": data[3], "homePercent": 0, "addition": "", "awayPercent": 100},
                ];
            }
            else if(leftGraphicsPrinted === true && rightGraphicsPrinted === true){
                console.log("inside the both true part");
                /*****************data arraylarinden hangisi boşsa onu doldur***************/
                if(!dataLeft){
                    dataLeft  = [playerCardDetails.statistics.passes[0],playerCardDetails.statistics.passes[1],playerCardDetails.statistics.shotsOnTarget[0],playerCardDetails.statistics.shotsOnTarget[1]];
                }
                if(!dataRight){
                    dataRight  = [playerCardDetails.statistics.passes[0],playerCardDetails.statistics.passes[1],playerCardDetails.statistics.shotsOnTarget[0],playerCardDetails.statistics.shotsOnTarget[1]];
                }
                /*****************data arraylarinden hangisi boşsa onu doldur***************/

                /*****************data arraylarinden hangisi güncellenecekse onu güncelle***************/
                if(bothPlayerIsPrintedLeft){
                    dataLeft  = [playerCardDetails.statistics.passes[0],playerCardDetails.statistics.passes[1],playerCardDetails.statistics.shotsOnTarget[0],playerCardDetails.statistics.shotsOnTarget[1]];
                    bothPlayerIsPrintedLeft =false;
                }
                if(bothPlayerIsPrintedRight){
                    dataRight  = [playerCardDetails.statistics.passes[0],playerCardDetails.statistics.passes[1],playerCardDetails.statistics.shotsOnTarget[0],playerCardDetails.statistics.shotsOnTarget[1]];
                    bothPlayerIsPrintedRight =false;
                }
                /*****************data arraylarinden hangisi güncellenecekse onu güncelle***************/

                var percentArray = new Array();
                for(var i=0; i<4 ;i++){
                    var percent = parseInt([dataLeft[i]/(dataRight[i]+dataLeft[i])]*100);
                    percentArray.push(percent);
                }

                teamStats = [
                    {"name": "Toplam Pas", "awayValue": dataRight[0], "homeValue": dataLeft[0], "homePercent": percentArray[0], "addition": "", "awayPercent": 100-percentArray[0]},
                    {"name": "Ortalama Pas", "awayValue": dataRight[1], "homeValue": dataLeft[1], "homePercent": percentArray[1], "addition": "", "awayPercent": 100-percentArray[1]},
                    {"name": "\u015eut", "awayValue": dataRight[2], "homeValue": dataLeft[2], "homePercent": percentArray[2], "addition": "", "awayPercent": 100-percentArray[2]},
                    {"name": "\u0130sabetli \u015eut", "awayValue": dataRight[3], "homeValue": dataLeft[3], "homePercent": percentArray[3], "addition": "", "awayPercent": 100-percentArray[3]},
                ];

            }


            $("#data-area").empty();
            simpleBar("#data-area", teamStats, pref);

        });




    }

    function showDetailsOfPlayersRight(){
        var position="right";

        rightPlayerIsPrinted =true;

        console.log(playerIdForDetails);
        serviceRequest("GetPlayerDetails", {"leagueId": 1, "seasonId": 9064, "playerId": playerIdForDetails}, function(playerDetails) {
            $('#graphicsRight > div').remove();
            if(!playerDetails){
                $('#chartRight > div').remove();
                $("#graphicsRight").append("<div >Oyuncuyla ilgili data mevcut değil.</div>");
                return;
            }
            console.log(playerDetails);
            $("#graphicsRight").append("<div >name: " + playerDetails[0][0]+ "</div>");
            $("#graphicsRight").append("<div>birthday: " + playerDetails[0][1]+ "</div>");
            $("#graphicsRight").append("<div>height: " + playerDetails[0][2]+ "</div>");

            //var data =[playerCardDetails.statistics.passes[0],playerCardDetails.statistics.passes[1],playerCardDetails.statistics.shotsOnTarget[0],playerCardDetails.statistics.shotsOnTarget[1]]
            //$("#graphicsLeft").append("<p>passes and average passes: " + playerCardDetails.statistics.passes+ "</p>");
            //$("#graphicsLeft").append("<p>shots and on target shots:" + playerCardDetails.statistics.shotsOnTarget+ "</p>");
            //loadPlayerStats(data,position);
            /*
             console.log("player id: " + playerCardDetails.playerId );
             console.log("player playerName: " + playerCardDetails.playerName);
             console.log("player teamId: " + playerCardDetails.teamId);
             console.log("player passes and average pass: " + playerCardDetails.statistics.passes);
             console.log("player shots on target: " + playerCardDetails.statistics.shotsOnTarget);
             */


        });
    }

    function showDetailsOfPlayersLeft(){
        var position="left";

        leftPlayerIsPrinted =true;

        console.log(playerIdForDetails);
        serviceRequest("GetPlayerDetails", {"leagueId": 1, "seasonId": 9064, "playerId": playerIdForDetails}, function(playerDetails) {
            $('#graphicsLeft > div').remove();
            if(!playerDetails){
                $('#chartLeft > div').remove();
                $("#graphicsLeft").append("<div >Oyuncuyla ilgili data mevcut değil.</div>");
                return;
            }
            console.log(playerDetails);
            $("#graphicsLeft").append("<div >name: " + playerDetails[0][0]+ "</div>");
            $("#graphicsLeft").append("<div>birthday: " + playerDetails[0][1]+ "</div>");
            $("#graphicsLeft").append("<div>height: " + playerDetails[0][2]+ "</div>");

            //var data =[playerCardDetails.statistics.passes[0],playerCardDetails.statistics.passes[1],playerCardDetails.statistics.shotsOnTarget[0],playerCardDetails.statistics.shotsOnTarget[1]]
            //$("#graphicsLeft").append("<p>passes and average passes: " + playerCardDetails.statistics.passes+ "</p>");
            //$("#graphicsLeft").append("<p>shots and on target shots:" + playerCardDetails.statistics.shotsOnTarget+ "</p>");
            // loadPlayerStats(data,position);
            /*
             console.log("player id: " + playerCardDetails.playerId );
             console.log("player playerName: " + playerCardDetails.playerName);
             console.log("player teamId: " + playerCardDetails.teamId);
             console.log("player passes and average pass: " + playerCardDetails.statistics.passes);
             console.log("player shots on target: " + playerCardDetails.statistics.shotsOnTarget);
             */
        });


    }






});
