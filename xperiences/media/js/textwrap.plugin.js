(function($){
	$.fn.defaultVal = function() {
		var curVal = this.val();
		var value = this.prop("alt");
		var self = this;

		var parentDiv = $("<div>");
		parentDiv.addClass("default-val-parent");
		var valueDiv = $("<div>");
		valueDiv.addClass("default-val-text").text(value);
		this.before(parentDiv);
		this.remove();
		parentDiv.append(this);
		parentDiv.append(valueDiv);

		parentDiv.css({
			"margin-left": this.css("margin-left"),
			"margin-right": this.css("margin-right"),
			"margin-top": this.css("margin-top"),
			"margin-bottom": this.css("margin-bottom")
		});

		parentDiv.css({
			"display": "inline-block",
			"width": this.outerWidth()
		})

		valueDiv.css({
			"padding-left": this.css("padding-left"),
			"padding-right": this.css("padding-right"),
			"padding-top": this.css("padding-top"),
			"padding-bottom": this.css("padding-bottom")
		})

		this.css("margin", 0);

		valueDiv.on('click', function(e) {
			self.focus();
		});

		this.on("focus", function(e) {
			valueDiv.animate({
				opacity: 0
			}, 300);
		});

		var w = this.width();
		var h = this.height();

		this.on('blur', function(e){
			var curEl = $(e.currentTarget);
			if(curEl.val() == '') {
				valueDiv.animate({
					opacity: 1
				}, 300);
			}
		});

		if(curVal != "") {
			valueDiv.css("opacity", 0);
		}

	};
})(jQuery);
