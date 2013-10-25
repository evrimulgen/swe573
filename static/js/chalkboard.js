/*jslint nomen: true, plusplus: true, todo: true, vars: true */
/*global $: true, _: true, paper: true, h337: true */

function Chalkboard(div_id, match_id){
    "use strict";

    var divSelector = "#" + div_id;

    // scaling stuff
    var pitchScale = 4.8;
    var pitchOffset = 12.8;

    var canvasWidth = 68*pitchScale +2* pitchOffset;
    var canvasHeight = 105*pitchScale +2*pitchOffset;

    // setting up the canvas and the loading animation
    // and setting up the slider for time range
    $(divSelector).append('<div class="alerts"></div><div class="chalkboard pitch"></div>');
    $('<canvas id="bgCanvas">').width(canvasWidth).height(canvasHeight).appendTo(divSelector + " .chalkboard");
    $('<canvas id="fgCanvas">').width(canvasWidth).height(canvasHeight).appendTo(divSelector + " .chalkboard");
    $(divSelector+" .chalkboard").append('<img id="spinner" src="/static/images/spinner.gif" />');
    $(".pitch canvas").width(canvasWidth).height(canvasHeight);

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

    var viewSize = [$("#bgCanvas").width(), $("#bgCanvas").height()];
    bgScope.view.viewSize = viewSize;
    fgScope.view.viewSize = viewSize;

    // setting up the django CSRF cookie
    var csrftoken = $.cookie('csrftoken');
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });


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

    // meter -> pixel conversion with offset (for points on screen)
    // change the scale and offset as needed
    var mt2px = function (mt) {
        return mt *pitchScale + pitchOffset;
    };

    // meter -> pixel conversion without offset
    // for scaling lengths, instead of points
    var len2px = function(mt){
        return mt * pitchScale;
    }

    // draws the football field
    var drawField = function () {
        paper = bgScope;

        var canvas = $(divSelector + " #bgCanvas");

        var img = new paper.Raster("/static/images/pitchradar2.png", paper.view.center);

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
        var length = pts.length;
        if(length<2){
            return;
        }

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
            heatmap.store.addDataPoint(canvasWidth-mt2px(item[1]),mt2px(item[0]), item[2]);
        });
    };

    var drawPasses = function () {
        paper = fgScope;
        layers.passes.activate();

        var passData = currentData["GetPassLocations"];

        _.each(passData, function (pass) {
            console.log(pass);

            // sometimes, the data returned from api contains some elements with null location data. i just ignore them
            if (pass[3] === null || pass[4] === null || pass[5] === null || pass[6] === null) {
                return;
            }

            // a pass with (0,0) start or end coordinates is null, filter that out as well
            if(pass[3]===0&&pass[4]===0||pass[5]===0&&pass[6]===0){
                return;
            }

            // filter by time
            if(pass[1]<timeBounds[0] || pass[1]>timeBounds[1]){
                return;
            }

            /* sample pass location data from GetPassLocations:
               [2, 49, 17, 2.76, 34.1, 6.7, 34.3, 1]
               [First/Second Half, Minute, Second, FromY, FromX, ToY, ToX, Successful] */

            var to = new paper.Point(canvasWidth-mt2px(pass[6]), mt2px(pass[5]));
            var from = new paper.Point(canvasWidth-mt2px(pass[4]), mt2px(pass[3]));

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

            // a shot with (0,0) coordinates is invalid as well
            if (shot[3]===0&&shot[4]===0){
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
                return new paper.Point(canvasWidth-mt2px(pt[3]), mt2px(pt[2]));
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
            $.post("/api/" + method, postData).done(function (data) {
                var res = data;
                if(res.code==0){
                    cache[method][postData] = res.data;
                    currentData[method] = res.data;
                    callback(res.data);
                } else {
                    createAlert("Bir hata oluştu");
                }
            }).fail(function(){
                createAlert("Bir hata oluştu");
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
