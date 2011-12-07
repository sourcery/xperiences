(function($){
	$.fn.defaultVal = function() {
		var value = this.val();
		var self = this;
		if(value) {
			var parentDiv = $("<div>");
			parentDiv.addClass("default-val-parent");
			var valueDiv = $("<div>");
			valueDiv.addClass("default-val-text").text(value);
			this.before(parentDiv);
			this.remove();
			this.val("");
			parentDiv.append(this);
			parentDiv.append(valueDiv);

			valueDiv.on('click', function(e) {
				self.focus();
			});

			this.on("focus", function(e) {
				valueDiv.animate({
					opacity: 0
				});
			});

			var w = this.width();
			var h = this.height();

			this.on('blur', function(e){
				var curEl = $(e.currentTarget);
				if(curEl.val() == '') {
					valueDiv.animate({
						opacity: 1
					});
				}
			});
		}
	};
})(jQuery);
