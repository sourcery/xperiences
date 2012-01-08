$(document).ready(function() {
    var query_params = read_query_string();
    $('#lat_field').val(query_params['lat']);
    $('#lng_field').val(query_params['lng']);
    $('#address_field').val(query_params['address']);
    $('#keywords_field').val(query_params['keywords']);
    if(!query_params['lat'] || !query_params['lng'])
    {
        user_position(function(loc) {
            for(var k in loc)
                query_params[k] = loc[k];
            get_experiences(query_params);
        },function() {
            get_experiences(query_params);
        });
    }
    else
    {
        get_experiences(query_params);
    }
	$(".default").textWrap("holder");
    address_autocomplete('address_field',null,function(place){
        $('#lat_field').val(place.geometry.location.lat());
        $('#lng_field').val(place.geometry.location.lng());
    });
});

function read_query_string()
{
    var querystr;
    var parts = window.location.href.split('?');
    if( parts.length != 2)
        querystr = '';
    else
    {
        var q_set_split = parts[1].split('#');
        querystr = q_set_split[0];
    }
    parts = querystr.split('&');
    var query_params = {};
    for( var i =0; i<parts.length; i++)
    {
        query_params[decodeURIComponent(parts[i].split('=')[0])] = decodeURIComponent(parts[i].split('=')[1]).replace(/\+/g,' ');
    }
    return query_params;
}

var data;
var meta;
var last_params;

function get_experiences(params) {
	params = params || {};
    params['max_distance'] = 1000;
    params['limit'] = 2;
    last_params = params;
	$.get('/api/experiences/json', params, function(_data){
		data = _data.objects;
        meta = _data.meta;
		render(data,meta);
	});
}


function render(data) {
	var totalWidth = $(window).width() - 20;

	var REQ_MARGIN = 6;

	var MAX_WIDTH = 400;
	var number = Math.floor((totalWidth - REQ_MARGIN) / MAX_WIDTH);

	var remnant = totalWidth - number * MAX_WIDTH;

	imgGrid = $(".image-grid");
	imgGrid.empty();

	var uls = [];
	for (var i = 0; i < number; i++) {
		var ul = $("<ul>").addClass("front-page-col");
		$(".image-grid").append(ul);
		uls.push(ul);
	}

	var margin = (remnant * 0.8) / (number * 2);

	$(".front-page-col").css({
		"margin-left": REQ_MARGIN,
		"margin-right": REQ_MARGIN
	});


	for (var i = 0; i < data.length; i++) {
		$("#test-template").tmpl(data[i]).appendTo(uls[i % number]);
	}

	$(".front-page-item").css({
		"margin": REQ_MARGIN,
	});

	$(".image-grid").css("width", number*MAX_WIDTH + REQ_MARGIN * number * 2)
	// $('#test-template').tmpl(data).appendTo('ul.image-gallery');
}

$(window).resize(function(e){
	if(data != null) {
		render(data);
	}
})


$(document).scroll(function(e){
	var top = $(e.currentTarget).scrollTop();
	if (top > 30) {
		$("#search-box").addClass("has-shadow");
	} else {
		$("#search-box").removeClass("has-shadow");
	}
});
