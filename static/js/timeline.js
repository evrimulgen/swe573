function Timeline(options){
    var div_id = options.divId;
    var match_id = options.matchId;
    var sliderCount = options.sliderCount;
    var scope = options.paperScope;

    var width = 662;
    var height = 50;

    var handleWidth = 20;

    $("#"+div_id).width(width).height(height);

    scope.setup(div_id);

    // setting up the django CSRF cookie
    var csrftoken = $.cookie('csrftoken');
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    var bg = new scope.Path.Rectangle(0, 0, width, height);
    bg.fillColor = "#ccccff";

    var leftHandle = null;
    var rightHandle = null;
    if(sliderCount > 0){
        leftHandle = new scope.Path.Rectangle(0, 0, handleWidth, height);
        leftHandle.fillColor = "#9999ff";
    }
    if(sliderCount > 1){
        rightHandle = new scope.Path.Rectangle(width-handleWidth, 0, handleWidth, height);
        rightHandle.fillColor = "#9999ff";
    }

    scope.view.draw();
    var scope_id = scope._id;

    var currentPoint = [0,0];
    var maxSecond = 90*60;

    var draggedHandle = null;

    var timeToPixel = function(minute, second){
        var totalSeconds = minute*60+second;
        var xratio = totalSeconds/maxSecond;
        return xratio*(width-handleWidth)+handleWidth/2;
    }

    var pixelToTime = function(pos){
        var xratio = pos/(width-handleWidth);
        var seconds = Math.round(maxSecond*xratio);
        return [Math.floor(seconds/60), seconds%60];
    }

    scope.tool.onMouseDown = function(event){
        if(leftHandle && leftHandle.hitTest(event.point)){
            draggedHandle = leftHandle;
        } else if(rightHandle && rightHandle.hitTest(event.point)){
            draggedHandle = rightHandle;
        }
    }

    scope.tool.onMouseDrag = function(event){
        if(draggedHandle){
            if(event.point.x < handleWidth/2){
                draggedHandle.position.x = handleWidth/2;
            }
            else if(event.point.x > width - handleWidth/2){
                draggedHandle.position.x = width - handleWidth/2;
            }
            else{
                draggedHandle.position.x = event.point.x;
            }
            currentPoint = pixelToTime(draggedHandle.position.x-(handleWidth/2));
        }
    }

    scope.tool.onMouseUp = function(event){
        if(draggedHandle){
            draggedHandle = null;
            var timeData = null;
            if(sliderCount==1){
                timeData = pixelToTime(leftHandle.position.x-(handleWidth/2));
            } else if(sliderCount==2){
                var leftData = pixelToTime(leftHandle.position.x-(handleWidth/2));
                var rightData = pixelToTime(rightHandle.position.x-(handleWidth/2));

                if(leftData[0]>rightData[0]){
                    timeData = [rightData, leftData];
                } else {
                    timeData = [leftData, rightData];
                }
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

        var eventWidth = 4;
        var offset = timeToPixel(event[1], 0);

        var rect = new scope.Path.Rectangle(offset, 0, eventWidth, height);
        rect.fillColor = "green";
    }

    var loadEvents = function(){
        $.post("/api/GetMatchEvents", JSON.stringify({"matchId": match_id})).done(function(data){
            _.each(data.data, function(event){
                drawEvent(event);
            });
            scope.view.draw();
        });

    };

    this.moveSlider = function(which, minute, second){
        paper = scope;
        var sliderToMove = null;
        if(which=="left") sliderToMove = leftHandle;
        else if(which=="right") sliderToMove = rightHandle;

        if(draggedHandle == sliderToMove) return;

        sliderToMove.position.x = timeToPixel(minute, second);
        scope.view.draw();
    }

    loadEvents();
}