(function($, _, filepicker, undefined) {
	filepicker.setKey('AxjOdegzSQyWi7pQqR3bnz');

	var $selection;
	var $results;
	var $list;
	var $progress;
	var rowTemplate;

	function analyze(file) {
		$selection.slideUp();
		$progress.removeClass('hide').slideDown();

		$.ajax('/analyze', {
			data: {file: file},
			type: 'POST',
			dataType: 'json',
			success: function(results) {
				$progress.slideUp();
				$results.removeClass('hide').slideDown();

				_.each(results, function(defs, acronym) {
					$list.append(rowTemplate({
						acronym: acronym,
						definition: _.keys(defs).slice(0,3).join(', ')
					}));
				});
		}});
	}


	function init() {
		$selection = $('.selection');
		$progress = $('.progress');
		$results = $('.results');
		$list = $('.list', $results);
		rowTemplate = _.template($('#acronym_row').html());

		analyze('https://www.filepicker.io/api/file/FWK04EbPRjuddZO2qMOM');

		$('#filepicker').change(function(ev) {
			var file = ev.originalEvent.fpfile;

			analyze(file.url);
			
		});
	}

	$(init);
	
}(jQuery, _, filepicker));