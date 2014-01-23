(function($, filepicker, undefined) {
	filepicker.setKey('AxjOdegzSQyWi7pQqR3bnz');

	$('#filepicker').change(function(ev) {
		var file = ev.originalEvent.fpfile;

		$.post('/analyze', {
			file: file.url
		}, function(results) {
			console.log(results);
		});

		console.log(ev, ev.originalEvent, file);
	});
}(jQuery, filepicker));