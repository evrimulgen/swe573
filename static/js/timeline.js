function Timeline(div_id, match_id){
    var width = 662;
    var height = 50;

    var handleWidth = 20;

    $("#"+div_id).width(width).height(height);

    var scope = new paper.PaperScope();
    scope.setup(div_id);

    var bg = new scope.Path.Rectangle(0, 0, width, height);
    bg.fillColor = "#ccccff";

    var leftHandle = new scope.Path.Rectangle(0, 0, handleWidth, height);
    var rightHandle = new scope.Path.Rectangle(width-handleWidth, 0, handleWidth, height);

    leftHandle.fillColor = "#9999ff";
    rightHandle.fillColor = "#9999ff";

    scope.view.draw();

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
        return [Math.floor(seconds/60), seconds%60]
    }

    scope.tool.onMouseDown = function(event){
        if(leftHandle.hitTest(event.point)){
            draggedHandle = leftHandle;
        } else if(rightHandle.hitTest(event.point)){
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
        console.log(scope);
        var eventWidth = 4;
        var offset = timeToPixel(event[1], 0)-eventWidth/2;

        console.log(event);
        var rect = new scope.Path.Rectangle(offset, 0, eventWidth, height);
        rect.fillColor = "green";
    }

    var loadEvents = function(){
        $.post("/api/GetMatchEvents", JSON.stringify({"matchId": match_id})).done(function(data){
            _.each(data.data, function(event){
                drawEvent(event);
            });
        });
    };

    loadEvents();
}

$(function(){
    new Timeline("slider", 11730068);
});