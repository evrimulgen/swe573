// setting up the django CSRF cookie
var csrftoken = $.cookie('csrftoken');
$.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

/*
    The timestamps in the radar data is in form of milliseconds
*/

function FootballPitch(div_id, scope){
    var divSelector = "#" + div_id;

    // scaling stuff
    var pitchScale = 6;
    var pitchOffset = 16;

    var canvasWidth = 105*pitchScale + 2*pitchOffset;
    var canvasHeight = 68*pitchScale + 2*pitchOffset;


    // setting up the canvas and the loading animation
    // and setting up the slider for time range
    $(divSelector).append('<div class="alerts"></div><div class="pitch"></div>');
    $('<canvas id="bgCanvas">').width(canvasWidth).height(canvasHeight).appendTo(divSelector + " .pitch");

    scope.setup("bgCanvas");

    var viewSize = [$("#bgCanvas").width(), $("#bgCanvas").height()];
    scope.view.viewSize = viewSize;


    // meter -> pixel conversion with offset (for points on screen)
    // change the scale and offset as needed
    var mt2px = function (mt) {
        return mt * pitchScale + pitchOffset;
    };

    // meter -> pixel conversion without offset
    // for scaling lengths, instead of points
    var len2px = function(mt){
        return mt * pitchScale;
    }

    var drawField = function () {
        var canvas = $(divSelector + " #bgCanvas");

        var img = new scope.Raster("/static/images/pitch_radar.png", scope.view.center);

        scope.view.draw();
    };


    drawField();
}

function Interpolator(coor1, coor2){
    this.coor1 = coor1;
    this.coor2 = coor2;
    this.delta = [];

    var self = this;
    this.coor1.forEach(function(d1){
        self.coor2.forEach(function(d2){
            if(d1[0]==d2[0] && d1[1]==d2[1]){
                var x = (d2[2]+d1[2])/2;
                var y = (d2[3]+d1[3])/2;
                self.delta.push([d1[0], d1[1], x, y]);
            }
        });
    });
}

Interpolator.prototype = {
    constructor: Interpolator,
    get: function(x){
        if(x == 0){
            return this.coor1;
        }
        else {
            return this.delta;
        }
    }
};

