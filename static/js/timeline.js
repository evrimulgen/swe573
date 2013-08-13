function Timeline(div_id, match_id){
    var width = 662;
    var height = 50;

    var handleWidth = 20;

    $("#"+div_id).width(width).height(height);

    var scope = new paper.PaperScope();
    paper.setup(div_id);

    var bg = new paper.Path.Rectangle(0, 0, width, height);
    bg.fillColor = "#ccccff";

    var leftHandle = new paper.Path.Rectangle(0, 0, handleWidth, height);
    var rightHandle = new paper.Path.Rectangle(width-handleWidth, 0, handleWidth, height);

    leftHandle.fillColor = "#9999ff";
    rightHandle.fillColor = "#9999ff";

    $.post("/api/GetMatchEvents", JSON.stringify({"matchId": match_id})).done(function(data){
        _.each(data.data, function(event){
            console.log(event);
        });
    });

    paper.view.draw();

    var currentPoint = [0,0];
    var maxSecond = 90*60;

    var draggedHandle = null;

    paper.tool.onMouseDown = function(event){
        if(leftHandle.hitTest(event.point)){
            draggedHandle = leftHandle;
        } else if(rightHandle.hitTest(event.point)){
            draggedHandle = rightHandle;
        }
    }

    paper.tool.onMouseDrag = function(event){
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
            var xratio = (draggedHandle.position.x-(handleWidth/2))/(width-handleWidth);
            var seconds = Math.round(maxSecond*xratio);
            currentPoint = [Math.floor(seconds/60), seconds%60];
            console.log(currentPoint);
        }
    }

    paper.tool.onMouseUp = function(event){
        if(draggedHandle){
            draggedHandle = null;
        }
    }
}

$(function(){
    new Timeline("slider", 11730068);
});