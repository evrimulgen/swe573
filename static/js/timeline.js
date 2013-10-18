function Timeline(options){
    var div_id = options.divId;
    var match_id = options.matchId;
    var sliderCount = options.sliderCount;
    var scope = new paper.PaperScope();
    var isLive = null;
    var matchInfo = {};

    var width = 662;
    var height = 50;

    var handleWidth = 20;

    var currentPoint = [0,0];
    var maxSecond = 90*60;

    var leftHandle = null;
    var rightHandle = null;
    var draggedHandle = null;

    var handleBarLeft = null;
    var handleBarRight = null;
    var choosenAreaRect = null;

    var eventImages = [];
    var matchEvents = [];
    var eventGroups = [];

    var boxOffset;
    var boxHeight = 15;
    var boxWidth = 125;
    var topPadding = 9;
    var boxPadding = 2;
    var fontSize = 10;

    var lastMin = 0;

    var momentumPath = null;
    var eventImagesGroup = null;

    $("#"+div_id).width(width).height(height+20);

    scope.setup(div_id);

    // setting up the django CSRF cookie
    var csrftoken = $.cookie('csrftoken');
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    $.post("/api/GetMatchInfo", JSON.stringify({"matchId": matchId})).done(function(data){
        matchInfo.week = data.data[0][0];
        matchInfo.status = data.data[0][2]; // match status, see API docs
        matchInfo.homeId = data.data[0][5];
        matchInfo.awayId = data.data[0][6];

        if(matchInfo.status == 2 || matchInfo.status == 3 || matchInfo.status == 10) isLive = true;

        drawSlider();
        drawTeamLogos(matchInfo.homeId, matchInfo.awayId);
        loadMomentum(function(unused){
            loadEvents();
            drawHandle();
        });
    });

    var drawSlider = function(){
        paper = scope;
        var bg = new scope.Path.Rectangle(0, 0, width, height);
        bg.fillColor = {
            gradient: {
                stops: [["#dbdbdb",0.93],["#6d6d6d",1]]
            },
            origin: [width/2,0],
            destination: [width/2,height]
        }

        var sliderbg = new scope.Path.Rectangle(0, height, width, height+20);
        sliderbg.fillColor = "#ffffff";
        var slider = new scope.Raster("/static/images/timebar.png", [width/2,height+10]);

        handleBarLeft = new scope.Path.Line(new scope.Point(timeToPixel(0,0), height), new scope.Point(timeToPixel(0,0), 0));
        handleBarLeft.strokeColor = new scope.Color(0,0,0,0);
        handleBarLeft.strokeWidth = 1;

        var middleLine = new scope.Path.Line(new scope.Point(0, height/2), new scope.Point(width, height/2));
        middleLine.strokeColor = "#000000";
        middleLine.strokeWidth = 1;

        if(sliderCount >1){
            choosenAreaRect = new scope.Path.Rectangle(timeToPixel(0,0), 0, width-30, height);
            choosenAreaRect.fillColor = {
                gradient: {
                    stops: [[new scope.Color(0,0,0,0.5),0],[new scope.Color(0,0,0,0),0.3],[new scope.Color(0,0,0,0),0.7],[new scope.Color(0,0,0,0.5),1]]
                },
                origin: [width/2,0],
                destination: [width/2,height]
            }
        }

        scope.view.draw();
    }
    var drawHandle = function(){
        paper = scope;
        for(var i = 5; i<91; i=i+5){

            var text = new scope.PointText(new scope.Point(timeToPixel(i,0),height+14));
            text.justification = 'center';
            text.fontSize = 10;
            text.fillColor = 'black';
            text.content = i;

            var line = new scope.Path.Line(new scope.Point(timeToPixel(i,0), 0), new scope.Point(timeToPixel(i,0), 4));
            var line2 = new scope.Path.Line(new scope.Point(timeToPixel(i,0), height), new scope.Point(timeToPixel(i,0), height - 4));
            line.strokeColor = "#000000";
            line2.strokeColor = "#000000";
            line.strokeWidth = 1;
            line2.strokeWidth = 1;
        }
        if(sliderCount > 0){
            leftHandle = new scope.Raster("/static/images/slide-button.png", [timeToPixel(0,0),height+10]);
        }
        if(sliderCount > 1){
            rightHandle = new scope.Raster("/static/images/slide-button.png", [width-10,height+10]);

            handleBarLeft = new scope.Path.Line(new scope.Point(timeToPixel(0,0), height), new scope.Point(timeToPixel(0,0), 0));
            handleBarLeft.strokeColor = "#5887ff";
            handleBarLeft.strokeWidth = 2;

            handleBarRight = new scope.Path.Line(new scope.Point(width-10, height), new scope.Point(width-10, 0));
            handleBarRight.strokeColor = "#5887ff";
            handleBarRight.strokeWidth = 2;
        }

        scope.view.draw();
    }

    var loadMomentum = function(callback){
        $.post("/api/GetMatchMomentum", JSON.stringify({"matchId": match_id})).done(function(data){
            if(isLive){
                maxSecond = 90*60;
            } else {
                maxSecond = data.data[data.data.length-1][0]*60;
            }

            paper = scope;

            if(momentumPath) momentumPath.remove();

            momentumPath = new scope.Path();
            momentumPath.strokeColor = "#76050e";
            momentumPath.strokeWidth = 2;

            var maxAbs = 0;
            _.each(data.data, function(pt){
                maxAbs = Math.max(maxAbs, Math.abs(pt[1]));
            });

            var factor = 0.95/maxAbs;

            _.each(data.data, function(pt){
                var x = timeToPixel(pt[0],0);
                var value = (-pt[1])*factor
                var y = height*(value + 1)/2;
                momentumPath.add(new scope.Point(x, y));
            });
            scope.view.draw();
            callback("");
        });
    }

    var drawTeamLogos = function(home, away){
        paper = scope;
        var homeRaster = new scope.Raster("/static/images/logo"+home+".png");
        var awayRaster = new scope.Raster("/static/images/logo"+away+".png");

        homeRaster.onLoad = function(){
            var scaleFactor = 20/homeRaster.height;
            homeRaster.position = new scope.Point(10, 12);
            homeRaster.scale(scaleFactor);
        };

        awayRaster.onLoad = function(){
            var scaleFactor = 20/awayRaster.height;
            awayRaster.position = new scope.Point(10, 37);
            awayRaster.scale(scaleFactor);
        };
    }

    var loadEvents = function(){
        paper = scope;

        if(eventImagesGroup){
            eventImagesGroup.remove();
        }

        eventImagesGroup = new scope.Group();

        $.post("/api/GetMatchEvents", JSON.stringify({"matchId": match_id})).done(function(data){
            _.each(data.data, function(event){
                if(event[2]===matchInfo.homeId){
                    event.push("home");
                } else if(event[2]===matchInfo.awayId){
                    event.push("away");
                }
                matchEvents.push(event);
                drawEvent(event);
            });
            scope.view.draw();
        });
    }

    var timeToPixel = function(minute, second){
        var totalSeconds = minute*60+second;
        var xratio = totalSeconds/maxSecond;
        return xratio*(width-handleWidth*2)+handleWidth;
    }

    var pixelToTime = function(pos){
        var xratio = (pos-handleWidth)/(width-handleWidth*2);
        var seconds = Math.round(maxSecond*xratio);
        return [Math.floor(seconds/60), seconds%60];
    }

    scope.tool.onMouseDown = function(event){
        if(isLive) return;

        if(leftHandle && leftHandle.hitTest(event.point)){
            draggedHandle = leftHandle;
        } else if(rightHandle && rightHandle.hitTest(event.point)){
            draggedHandle = rightHandle;
        }
    }

    scope.tool.onMouseDrag = function(event){
        if(draggedHandle){

            if(sliderCount > 1){
                if( draggedHandle == leftHandle){
                    if(event.point.x < timeToPixel(0,0)){
                        draggedHandle.position.x = timeToPixel(0,0);
                        handleBarLeft.position.x = timeToPixel(0,0);
                    }
                    else if(pixelToTime(event.point.x)[0]>=75 && pixelToTime(rightHandle.position.x)[0] > 75){
                        draggedHandle.position.x = timeToPixel(75,0);
                        handleBarLeft.position.x = timeToPixel(75,0);
                    }
                    else if(event.point.x > timeToPixel(pixelToTime(rightHandle.position.x)[0] - 15 ,0)){
                        draggedHandle.position.x = timeToPixel(pixelToTime(rightHandle.position.x)[0] - 15 ,0);
                        handleBarLeft.position.x = timeToPixel(pixelToTime(rightHandle.position.x)[0] - 15 ,0);
                    }
                    else{
                        draggedHandle.position.x = event.point.x;
                        var temp = ((pixelToTime(event.point.x)[0]) / 15).toFixed(0);
                        handleBarLeft.position.x = timeToPixel(temp * 15 , 0);
                    }
                }
                else if(draggedHandle == rightHandle){
                    if(event.point.x > width - handleWidth/2 || pixelToTime(handleBarLeft.position.x)[0] > 74){
                        draggedHandle.position.x = width - handleWidth/2;
                        handleBarRight.position.x = width - handleWidth/2;
                    }
                    else if(event.point.x > timeToPixel(82,0) ){
                        draggedHandle.position.x = event.point.x;
                        handleBarRight.position.x = width - handleWidth/2;
                    }
                    else if(event.point.x < timeToPixel(pixelToTime(leftHandle.position.x)[0] + 15 ,0)){
                        draggedHandle.position.x = timeToPixel(pixelToTime(leftHandle.position.x)[0] + 15 ,0);
                        handleBarRight.position.x = timeToPixel(pixelToTime(leftHandle.position.x)[0] + 15 ,0);
                    }
                    else{
                        draggedHandle.position.x = event.point.x;
                        var temp = ((pixelToTime(event.point.x)[0]) / 15).toFixed(0);
                        handleBarRight.position.x = timeToPixel(temp * 15 , 0);
                    }
                }
                choosenAreaRect.bounds = { x: handleBarLeft.position.x, y: 0, width:handleBarRight.position.x - handleBarLeft.position.x, height:height };

            }
            else{
                if(event.point.x < timeToPixel(0,0)){
                    draggedHandle.position.x = timeToPixel(0,0);
                }
                else if(event.point.x > width - handleWidth/2){
                    draggedHandle.position.x = width - handleWidth/2;
                }
                else{
                    draggedHandle.position.x = event.point.x;
                }
                handleBarLeft.remove();
                handleBarLeft = new scope.Path.Line(new scope.Point(draggedHandle.position.x, height), new scope.Point(draggedHandle.position.x, 0));
                handleBarLeft.strokeColor = "#5887ff";
                handleBarLeft.strokeWidth = 2;
                var min = pixelToTime(draggedHandle.position.x)[0];
                handleEventDragOns(min);
                currentPoint = pixelToTime(draggedHandle.position.x);
            }
        }
    }

    var handleEventDragOns = function(min){
        if(min>lastMin+1 || min < lastMin-1){
            for(var i=0;i<eventGroups.length; i++){
                eventGroups[i].removeChildren();
            }
        }
        var imageNames = ["goal.png", "own-goal.png", "penalty.png", "missed-pen.png",
            "yellow.png", "second-yellow.png", "red.png", "substitution.png"];
        var count = 0;
        for( var i=0; i<matchEvents.length; i++){
            var evMin = parseInt(matchEvents[i][1]);
            if(evMin == min){

                lastMin = min;

                var text = "";
                if(matchEvents[i][0] == 7){
                    var sName1 = matchEvents[i][7].split(" ");
                    var sName2 = matchEvents[i][8].split(" ");
                    var playerIn;
                    var playerOut;
                    if (sName1.length > 1){
                        playerOut = sName1[0].charAt(0) + "." +sName1[1];
                    }
                    else{
                        playerOut = sName1[0];
                    }
                    if (sName2.length > 1){
                        playerIn = sName2[0].charAt(0) + "." +sName2[1];
                    }
                    else{
                        playerIn = sName2[0];
                    }
                    text = playerOut + " - " + playerIn;
                }
                else{
                    text = matchEvents[i][7];
                }

                boxWidth = text.length * 6 + 15;

                if(min>45){
                    boxOffset =  0 - (boxWidth/2+10);;
                }
                else{
                    boxOffset = (boxWidth/2+10);
                }

                var eventGroup = new scope.Group();
                eventGroup.addChild(new scope.Path.Rectangle({
                    rectangle: {
                        size: [boxWidth, boxHeight],
                        center: [timeToPixel(min,0)+boxOffset,topPadding+count*(boxHeight+boxPadding)]
                    },
                    radius: 3,
                    fillColor: "#f8f8f8",
                    strokeWidth: 1,
                    strokeColor: "#888888"
                })
                );

                eventGroup.addChild(new scope.Raster("/static/images/"+ imageNames[matchEvents[i][0]], [timeToPixel(min,0)+boxOffset-(boxWidth/2)+5,topPadding+count*(boxHeight+boxPadding)]).scale(0.6));

                eventGroup.addChild( new scope.PointText({
                    point: [timeToPixel(min,0)+boxOffset-(boxWidth/2)+15,topPadding+count*(boxHeight+boxPadding)+fontSize/3],
                    content: text,
                    fillColor: 'black',
                    fontSize: fontSize
                })
                );
                eventGroups.push(eventGroup);
                count++;
            }
        }
    }

    scope.tool.onMouseUp = function(event){
        if(draggedHandle){
            draggedHandle = null;
            var timeData = null;
            if(sliderCount==1){
                timeData = pixelToTime(leftHandle.position.x-(handleWidth/2));
                handleBarLeft.strokeColor = new scope.Color(0,0,0,0);
            } else if(sliderCount==2){
                leftHandle.position.x = handleBarLeft.position.x;
                rightHandle.position.x = handleBarRight.position.x;
                var leftData = pixelToTime(leftHandle.position.x-(handleWidth/2));
                var rightData = pixelToTime(rightHandle.position.x-(handleWidth/2));

                if(leftData[0]>rightData[0]){
                    timeData = [rightData, leftData];
                } else {
                    timeData = [leftData, rightData];
                }
            }

            for(var i=0;i<eventGroups.length; i++){
                eventGroups[i].removeChildren();
            }

            $("#"+div_id).trigger({type:"timeChanged", time: timeData});
        }
    }

    var drawEvent = function(event){
        // Event format:
        // [Event Type, Minute, Team Id, ...]
        // event types:
        // 0 => Goal
        // 1 => Own Goal
        // 2 => Penalty
        // 3 => Missed Penalty
        // 4 => Yellow Card
        // 5 => Second Yellow Card
        // 6 => Red Card
        // 7 => Substitution

        // Todo: differentiate between events, or highlight the entry below on hover/click
        paper = scope;

        var imageNames = ["goal.png", "own-goal.png", "penalty.png", "missed-pen.png",
            "yellow.png", "second-yellow.png", "red.png", "substitution.png"];

        var xoffset = timeToPixel(event[1], 0);
        var yoffset;
        if(event[9]==="home"){
            yoffset = 14;
        } else {
            yoffset = 36;
        }

        var point = new scope.Point(xoffset, yoffset);

        var img = new scope.Raster("/static/images/"+ imageNames[event[0]], point);
        img.scale(0.8);

        var eventGroup = null;
        img.onMouseEnter = function(){

            eventGroup = new scope.Group();

            var text = "";
            if(event[0] == 7){
                var sName1 = event[7].split(" ");
                var sName2 = event[8].split(" ");
                var playerIn;
                var playerOut;
                if (sName1.length > 1){
                    playerOut = sName1[0].charAt(0) + "." +sName1[1];
                }
                else{
                    playerOut = sName1[0];
                }
                if (sName2.length > 1){
                    playerIn = sName2[0].charAt(0) + "." +sName2[1];
                }
                else{
                    playerIn = sName2[0];
                }
                text = playerOut + " - " + playerIn;
            }
            else{
                text = event[7];
            }
            boxWidth = text.length * 6 + 15;

            if(event[1]>45){
                boxOffset = 0 - (boxWidth/2+10);
            }
            else{
                boxOffset = (boxWidth/2+10);
            }

            eventGroup.addChild(new scope.Path.Rectangle({
                rectangle: {
                    size: [boxWidth, boxHeight],
                    center: [timeToPixel(event[1],0)+boxOffset,yoffset]
                },
                radius: 3,
                fillColor: "#f8f8f8",
                strokeWidth: 1,
                strokeColor: "#888888"
            })
            );

            eventGroup.addChild(new scope.Raster("/static/images/"+ imageNames[event[0]], [timeToPixel(event[1],0)+boxOffset-(boxWidth/2)+5,yoffset]).scale(0.6));

            eventGroup.addChild( new scope.PointText({
                point: [timeToPixel(event[1],0)+boxOffset-(boxWidth/2)+15,yoffset+fontSize/3],
                content: text,
                fillColor: 'black',
                fontSize: fontSize
            })
            );
        }
        img.onMouseLeave = function(){
            eventGroup.removeChildren();
        }
        eventImagesGroup.addChild(img);
        eventImages.push(img);
    }

    this.changeTime = function(minute, second){
        if(isLive && second == 0 && minute != 0){
            loadMomentum();
            loadEvents();
        }
    }

    this.moveSlider = function(which, minute, second){
        paper = scope;
        var sliderToMove = null;
        if(which=="left") sliderToMove = leftHandle;
        else if(which=="right") sliderToMove = rightHandle;

        if(draggedHandle == sliderToMove) return;

        sliderToMove.position.x = timeToPixel(minute, second);
        scope.view.draw();
    }

}