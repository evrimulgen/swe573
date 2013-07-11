/*jslint nomen: true, plusplus: true, todo: true, vars: true */
/*global $: true, _: true, paper: true, h337: true */

function Chalkboard(div_id, match_id){
    "use strict";

    var divSelector = "#" + div_id;

    // setting up the canvas and the loading animation
    // and setting up the slider for time range
    $(divSelector).append('<div class="alerts"></div><div class="chalkboard"><canvas id="bgCanvas"></canvas><canvas id="fgCanvas"></canvas><img id="spinner" src="/static/images/spinner.gif" /></div>');

    // setting up two scopes for two canvases
    // bgCanvas contains the football field and fgCanvas has everything else
    // this is in order to have the field-heatmap-passes order
    // TODO: it is said that this causes problems when resizing
    // if this causes a problem, the links with fix:
    // https://groups.google.com/forum/#!topic/paperjs/lM6u_m2epi8
    // http://zgrossbart.github.io/multipaper/
    var bgScope = new paper.PaperScope();
    var fgScope = new paper.PaperScope();
    bgScope.setup("bgCanvas");
    fgScope.setup("fgCanvas");

    // setting up layers for different displays
    paper = fgScope;
    var layers = { passes: new paper.Layer(), shots: new paper.Layer(), runpaths: new paper.Layer() };

    // setting up the (currently empty) heatmap
    var heatmap = h337.create({element: $(divSelector + " .chalkboard")[0], opacity: 60, radius: 25});

    // Cache for api requests so that if it's already been fetched, it doesn't have to be requested again
    var cache = {};

    // used for filtering shots and passes without reloading the data from the backend
    var currentData = {};

    // table of currently activated layers
    var activatedLayers = { passes: false, shots: false, heatmap: false, runpaths: false };

    var matchId = match_id;
    var currentPlayer = {};
    
    var timeBounds = [0, 90];

    // scaling stuff
    var pitchScale = 5;
    var pitchOffset = 16;

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

    var drawCircleWithInfo = function (center, info) {
        var circ = new paper.Path.Circle(center, 10);

        // TODO: use the team's colors that'll be fetched from the backend
        circ.fillColor = "#FFED3F";
        circ.strokeColor = "#E82A20";
        circ.strokeWidth = 2;

        // moving 4pixels down to center the text vertically
        // not sure if this approach will work as intended in mobile browsers
        var textpt = center.add(new paper.Point(0, 4));

        var txt = new paper.PointText(textpt);
        txt.content = info;
        txt.justification = "center";
        txt.fillColor = "black";
    };

    var drawArrow = function (pts, info) {
        // drawing the line itself
        var line = new paper.Path();
        
        _.each(pts, function (pt) {
            line.add(pt);
        });
        line.strokeColor = "#eeeeee";
        line.strokeWidth = 2;

        // drawing the info circle
        if (info !== undefined) {
            drawCircleWithInfo(pts[0], info);
        }

        // drawing the arrow head
        // the trigonometric stuff is copy-pasted from the code i've previously written 
        // on https://github.com/kuzux/kuzux.github.com/blob/master/line-segment-intersection.js (the drawArrow function)
        // there might be an easier/clearer way to do that with paperjs, 
        // i think it can modify the angles of vector objects and stuff
        var length = pts.length;

        var fromx = pts[length - 2].x;
        var fromy = pts[length - 2].y;
        var tox = pts[length - 1].x;
        var toy = pts[length - 1].y;

        var headlength = 10;
        var angle = Math.atan2(toy - fromy, tox - fromx);

        var leftpt = new paper.Point(tox - headlength * Math.cos(angle - Math.PI / 6), toy - headlength * Math.sin(angle - Math.PI / 6));
        var rightpt = new paper.Point(tox - headlength * Math.cos(angle + Math.PI / 6), toy - headlength * Math.sin(angle + Math.PI / 6));

        var arrow = new paper.Path();
        arrow.add(leftpt);
        arrow.add(pts[length - 1]);
        arrow.add(rightpt);
        arrow.strokeColor = "#eeeeee";
        arrow.strokeWidth = 2;
    };

    var generateHeatmap = function (heatData) {
        heatmap.clear();

        // convert the items coordinates from meters to pixels with correct order
        _.each(heatData, function (item) {
            heatmap.store.addDataPoint(mt2px(item[0]), mt2px(item[1]), item[2]);
        });
    };

    var drawPasses = function () {
        paper = fgScope;
        layers.passes.activate();

        var passData = currentData["GetPassLocations"];

        _.each(passData, function (pass) {

            // sometimes, the data returned from api contains some elements with null location data. i just ignore them
            if (pass[3] === null || pass[4] === null || pass[5] === null || pass[6] === null) {
                return;
            }

            // filter by time
            if(pass[1]<timeBounds[0] || pass[1]>timeBounds[1]){
                return;
            }

            /* sample pass location data from GetPassLocations:
               [2, 49, 17, 2.76, 34.1, 6.7, 34.3, 1]
               [First/Second Half, Minute, Second, FromY, FromX, ToY, ToX, Successful] */

            var to = new paper.Point(mt2px(pass[5]), mt2px(pass[6]));
            var from = new paper.Point(mt2px(pass[3]), mt2px(pass[4]));

            drawArrow([from, to], pass[1]);
        });

        paper.view.draw();
    };

    var drawShots = function () {
        paper = fgScope;
        layers.shots.activate();

        var shotData = currentData["GetShotLocations"];

        _.each(shotData, function (shot) {
            // the shot data can also contain null coordinates just like the pass data
            if (shot[3] === null || shot[4] === null) {
                return;
            }

            // filter by time
            if(shot[1]<timeBounds[0] || shot[1]>timeBounds[1]){
                return;
            }

            /* sample shot locaton data from GetShotLocations:
               [1, 22, 4, 104.02, 48.48]
               [First/Second Half, Minute, Second, FromY, FromX] */

            var from = new paper.Point(mt2px(shot[3]), mt2px(shot[4]));

            drawCircleWithInfo(from, shot[1]);
        });

        paper.view.draw();
    };

    var drawRunPaths = function (pathData) {
        paper = fgScope;
        layers.runpaths.activate();

        /* sample runpath data from GetRunPaths
           [1, 2, 72.3499984741211, 40.099998474121094]
           [First/Second Half, RunpathId, PointY, PointX] */

        // separate the points by their runpath IDs 
        var paths = _.groupBy(pathData, function (item) {
            return item[1];
        });

        // then process those separated runpaths into paper.Path objects
        _.each(paths, function (path) {
            var pathToDraw = new paper.Path();
            pathToDraw.strokeColor = "white";

            var pts = _.map(path, function (pt) {
                return new paper.Point(mt2px(pt[2]), mt2px(pt[3]));
            });

            drawArrow(pts);
        });

        paper.view.draw();
    };

    // create a bootstrap alerts box on top of the chalkboard canvas
    var createAlert = function(message){
        $(divSelector + " .alerts").append('<div class="alert"><span>'+message+'</span><a class="close" data-dismiss="alert">×</a></div>')
    }

    // Does an api request to the specified method with args and passes the requested data to callback
    // Also does caching, not usable for realtime data
    // Caching is somewhat naive, using two nested objects with method and arguments as keys.
    var apiRequest = function (method, args, callback) {
        var postData = JSON.stringify(args);

        // lazily initialize the subobjects of the cache
        if(cache[method]===undefined){
            cache[method] = {};
        }

        // if the data exists in the cache, just call the callback
        // if it isn't, populate the cache and then do the callback
        if(cache[method][postData]!==undefined){
            currentData[method] = cache[method][postData];
            callback(cache[method][postData]);
        } else {
            $(divSelector + " #spinner").show();

            // actually fetch the data from the backend
            $.post("http://localhost:8080/api/" + method, postData).done(function (data) {
                var res = JSON.parse(data);
                if(res.code==0){
                    cache[method][postData] = res.data;
                    currentData[method] = res.data;
                    callback(res.data);
                } else {
                    createAlert("Biseyler ters gitti");
                }
            }).fail(function(){
                createAlert("Biseyler ters gitti");
            }).always(function(){
                // hide the spinner gif whether the request succeeded or not
                $(divSelector + " #spinner").hide();
            });
        }
    };

    var clearAll = function () {
        layers.shots.removeChildren();
        layers.passes.removeChildren();
        layers.runpaths.removeChildren();
        heatmap.clear();
    };

    this.changePlayer = function (player) {
        if(currentPlayer.id === player.id) return;

        clearAll();
        currentPlayer = player;
        var cb = this;

        _.each(activatedLayers, function(value,key){
            if(value){
                cb.activateLayer(key);
            }
        });
    };

    this.activateLayer = function (layer) {
        activatedLayers[layer] = true;
        switch(layer){
        case "shots":
            apiRequest("GetShotLocations", {"match_id": matchId, "player_id": currentPlayer.id}, drawShots);
            break;
        case "passes":
            apiRequest("GetPassLocations", {"match_id": matchId, "player_id": currentPlayer.id}, drawPasses);
            break;
        case "heatmap":
            apiRequest("GetPlayersHeatmap", {"match_id": matchId, "team_id": currentPlayer.team_id, 
                                             "jersey_number": currentPlayer.jersey_number, "min_from": timeBounds[0], 
                                             "min_to": timeBounds[1]}, generateHeatmap);
            break;
        case "runpaths":
            apiRequest("GetRunPaths", {"match_id": matchId, "team_id": currentPlayer.team_id, 
                                       "jersey_number": currentPlayer.jersey_number, "min_from": timeBounds[0], 
                                       "min_to": timeBounds[1]}, drawRunPaths);
            break;
        }
    };

    this.deactivateLayer = function (layer) {
        activatedLayers[layer]  =false;
        if(layer==="heatmap") heatmap.clear();
        else layers[layer].removeChildren();
    };

    this.applyTimeFilter = function (start, end) {
        timeBounds = [start, end];

        // weird hack because 'this' is something else within the callback of _.each
        var cb = this;

        _.each(activatedLayers, function(val, key){
            if(val){
                cb.deactivateLayer(key);
                cb.activateLayer(key);
            }
        });
    };

    // draw the football field
    drawField();
}