function Radar(matchId){
    var teams = {};
    var scope = new paper.PaperScope();

    var pitch = new FootballPitch("canvasContainer", scope);

    // scaling stuff
    var pitchScale = 6;
    var pitchOffset = 16;

    var mt2px = function (mt) {
        return mt * pitchScale + pitchOffset;
    };

    // meter -> pixel conversion without offset
    // for scaling lengths, instead of points
    var len2px = function(mt){
        return mt * pitchScale;
    }

    var modifyPlayerLocation = function(team_id, jersey_no, xpos, ypos){
        // create the players representation in the first frame
        paper = scope;
        if(teams[team_id]===undefined)
            teams[team_id] = {};

        if(teams[team_id][jersey_no]===undefined){
            var fillColor;
            var strokeColor;
            var text;
            if(team_id===0){
                fillColor = teamColors.homefill;
                strokeColor = teamColors.homestroke;
                text = jersey_no;
            } else if(team_id===1){
                fillColor = teamColors.awayfill;
                strokeColor = teamColors.awaystroke;
                text = jersey_no;
            } else {
                fillColor = "black";
                strokeColor = "yellow";
                text = "H";
            }

            // Creating a group so that the circle + text objects can be moved together
            teams[team_id][jersey_no] = new scope.Group([
                new scope.Path.Circle({
                    center: [mt2px(xpos), mt2px(ypos)],
                    radius: 8,
                    strokeColor: strokeColor,
                    strokeWidth: 2,
                    fillColor: fillColor
                }),
                new scope.PointText({
                    point: [mt2px(xpos), mt2px(ypos)+4],
                    content: text,
                    justification: 'center',
                    fillColor: strokeColor
                })
            ]);
        }
        else{
            // 
            teams[team_id][jersey_no].visible = true;
            teams[team_id][jersey_no].position = new scope.Point(mt2px(xpos), mt2px(ypos));
        }
    };

    var modifyBallLocation = function(x, y){
        if(teams.ball===undefined){
            teams.ball = new scope.Path.Circle({
                center: [mt2px(x), mt2px(y)],
                radius: 4,
                fillColor: "orange",
                strokeColor: "black",
                strokeWidth: 1
            });
        } else {
            teams.ball.visible = true;
            teams.ball.position = new scope.Point(mt2px(x), mt2px(y));
        }
    };

    var modifyPlayerLocations = function(coords){
        var ballVisible = false;
        _.each(teams, function(team, key){
            if(key=='ball') team.visible = false;
            _.each(team, function(player){
                if(player!=undefined){
                    player.visible = false;
                }
            });
        });
        _.each(coords, function(coord){
            // coordinate format:
            // [Type, JerseyNo, X, Y]
            // Types:
            // 0 => Home
            // 1 => Away
            // 2 => Referee
            // 3 => Away GK
            // 4 => Home GK
            // 5 => Ball
            if(coord[1]==-1) return; // ignore unidentified players
            
            if(coord[0]==3 || coord[0]==4) coord[0] -= 3;
            
            if(coord[0]==5){
                modifyBallLocation(coord[2],coord[3]);
            } 
            else modifyPlayerLocation(coord[0], coord[1], coord[2], coord[3]);
        });
    };


    var minute = 0;
    var second = 0;

    var matchInfo = {};
    var teamColors = {};
    var matchSquad = null;
    var connected = false;
    var started = false;
    var paused = false;
    var events = [];
    var currTime = -1;

    var socket = io.connect('http://sentiomessi.cloudapp.net:8080/');
//    var socket = io.connect('http://localhost:8080/');
    var self = this;

    var processCounter = 0;
    var processData = null;
    var processInterpolator = null;
    var processTimeout = false;

    var processEvent = function processEvent(){
        if(processCounter == 0) {

            processData = events.shift();
            processInterpolator = new Interpolator(processData.coor, events[0].coor);
            currTime = processData.gametime;

            if(processData.minute!=minute || processData.second!=second){
                minute = processData.minute;
                second = processData.second;

                $.event.trigger({type: "radarTimeChange", "minute": minute, "second":second});
            }
        }
        modifyPlayerLocations(processInterpolator.get(processCounter));
        scope.view.draw();

        if (processCounter==1){
            processCounter = 0;
        }
        else processCounter++;

        processTimeout = setTimeout(processEvent, (events[0].gametime-currTime) / 2);
    };

    scope.tool.onMouseDown = function(event){
        _.each(teams, function(vals, team){
            if(team=="ball" || team==2) return;
            _.each(vals, function(group, jersey_no){

                if(group.hitTest(event.point)){
                    var team_id = null, player_id=null;
                    if(team==0) team_id = matchInfo.homeId;
                    else if(team==1) team_id = matchInfo.awayId;

                    _.each(matchSquad, function(data){
                        if(data.data[1]==jersey_no && data.data[3]==team_id){
                            player_id = data.data[5];
                        }
                    });

                    $.event.trigger({type: "radarPlayerClick", team_id: team_id, jersey_no: jersey_no,
                                     player_id: player_id, week: matchInfo.week, homeOrAway: team});
                }
            });
        });
    }

    $.post("/api/GetMatchInfo", JSON.stringify({"matchId": matchId})).done(function(data){
        matchInfo.week = data.data[0][0];
        matchInfo.status = data.data[0][2]; // match status, see API docs
        matchInfo.homeId = data.data[0][5];
        matchInfo.awayId = data.data[0][6];

        $.post("/api/GetTeamColors", JSON.stringify({"homeid": matchInfo.homeId, "awayid": matchInfo.awayId})).done(function(data){
            teamColors = data.data;
        });
    });


    $.post("/api/GetMatchSquad", JSON.stringify({"matchId": window.matchId})).done(function(data){
        matchSquad = data.data;
    });

//   var socket = io.connect('http://sentiomessi.cloudapp.net:8080/');
    var socket = io.connect('http://localhost:8080/');
    var self = this;

    socket.on("welcome", function(){
        connected = true;
        $("#canvasOverlay").show();
        console.log("connected");
        self.throw("Bağlantı kuruldu");
    });

    socket.on("matchinfo", function(data){
        console.log("matchinfo");
        console.log(data);
        //TODO: $.event.trigger('matchinfo', ...); for setting up the timeline
    });

    socket.on("match", function(data){
        events.push(data);
        if (events.length == 10 && !started){
            processEvent();
            started = true;
        }
        if (data.comm != undefined){
            $.event.trigger({type: "radarCommentary", message:data.comm});
        }
    });


    socket.on("disconnect", function(){
        console.log("disconnected");
        connected = false;
    });

    this.startMatch = function(){
        // match status: 2 => First half is being played
        //               3 => Second half is being played
        //               6 => Played
        if(!connected){
            self.throw("Sunucuyla bağlantı kesildi!");
            return;
        }
        if(!started){
//            started = true;
            if(matchInfo.status === 2 || matchInfo.status === 3){
                socket.emit('getlivematch', matchId);
            } else if(matchInfo.status === 6){
                socket.emit('getmatch', matchId);
            } else {
                self.throw("Beklenmeyen bir hata oluştu!");
            }
        }
    };

    this.changeTime = function(time){
        processTimeout = false;

        events = [];

        processData = null;
        processInterpolator = null;
        processCounter = 0;
        socket.emit('setmatchtime', time);
    };

    this.togglePause = function(){
        if(!started){
            return;
        } 
        if(paused){
            paused = false;
            socket.emit('resume');
        } else {
            paused = true;
            socket.emit('pause');
        }
    };

    this.throw = function(message){
        $.event.trigger({type: "radarMessage", "message": message});
    }
}