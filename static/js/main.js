(function($) {

	"use strict";

	$('nav .dropdown').hover(function(){
		var $this = $(this);
		$this.addClass('show');
		$this.find('> a').attr('aria-expanded', true);
		$this.find('.dropdown-menu').addClass('show');
	}, function(){
		var $this = $(this);
			$this.removeClass('show');
			$this.find('> a').attr('aria-expanded', false);
			$this.find('.dropdown-menu').removeClass('show');
	});

})(jQuery);

function makeAnother(){
	document.getElementById('apl2').innerHTML = 'APPROVED';
	document.getElementById('apl2').style.color = "green";
	document.getElementById('apl2').style.fontWeight = 'bold';
} 

let check = document.getElementById('apl').innerHTML;
if(check == "Approve"){
	document.getElementById('apl').innerHTML = 'APPROVED';
	document.getElementById('apl').style.color = "green";
	document.getElementById('apl').style.fontWeight = 'bold';
	makeAnother()
}

function makeAnother2(){
	document.getElementById('apl2').innerHTML = 'REJECTED';
	document.getElementById('apl2').style.color = "red";
	document.getElementById('apl2').style.fontWeight = 'bold';
} 


let check2 = document.getElementById('apl').innerHTML;
if(check2 == "Cancel"){
	document.getElementById('apl').innerHTML = 'REJECTED';
	document.getElementById('apl').style.color = "red";
	document.getElementById('apl').style.fontWeight = 'bold';
	makeAnother2()
}

