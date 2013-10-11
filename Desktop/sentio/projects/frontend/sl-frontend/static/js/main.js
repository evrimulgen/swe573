/**
 * Created with PyCharm.
 * User: Caner
 * Date: 2/2/13
 * Time: 3:18 PM
 * To change this template use File | Settings | File Templates.
 */

var is_clickable = true;

$(document).ready(function(){
    var kcClickHandler = function (e) {
        var t, n;
        return e.preventDefault(), t = $(this),
            n = t.attr("data-id"),
            t.removeClass("inactive"),
            t.addClass("active"),
            t.html("Aklında!"),
            t.unbind("click"),
            $.ajax({url:"/request/" + n + "/",
                type:'GET',
                success:function (data) {
                    if (data == "match") {
                        t.addClass("success");
                        t.removeClass("inactive");
                        t.html("Hayırlısı :)");
                    }
                },
                error:function () {
                    t.addClass("inactive");
                    t.removeClass("active");
                    t.html("Seç");
                    t.bind("click", kcClickHandler);
                    alert("Hata!");
                }
            })
    };

    $("body a.inactive").bind("click", kcClickHandler);

    $("body a.active").on("click",function(e){
                                var t,n;
                                return e.preventDefault()
                            });
    var $container = $('#friends-container');
    $container.imagesLoaded(function(){
        $container.masonry({
            itemSelector : '.friendbox',
            columnWidth : 230
        });
    });

});

