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

function FootballPitch(div_id){
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
    $('<canvas id="fgCanvas">').width(canvasWidth).height(canvasHeight).appendTo(divSelector + " .pitch");

    var bgScope = new paper.PaperScope();
    var fgScope = new paper.PaperScope();
    bgScope.setup("bgCanvas");
    fgScope.setup("fgCanvas");

    var viewSize = [$("#bgCanvas").width(), $("#bgCanvas").height()];
    bgScope.view.viewSize = viewSize;
    fgScope.view.viewSize = viewSize;

    this.paper = bgScope;

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
        paper = bgScope;

        var canvas = $(divSelector + " #bgCanvas")
        var greenBg = new paper.Path.Rectangle(0, 0, canvas.width(), canvas.height());
        greenBg.fillColor = "#618142";

        // green lines in the pitch
        var greenLineHeight = $(divSelector + " #bgCanvas").height();
        var greenLineWidth = $(divSelector + " #bgCanvas").width()/15+1;
        for (var i = 0; i < 15; i++) {
            var bgPath = new paper.Path.Rectangle(new paper.Rectangle(i * greenLineWidth-1, 0, greenLineWidth, greenLineHeight));
            if (i % 2) {
                bgPath.fillColor = "#ffffff";
                bgPath.opacity = 0.1;
            }
        }
        

        // pretty straightforward lines and stuff
        // the dimensions of the football pitch are taken from http://en.wikipedia.org/wiki/Association_football_pitch

        var lineWidth = 2;
        
        var outerLine = new paper.Path.Rectangle(new paper.Rectangle(mt2px(0), mt2px(0), len2px(105), len2px(68)));
        outerLine.strokeColor = "white";
        outerLine.strokeWidth = lineWidth;

        var halfLine = new paper.Path();
        halfLine.add(new paper.Point(mt2px(52.5), mt2px(0)), new paper.Point(mt2px(52.5), mt2px(68)));
        halfLine.strokeColor = "white";
        halfLine.strokeWidth = lineWidth;

        var centerCircle = new paper.Path.Circle(new paper.Point(mt2px(52.5), mt2px(34)), len2px(9.15));
        centerCircle.strokeColor = "white";
        centerCircle.strokeWidth = lineWidth;

        var centerSpot = new paper.Path.Circle(new paper.Point(mt2px(52.5), mt2px(34)), 3);
        centerSpot.fillColor = "white";

        var penaltyAreaTop = new paper.Path.Rectangle(new paper.Rectangle(mt2px(0), mt2px(13.85), len2px(16.5), len2px(40.3)));
        penaltyAreaTop.strokeColor = "white";
        penaltyAreaTop.strokeWidth = lineWidth;

        var penaltySpotTop = new paper.Path.Circle(new paper.Point(mt2px(11), mt2px(34)), 3);
        penaltySpotTop.fillColor = "white";

        var goalAreaTop = new paper.Path.Rectangle(new paper.Rectangle(mt2px(0), mt2px(24.84), len2px(5.5), len2px(18.32)));
        goalAreaTop.strokeColor = "white";
        goalAreaTop.strokeWidth = lineWidth;

        // needed for arcs:
        // the radius of the arcs are 9.15m and they are centered on the penalty spot
        // distance between penalty spot and the penalty area is 5.5m
        // so, distance between the horizontally centered line of the pitch and an endpoint 
        // of the specified arc is sqrt(9.15^2-5.5^2) = 7.31m
        var penaltyCircleTop = new paper.Path.Arc(new paper.Point(mt2px(16.5), mt2px(26.69)), new paper.Point(mt2px(20.15), mt2px(34)), new paper.Point(mt2px(16.5), mt2px(41.31)));
        penaltyCircleTop.strokeColor = "white";
        penaltyCircleTop.strokeWidth = lineWidth;

        var penaltyAreaBottom = new paper.Path.Rectangle(new paper.Rectangle(mt2px(88.5), mt2px(13.85), len2px(16.5), len2px(40.3)));
        penaltyAreaBottom.strokeColor = "white";
        penaltyAreaBottom.strokeWidth = lineWidth;

        var penaltySpotBottom = new paper.Path.Circle(new paper.Point(mt2px(94), mt2px(34)), 3);
        penaltySpotBottom.fillColor = "white";

        var goalAreaBottom = new paper.Path.Rectangle(new paper.Rectangle(mt2px(99.5), mt2px(24.84), len2px(5.5), len2px(18.32)));
        goalAreaBottom.strokeColor = "white";
        goalAreaBottom.strokeWidth = lineWidth;

        var penaltyCircleBottom = new paper.Path.Arc(new paper.Point(mt2px(88.5), mt2px(26.69)), new paper.Point(mt2px(84.85), mt2px(34)), new paper.Point(mt2px(88.5), mt2px(41.31)));
        penaltyCircleBottom.strokeColor = "white";
        penaltyCircleBottom.strokeWidth = lineWidth;

        paper.view.draw();
    };

    drawField();
};

