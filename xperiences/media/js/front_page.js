$(document).ready(function() {
	user_position(function(loc) {
		get_experiences(loc);
	},function() {
		get_experiences();
	});

	$(".default").each(function(i, el) {
		$(el).defaultVal();
	});

});

var data;

function get_experiences(params) {
	params = params || {};
	$.get('/api/experiences/json', params, function(_data){
		data = _data;
		render(_data);
	});
};

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
