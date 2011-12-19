(function($){
	var PARENT_CLASS_NAME = "textwrap-parent";
	var HOLDER_CLASS_NAME = "textwrap-holder";

	$.fn.textWrap = function(className) {
		return this.each(function() { 
			var $this = $(this);
			var curVal = $this.val();
			var value = $this.prop("alt");
			console.log(value);

			var parentDiv = $("<div>");
			parentDiv;
			var valueDiv = $("<div>");
			valueDiv.text(value);
			$this.before(parentDiv);
			$this.remove();
			parentDiv.append($this);
			parentDiv.append(valueDiv);

			parentDiv.css({
				"margin-left": $this.css("margin-left"),
				"margin-right": $this.css("margin-right"),
				"margin-top": $this.css("margin-top"),
				"margin-bottom": $this.css("margin-bottom")
			});

			parentDiv.css({
				"display": "inline-block",
				"width": $this.outerWidth(),
				"position": "relative"
			})

			valueDiv.css({
				"padding-left": parseInt($this.css("padding-left"), 10) + 2,
				"padding-right": $this.css("padding-right"),
				"padding-top": $this.css("padding-top"),
				"padding-bottom": $this.css("padding-bottom"),
				"position": "absolute",
				"top": 0
			});

			if(className) {
				valueDiv.addClass(className);
			}

			$this.css("margin", 0);

			valueDiv.on('click', function(e) {
				$this.focus();
			});

			function keyupHandler(e) {
				var target = $(e.currentTarget);
				if(target.val() != "") {
					valueDiv.css("opacity", 0);
					target.unbind("keyup");
				}	
			}

			var w = $this.width();
			var h = $this.height();

			$this.on('blur', function(e){
				var curEl = $(e.currentTarget);
				if(curEl.val() == '') {
					valueDiv.animate({
						opacity: 1
					}, 300);
				}
				curEl.keyup(keyupHandler);
			});

			$this.keyup(keyupHandler);

			if(curVal != "") {
				valueDiv.css("opacity", 0);
			}
		});

	};
})(jQuery);
