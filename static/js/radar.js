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

    // draws the football field
    var drawField = function () {
        var canvas = $(divSelector + " #bgCanvas")
        var greenBg = new scope.Path.Rectangle(0, 0, canvas.width(), canvas.height());
        greenBg.fillColor = "#618142";

        // green lines in the pitch
        var greenLineHeight = $(divSelector + " #bgCanvas").height();
        var greenLineWidth = $(divSelector + " #bgCanvas").width()/15+1;
        for (var i = 0; i < 15; i++) {
            var bgPath = new scope.Path.Rectangle(new scope.Rectangle(i * greenLineWidth-1, 0, greenLineWidth, greenLineHeight));
            if (i % 2) {
                bgPath.fillColor = "#ffffff";
                bgPath.opacity = 0.1;
            }
        }
        

        // pretty straightforward lines and stuff
        // the dimensions of the football pitch are taken from http://en.wikipedia.org/wiki/Association_football_pitch

        var lineWidth = 2;
        
        var outerLine = new scope.Path.Rectangle(new scope.Rectangle(mt2px(0), mt2px(0), len2px(105), len2px(68)));
        outerLine.strokeColor = "white";
        outerLine.strokeWidth = lineWidth;

        var halfLine = new scope.Path();
        halfLine.add(new scope.Point(mt2px(52.5), mt2px(0)), new scope.Point(mt2px(52.5), mt2px(68)));
        halfLine.strokeColor = "white";
        halfLine.strokeWidth = lineWidth;

        var centerCircle = new scope.Path.Circle(new scope.Point(mt2px(52.5), mt2px(34)), len2px(9.15));
        centerCircle.strokeColor = "white";
        centerCircle.strokeWidth = lineWidth;

        var centerSpot = new scope.Path.Circle(new scope.Point(mt2px(52.5), mt2px(34)), 3);
        centerSpot.fillColor = "white";

        var penaltyAreaTop = new scope.Path.Rectangle(new scope.Rectangle(mt2px(0), mt2px(13.85), len2px(16.5), len2px(40.3)));
        penaltyAreaTop.strokeColor = "white";
        penaltyAreaTop.strokeWidth = lineWidth;

        var penaltySpotTop = new scope.Path.Circle(new scope.Point(mt2px(11), mt2px(34)), 3);
        penaltySpotTop.fillColor = "white";

        var goalAreaTop = new scope.Path.Rectangle(new scope.Rectangle(mt2px(0), mt2px(24.84), len2px(5.5), len2px(18.32)));
        goalAreaTop.strokeColor = "white";
        goalAreaTop.strokeWidth = lineWidth;

        // needed for arcs:
        // the radius of the arcs are 9.15m and they are centered on the penalty spot
        // distance between penalty spot and the penalty area is 5.5m
        // so, distance between the horizontally centered line of the pitch and an endpoint 
        // of the specified arc is sqrt(9.15^2-5.5^2) = 7.31m
        var penaltyCircleTop = new scope.Path.Arc(new scope.Point(mt2px(16.5), mt2px(26.69)), new scope.Point(mt2px(20.15), mt2px(34)), new scope.Point(mt2px(16.5), mt2px(41.31)));
        penaltyCircleTop.strokeColor = "white";
        penaltyCircleTop.strokeWidth = lineWidth;

        var penaltyAreaBottom = new scope.Path.Rectangle(new scope.Rectangle(mt2px(88.5), mt2px(13.85), len2px(16.5), len2px(40.3)));
        penaltyAreaBottom.strokeColor = "white";
        penaltyAreaBottom.strokeWidth = lineWidth;

        var penaltySpotBottom = new scope.Path.Circle(new scope.Point(mt2px(94), mt2px(34)), 3);
        penaltySpotBottom.fillColor = "white";

        var goalAreaBottom = new scope.Path.Rectangle(new scope.Rectangle(mt2px(99.5), mt2px(24.84), len2px(5.5), len2px(18.32)));
        goalAreaBottom.strokeColor = "white";
        goalAreaBottom.strokeWidth = lineWidth;

        var penaltyCircleBottom = new scope.Path.Arc(new scope.Point(mt2px(88.5), mt2px(26.69)), new scope.Point(mt2px(84.85), mt2px(34)), new scope.Point(mt2px(88.5), mt2px(41.31)));
        penaltyCircleBottom.strokeColor = "white";
        penaltyCircleBottom.strokeWidth = lineWidth;

        scope.view.draw();
    };

    drawField();
};

