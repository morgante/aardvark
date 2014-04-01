(function($, _, filepicker, undefined) {
	filepicker.setKey('AxjOdegzSQyWi7pQqR3bnz');

	var $selection;
	var $results;
	var $list;
	var $progress;
	var rowTemplate;

	function info(file) {
		$.ajax('/analyze', {
			data: {file: file},
			type: 'POST',
			dataType: 'json',
			success: function(results) {
				$progress.slideUp();
				$results.removeClass('hide').slideDown();

				$('#pdf').val(file);

				_.each(results, function(acronym) {
					$list.append(rowTemplate({
						acronym: acronym,
						// definition: _.keys(defs).slice(0,3).join(', ')
					}));
				});
		}});
	}

	function analyze(file) {
		$selection.slideUp();
		$progress.removeClass('hide').slideDown();

		setTimeout(function() {
			info(file);
		}, 2000);
	}


	function init() {
		$selection = $('.selection');
		$progress = $('.progress');
		$results = $('.results');
		$list = $('.list', $results);
		rowTemplate = _.template($('#collect_row').html());

		// analyze('https://www.filepicker.io/api/file/FWK04EbPRjuddZO2qMOM');

		$('#filepicker').change(function(ev) {
			var file = ev.originalEvent.fpfile;

			analyze(file.url);
			
		});
	}

	$(init);
	
}(jQuery, _, filepicker));