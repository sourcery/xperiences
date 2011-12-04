
var ANIMATE_INTERVAL = 6000;
var intervalIndex;

$(document).ready(function() {
	var mainImg = $("#exp-main-image");
	var thumbs = $(".exp-thumbs-img");
	var thumbswrapper = $("#exp-thumbs");

	var thumbW = thumbs.first().outerWidth(true);
	var thumbH = thumbs.first().outerHeight(true);
	thumbswrapper.css("width", thumbW * (thumbs.length - 1));
	thumbswrapper.css("height", thumbH);

	thumbs.each(function(index, el) {
		$(el).css({
			"position": "absolute",
			"left": (index - 1) * thumbW
		});
	});

	intervalIndex = window.setInterval(function() {
		var thumbs = $(".exp-thumbs-img");
		var first = thumbs.first();
		var second = first.next();
		first.remove();
		first.css({
			"left": (thumbs.length - 1) * thumbW
		})
		var w = thumbW;
		thumbswrapper.append(first);
		thumbs.each(function(index, el) {
			$(el).animate({
				"left": "-=" + thumbW
			})
		});
		setMainImage(second.prop("src"));
	}, ANIMATE_INTERVAL);

	thumbs.live("click", function(e) {
		setImageToMain($(e.currentTarget));
	})

	setMainImage(thumbs.first().prop("src"));
});

function setImageToMain(item) {
	var thumbs = $(".exp-thumbs-img");
	var index = item.prevAll("img").length;
	if (index >= thumbs.length) return;

	var thumbswrapper = $("#exp-thumbs");
	var w = thumbs.first().outerWidth(true);

	var first = thumbs.first();
	first.remove();
	first.css({
		"left": item.css('left')
	});
	item.before(first)

	setMainImage(item.prop("src"));	

	item.animate({
		"opacity": 0
	}, {
		"complete": function() {
			item.remove();
			thumbswrapper.prepend(item);
			item.css({
				"first": -w,
				"opacity": ""	
			});
		}
	});
}

function setMainImage(imgPath) {
	var mainImg = $("#exp-main-image");
	var oldImage = mainImg.children("img");
	var newImage = $("<img>").addClass("main-image").prop("src", imgPath);
	mainImg.prepend(newImage);
	if(oldImage.length > 0) {
		oldImage.animate({
			"opacity": 0	
		},{
			"complete": function() {
				oldImage.remove();
			}
		})
	}
}

$.prototype.cjObjectScaler = function(params)
{
	image_autoscale($(this), params);
}

function image_autoscale(obj, params)
{

    params = params || {};
    var fadeIn = params['fade'] || 800;
    obj.css({width:'', height:''});
    obj.load(function()
    {
        var elm = $(this);
        var parent = $(elm.parent());
        var parent_width = parent.innerWidth();
        var parent_height = parent.innerHeight();
        var parent_prop = parent_width * 1.0 / parent_height;
        parent.css({position:'relative;', overflow:'hidden'});

        var width = elm.width();
        var height = elm.height();
        var prop = width * 1.0 / height;
        var top=0.0, left=0.0;
        if( prop < parent_prop)
        {
            width = parent_width;
            height = width / prop;
            top = (parent_height - height)/2;
        }
        else
        {
            height = parent_height;
            width = height * prop;
            left = (parent_width - width)/2;
        }

        elm.css({position:'absolute', width:width, height:height, top:top, left:left});
        elm.fadeIn(800)
    });

    obj.load();
}