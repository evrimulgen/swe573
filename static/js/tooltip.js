/**
 * Created with PyCharm.
 * User: Serhat
 * Date: 25.10.2013
 * Time: 14:01
 * To change this template use File | Settings | File Templates.
 */
var squad = null;
function setSquad(squad_){
    squad = squad_;
}

$(function() {
    $( document ).tooltip({
        items: "[form-data],[event-data],[player-data]",
        content: function() {
            var element = $( this );
            if ( element.is( "[form-data]" ) ) {
                var text = element.attr("form-data");
                var splitted=text.split(",");
                var weekId  = splitted[0];
                var homeTeam = splitted[1];
                var homeScore = splitted[2];
                var awayScore =splitted[3];
                var awayTeam =splitted[4];
                return "<div class='ttip-form'><p>"+weekId+". Hafta</p><p>"+homeTeam+" "+homeScore+" - "+awayScore+" "+awayTeam+"</p></div>"
            }
            else if ( element.is( "[event-data]" ) ) {
                var text = element.attr("event-data");
                var splitted=text.split(",");
                var matchTime  = splitted[0];
                var playerNameIn = splitted[1];
                var playerName = splitted[2];
                var eventType =splitted[3];

                if(eventType == 7){
                    return "<div class='ttip-events'><p>Oyuncu Değişikliği - Dakika: " + matchTime + "</p><p><span style='color:#ca1111'>" + playerName + "</span> - <span style='color:#139d04'>" + playerNameIn + "</span></p></div>"
                }
                else if(eventType == 0){
                    return "<div class='ttip-events'><p>Gol - Dakika: " + matchTime + "</p><p>" + playerName + "</p></div>"
                }
                else if(eventType == 1){
                    return "<div class='ttip-events'><p>Kendi Kalesine Gol - Dakika: " + matchTime + "</p><p>" + playerName + "</p></div>"
                }
                else if(eventType == 2){
                    return "<div class='ttip-events'><p>Gol(Penaltı) - Dakika: " + matchTime + "</p><p>" + playerName + "</p></div>"
                }
                else if(eventType == 3){
                    return "<div class='ttip-events'><p>Kaçan Penaltı - Dakika: " + matchTime + "</p><p>" + playerName + "</p></div>"
                }
                else if(eventType == 4){
                    return "<div class='ttip-events'><p>Sarı Kart - Dakika: " + matchTime + "</p><p>" + playerName + "</p></div>"
                }
                else if(eventType == 5){
                    return "<div class='ttip-events'><p>İkinci Sarı Kart - Dakika: " + matchTime + "</p><p>" + playerName + "</p></div>"
                }
                else if(eventType == 6){
                    return "<div class='ttip-events'><p>Kırmızı Kart - Dakika: " + matchTime + "</p><p>" + playerName + "</p></div>"
                }
            }
            else if ( element.is( "[player-data]" ) ) {
                var text = element.attr("player-data");
                for(var i=0;i<squad.length;i++){
                    var returnVal = "";
                    if(parseInt(squad[i]["playerId"]) == parseInt(text)){
                        var events = squad[i]["playerEvents"];
                        if(events.length == 0){
                            return
                        }
                        for(var j=0; j<events.length; j++){
                            var eventType = events[j]["eventType"];
                            var matchTime  = events[j]["matchTime"];
                            var playerName = events[j]["playerName"];
                            var playerNameIn = events[j]["playerNameIn"];
                            if(eventType == 7){;
                                returnVal += "<div class='ttip-formation'><p>" + matchTime + "' <span style='color:#ca1111'>" + playerName + "</span> - <span style='color:#139d04'>" + playerNameIn + "</span></p></div>"
                            }
                            else if(eventType == 0){
                                returnVal += "<div class='ttip-formation'><p>" + matchTime + "' Gol</p></div>"
                            }
                            else if(eventType == 1){
                                returnVal += "<div class='ttip-formation'><p>" + matchTime + "' Kendi Kalesine Gol</p></div>"
                            }
                            else if(eventType == 2){
                                returnVal += "<div class='ttip-formation'><p>" + matchTime + "' Gol(Penaltı)</p> </div>"
                            }
                            else if(eventType == 3){
                                returnVal += "<div class='ttip-formation'><p>" + matchTime + "' Kaçan Penaltı</p> </div>"
                            }
                            else if(eventType == 4){
                                returnVal += "<div class='ttip-formation'><p>" + matchTime + "' Sarı Kart</p> </div>"
                            }
                            else if(eventType == 5){
                                returnVal += "<div class='ttip-formation'><p>" + matchTime + "' İkinci Sarı Kart</p> </div>"
                            }
                            else if(eventType == 6){
                                returnVal += "<div class='ttip-formation'><p>" + matchTime + "' Kırmızı Kart</p> </div>"
                            }
                        }
                        return returnVal;
                    }
                }
            }
        },
        show: {
            effect: "show",
            delay: 50
        },
        hide: {
            effect: "hide",
            delay: 100
        },
        position: {
            my: "center bottom",
            at: "center top-2"
        },
        close: function (event, ui) {
            $('div.ui-effects-wrapper').remove();
        }
    });
});