$(function(){
    var socket = io.connect('http://sentiomessi.cloudapp.net:8080/');

    var teams = {};

    var pitch = new FootballPitch("radarContainer");

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
        if(teams[team_id]===undefined) teams[team_id] = {};
        if(teams[team_id][jersey_no]===undefined){
            var fillColor;
            if(team_id==1){
                fillColor = "red";
            } else {
                fillColor = "blue";
            }

            teams[team_id][jersey_no] = new pitch.paper.Group([
                new pitch.paper.Path.Circle({
                    center: [mt2px(xpos), mt2px(ypos)],
                    radius: 8,
                    strokeColor: 'yellow',
                    strokeWidth: 2,
                    fillColor: fillColor
                }),
                new pitch.paper.PointText({
                    point: [mt2px(xpos), mt2px(ypos)+4],
                    content: jersey_no,
                    justification: 'center',
                    fillColor: 'white'
                })
            ]);
        }
        else{
            teams[team_id][jersey_no].position = new pitch.paper.Point(mt2px(xpos), mt2px(ypos));
        }
        //$("#playerPositions").text(JSON.stringify(teams));
    };

    var modifyBallLocation = function(x, y){
        if(teams.ball===undefined){
            teams.ball = new pitch.paper.Path.Circle({
                center: [mt2px(x), mt2px(y)],
                radius: 4,
                fillColor: "white",
                strokeColor: "black",
                strokeWidth: 1
            });
        } else {
            teams.ball.position = new pitch.paper.Point(mt2px(x), mt2px(y));
        }
    };

    var modifyPlayerLocations = function(coordString){
        var coords = coordString.split("+");

        _.each(coords, function(coord){
            // coordinate format:
            // [Type, ??, JerseyNo, X, Y]
            // Types:
            // 0 => Home
            // 1 => Away
            // 2 => Ball?
            // 3 => Away GK
            // 4 => Home GK
            if(coord.length > 1){
                var data = coord.split(",");
                if(data[0]==3 || data[0]==4) data[0] -= 3;
                
                if(data[0]==5) modifyBallLocation(data[3],data[4]);
                else modifyPlayerLocation(data[0], data[2], data[3], data[4]);
            }
        });
    }

    var minute = 0;
    var second = 0;

    var started = false;
    var events = [];
    var animations = [];
    var currTime = -1;

    var processEvent = function processEvent(){
        var data = events.shift();
        currTime = data['MATCH_TIMESTAMP'];

        modifyPlayerLocations(data['COORDINATE_STRING']);
        pitch.paper.view.draw();

        if(data['MATCH_MINUTE']!=minute || data['MATCH_SECOND']!=second){
            minute = data['MATCH_MINUTE'];
            second = data['MATCH_SECOND'];
            $("#timeDisplay").html((minute-1)+":"+second);
        }

        if(events[0]!==undefined)
            setTimeout(processEvent, events[0]['MATCH_TIMESTAMP']-currTime);
    };

    socket.on("welcome", function(){
        console.log("connected");
    });

    $("#startMatch").click(function(){
        if(!started){
            started = true;
            socket.emit('getmatch', 85);
        }
    });

    socket.on("match", function(data){
        events.push(data);
        if(events.length===1){
            processEvent();
        }
    });

});