var ANIMATE_INTERVAL = 6000;
var intervalIndex;

var wrapperW;
var wrapperH;

$(document).ready(function() {
	var close = $("#header-notice-close");
	if(close.length > 0) {
		var show = $.cookie("header_show");
		if(show != "off") {
			$("#header-notice-bar").css("display", "block");
			close.click(function(e) {
				e.stopPropagation();
				$.cookie("header_show", "off");
				$("#header-notice-bar").css("display", "none");
			});
		}

	}

	$.cookie("show_header");

	var mainImg = $("#exp-main-image");
	var thumbs = $(".exp-thumbs-img");
	var thumbswrapper = $("#exp-thumbs");

	if(thumbs.length > 0) {
		wrapperW = mainImg.width();
		wrapperH = mainImg.height();
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
			});
			var w = thumbW;
			thumbswrapper.append(first);
			thumbs.each(function(index, el) {
				$(el).animate({
					"left": "-=" + thumbW
				});
			});
			setMainImage(second.prop("src"));
		}, ANIMATE_INTERVAL);

		thumbs.live("click", function(e) {
			setImageToMain($(e.currentTarget));
		});

		setMainImage(thumbs.first().prop("src"));
	}


});

function delete_message(sender, message_id)
{
    $.ajax({ type:'DELETE', url : '/api/message/' + message_id + '/json', success:function(data)
    {
        var li = $(sender).parents('li');
        li.slideUp(800,function()
        {
            if(li.siblings().length)
                li.remove();
            else
                $(li.parent()).html('<li class="empty-inbox">Your inbox is empty!</li>');
        });
    }, error: function(err){
        //alert(err);
    }});
}

function send_message_dialog(merchant_id)
{
     open_dialog({ template: 'send_message_template', submit:function(dialog){
         var dict = read_input_params(dialog);
         if(dict.title == '' || dict.message == '')
            return false;
         dict['to__id'] = merchant_id;
         var on_complete = function(response) {
             $.get('/accounts/facebook_login/done/', response.authResponse, function()
             {
                 $.ajax({url:'/api/message/json',data:dict,type:'POST',
                     success:function()
                     {
                         message_dialog('message sent');
                     },
                     error: function(err){
                         alert(err);
                     }
                 });
            });
         };
         FB.login(on_complete, {'scope' : _FB_SCOPE });
     }});
}
function read_input_params(elm)
{
    var dict = {};
    $('input,textarea',elm).each(function()
    {
        var input = $(this);
        var key = input.attr('name');
        var value = input.val();
        dict[key] = value;
    });
    return dict;
}
function message_dialog(message)
{
    open_dialog({template:'message_box', data:{'message':message}});
}

function open_dialog(params)
{
    var dialog;

    function close_dialog()
    {
        $('body>.active_dialog,body>.shadow_div').fadeOut(300,function() { $(this).remove(); });
    }
    function on_cancel()
    {
        if(params.cancel)
            if(params.cancel(dialog) ===false)
                return;
        close_dialog();
    }

    params = params || {};
    var data = params.data || {};
    $('body>.active_dialog').remove();
    var shadow = $('<div class="shadow_div" style="background-color:gray; opacity:0.4; width:100%; height:100%; position:absolute; z-index:100;">&nbsp;</div>');
    shadow.css({height:$('body').outerHeight()});
    shadow.prependTo('body');
    shadow.click(on_cancel);

    dialog = $('#' + params.template).tmpl(data);
    dialog.css({display:'none'});
    dialog.prependTo('body');
    dialog.addClass('active_dialog');
    var width = dialog.outerWidth();
    var height = dialog.outerHeight();
    var w = $(window);
    var top = w.height()/2 + w.scrollTop() - height/2;
    var left = w.width()/2 - width/2;
    dialog.css( { position:'absolute', left:left, top:top ,'z-index':101 } );
    dialog.show('fast', function ()
    {
        if(params.load)
            params.load(dialog);
    });
    $('.dialog_cancel', dialog).click( on_cancel );
    $('.dialog_submit', dialog).click(function()
    {
        if(params.submit)
            if(params.submit(dialog)===false)
                return;
        close_dialog();
    });
}

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
	newImage.css("width", 610);
	mainImg.prepend(newImage);
	var h = newImage.width();
	var w = newImage.height();
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

// Prevent errors in browsers without console support
if (!console) {
	var console = {
		log: function() {}
	}
}

$.prototype.cjObjectScaler = function(params)
{
    var obj = $(this);
    if(obj.length)
        image_autoscale(obj, params);
}

function image_autoscale(obj, params)
{

    params = params || {};
    var fadeIn = params['fade'] || 800;
    obj.css({width:'', height:''}).hide();
    obj.load(function()
    {
        var elm = $(this);
        var parent = $(elm.parent());
        parent.css({'overflow':'hidden'});
        var parent_width = parent.innerWidth();
        var parent_height = parent.innerHeight();
        var parent_prop = parent_width * 1.0 / parent_height;
        parent.css({position:'relative'});

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
