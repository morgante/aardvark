(function($, _, filepicker, undefined) {
	filepicker.setKey('AxjOdegzSQyWi7pQqR3bnz');

	var $selection;
	var $intro;
	var $loading;
	var $glossary;
	var $results;
	var $list;
	var $progress;
	var $header;
	var rowTemplate;

	function info(file) {
		$.ajax('/analyze', {
			data: {file: file},
			type: 'POST',
			dataType: 'json',
			success: function(results) {
				$loading.slideUp();
				$glossary.removeClass('hide').slideDown();

				$('#pdf').val(file);
				
				$header.text('Acronym Glossary');

				_.each(results, function(data) {
					$list.append(rowTemplate(data));
				});
		}});
	}

	function analyze(file) {
		$intro.slideUp();
		$loading.removeClass('hide').slideDown();

		setTimeout(function() {
			info(file);
		}, 2000);
	}


	function init() {
		$selection = $('.selection');
		$progress = $('.progress');
		$results = $('.results');
		$list = $('.list', $results);
		$header = $('h1');
		rowTemplate = _.template($('#acronym_row').html());

		$intro = $('.intro');
		$loading = $('.loading');
		$glossary = $('.glossary');

		$('#filepicker').change(function(ev) {
			var file = ev.originalEvent.fpfile;

			analyze(file.url);
			
		});
	}

	$(init);
	
}(jQuery, _, filepicker));