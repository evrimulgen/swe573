// setting up the django CSRF cookie
var csrftoken = $.cookie('csrftoken');
$.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

$.get("/api/GetAttributeLookup").done(function(data){
    $("#ajaxResult").append("<div>"+JSON.stringify(data)+"</div>")
});

var postData = JSON.stringify({"player_ids":["180"],"attribute_ids":["11","21"],"number_of_matches":20});
$.post("/api/GetPlayersLastNAttributeValue", postData).done(function(data){
    $("#ajaxResult").append("<div>"+JSON.stringify(data)+"</div>");
});

postData = JSON.stringify({"player_ids":["180"]});
$.post("/api/GetPlayersInformation", postData).done(function(data){
    $("#ajaxResult").append("<div>"+JSON.stringify(data)+"</div>");
});
