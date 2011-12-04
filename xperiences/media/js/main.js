
$(document).ready(function(e) {
	$(".default-val").each(function(i, el) {
		$(el).defaultVal();
	})

});

// Prevent errors in browsers without console support
if (!console) {
	console.log = function() {}
}