function Radar(matchId, scope){
    var teams = {};
    var pitch = new FootballPitch("radarContainer", scope);

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
        if(teams[team_id]===undefined) teams[team_id] = {};
        if(teams[team_id][jersey_no]===undefined){
            var fillColor;
            if(team_id==1){
                fillColor = "red";
            } else {
                fillColor = "blue";
            }

            // Creating a group so that the circle + text objects can be moved together
            teams[team_id][jersey_no] = new scope.Group([
                new scope.Path.Circle({
                    center: [mt2px(xpos), mt2px(ypos)],
                    radius: 8,
                    strokeColor: 'yellow',
                    strokeWidth: 2,
                    fillColor: fillColor
                }),
                new scope.PointText({
                    point: [mt2px(xpos), mt2px(ypos)+4],
                    content: jersey_no,
                    justification: 'center',
                    fillColor: 'white'
                })
            ]);
        }
        else{
            // 
            teams[team_id][jersey_no].position = new scope.Point(mt2px(xpos), mt2px(ypos));
        }
    };

    var modifyBallLocation = function(x, y){
        if(teams.ball===undefined){
            teams.ball = new scope.Path.Circle({
                center: [mt2px(x), mt2px(y)],
                radius: 4,
                fillColor: "magenta",
                strokeColor: "black",
                strokeWidth: 1
            });
        } else {
            teams.ball.visible = true;
            teams.ball.position = new scope.Point(mt2px(x), mt2px(y));
        }
    };

    var hideBall = function(){
        if(teams.ball!==undefined){
            teams.ball.visible = false;
        }
    }

    var modifyPlayerLocations = function(coords){
        var ballVisible = false;
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
                ballVisible = true;
                modifyBallLocation(coord[2],coord[3]);
            } 
            else modifyPlayerLocation(coord[0], coord[1], coord[2], coord[3]);
        });
        if(!ballVisible) hideBall();
    }

    var minute = 0;
    var second = 0;

    var started = false;
    var paused = false;
    var events = [];
    var currTime = -1;

    var processEvent = function processEvent(){
        var data = events.shift();
        currTime = data.gametime;

        modifyPlayerLocations(data.coor);
        scope.view.draw();

        // updating the time display
        if(data.minute!=minute || data.second!=second){
            minute = data.minute;
            second = data.second;
            $("#timeDisplay").html(minute+":"+second);

            $.event.trigger({type: "radarTimeChange", "minute": minute, "second":second});
        }

        if(events[0]!==undefined){
            // wait until the next event's time
            setTimeout(processEvent, events[0].gametime-currTime);
        }
    };

    scope.tool.onMouseDown = function(event){
        _.each(teams, function(vals, team){
            if(team==="ball") return;
            _.each(vals, function(group, jersey_no){
                if(group.hitTest(event.point)){
                    console.log("clicked player - team id " + team + " - jersey number " + jersey_no);
                }
            });
        });
    }

    var socket = io.connect('http://sentiomessi.cloudapp.net:8080/');
    //var socket = io.connect('http://localhost:8080/');

    socket.on("welcome", function(){
        console.log("connected");
    });

    socket.on("matchinfo", function(data){
        console.log("matchinfo");
        console.log(data);
        //$.event.trigger('matchinfo', ...);
    });

    socket.on("match", function(data){
        events.push(data);
        if(events.length===1){
            processEvent();
        }
    });


    this.startMatch = function(){
        if(!started){
            started = true;
            socket.emit('getmatch', matchId);
        }
    };

    this.changeTime = function(time){
        console.log(time);
        events = [];
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
    }
}