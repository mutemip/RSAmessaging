
	function copy(element) {
		var $temp = $("<input>");
		$("content").append($temp);
		$temp.val($(element).text()).select();
		document.execCommand("copy");
		$temp.remove();
	}
		$(document).ready(function(){
	$("#button1").click(function(event){

event.preventDefault();
	});
	$("#button2").click(function(event){

event.preventDefault();
	});

		});


