function update() {

	if(!$('.modal').hasClass('act')) {
	$.ajax({
	  url: '',
	  success: function(data) {	
		$('body').html(data);
	  }
	});
	} else {
	}
}
setTimeout(update,5000)

$('.modal').on('hidden.bs.modal', function (e) {
	$('.modal').removeClass('act')
	setTimeout(update,5000)
})
$('.modal').on('show.bs.modal', function (e) {
	$(this).addClass('act')
})
