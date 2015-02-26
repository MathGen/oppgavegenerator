// Common variables
var Q_INPUT					= '#q_input_mathquill';
var S_INPUT					= '#s_input_mathquill_';
var A_INPUT					= '#a_input_mathquill_';
var C_INPUT					= '#c_input_mathquill';
var STEP					= 1;
var ANSWER					= 1;
var SUB						= 1;
var c_count 				= 0;
var array_calc				= [];

$(document).ready(function() {
	// Common variables
	var q_input					= $('#q_input_mathquill');
	var input_field				= "";

	// Topic selection validation
	var category_selection = $('#category_selection');
	category_selection.change(function() {
		if(TOPIC_SELECTED == false){
			$('#category_selection').removeClass('select_error');
			TOPIC_SELECTED = true;
		}
	});

	// Insert text
	var t_btn_ok = $('#t_btn_ok');
	$(t_btn_ok).click(function(e){
		e.preventDefault();
		var t_input = $('#t_input').val();
		$(Q_INPUT).mathquill('cmd', '\\text').mathquill('cmd', t_input);
		$('#t_input').val("");
		var custom_tab_event = $.Event('keydown');
		custom_tab_event.bubbles = true;
		custom_tab_event.cancelable = true;
		custom_tab_event.keyCode = 9;
		$(Q_INPUT).trigger(custom_tab_event);
	});
	
	// Cancel text-input
	var t_btn_cancel = $('.btn_close_text');
	$(t_btn_cancel).click(function(e){
		e.preventDefault();
		$('#t_input').val("");
	});
	
	// Open text-input with focus
	var btn_text = $('#q_btn_text')
	$(btn_text).click(function(e){
		$('#text_modal').on('shown.bs.modal', function () {
			$('#t_input').focus();
		});
	});
	
	// Insert new variable
	var q_btn_var = $('#q_btn_var');
	var q_btn_var_dyn = $('#q_btn_var_dyn');
	var s_btn_var_dyn = $('#s_btn_var_dyn');
	$(q_btn_var).click(function(e){
		e.preventDefault();
		var var_available = false;
		var q_var = "a";
		var q_var_id = 0;
		while(var_available == false){
			if($('#q_btn_abc_' + q_var_id).length || q_var == "e" || q_var == "f"){
				q_var = String.fromCharCode(q_var.charCodeAt(0) + 1);
				q_var_id++;
			}
			else{
				var_available = true;
			}
		}
		$(Q_INPUT).mathquill('write', q_var);
		$(Q_INPUT).find('var').each(function(){
		if($(this).html() == q_var){
			$(this).attr('id', 'R' + q_var_id).addClass('content_var');
			}
		});
		$(q_btn_var_dyn).append('<button id="q_btn_abc_'+q_var_id+'" class="btn btn-danger btn_var_abc">'+q_var+'</button>');
		$(s_btn_var_dyn).append('<button id="s_btn_abc_'+q_var_id+'" class="btn btn-danger btn_var_abc">'+q_var+'</button>');
		$(c_btn_var_dyn).append('<button id="c_btn_abc_'+q_var_id+'" class="btn btn-danger btn_var_abc">'+q_var+'</button>');
		$(a_btn_var_dyn).append('<button id="a_btn_abc_'+q_var_id+'" class="btn btn-danger btn_var_abc">'+q_var+'</button>');
		q_var = String.fromCharCode(q_var.charCodeAt(0) + 1);
		q_var_id++;
	});
	
	// Insert variable a,b,c,..
	$(document).on('click', '.btn_var_abc', function(e){
		e.preventDefault();
		var id = parseInt($(this).attr("id").match(/[\d]+$/)); // Retrieve the number-id
		var tmp_var = "a";
		tmp_var = String.fromCharCode(tmp_var.charCodeAt(0) + id);
		$(get_input_field(this)).mathquill('write', tmp_var);
		$(get_input_field(this)).find('var').each(function(){
		if($(this).html() == tmp_var){
			$(this).attr('id', 'R' + id).addClass('content_var');
			}
		});
	});
	
	// Insert unknown x,y,z
	var btn_x = $('.btn_x');
	$(btn_x).click(function(e){
		e.preventDefault();
		var id = parseInt($(this).attr("id").match(/[\d]+$/));
		var tmp_x = "x";
		tmp_x = String.fromCharCode(tmp_x.charCodeAt(0) + id);
		$(get_input_field(this)).mathquill('write', tmp_x);
		$(get_input_field(this)).find('var').each(function(){
		if($(this).html() == tmp_x){
			$(this).addClass('content_x');
			}
		});
	});
	
	// Insert equal sign
	var btn_equal = $('.btn_equal');
	$(btn_equal).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '=');
	});
	
	// Insert parentheses operator
	var q_btn_par = $('.btn_par');
	$(q_btn_par).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '\\left(\\right)');
	});
	
	// Insert addition operator
	var q_btn_addition = $('.btn_addition');
	$(q_btn_addition).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '+');
	});
	
	// Insert subtraction operator
	var q_btn_subtraction = $('.btn_subtraction');
	$(q_btn_subtraction).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '-');
	});
	
	// Insert multiplication operator
	var q_btn_multiplication = $('.btn_multiplication');
	$(q_btn_multiplication).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '\\cdot');
	});
	
	// Insert division operator
	var q_btn_division = $('.btn_division');
	$(q_btn_division).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '\\frac{}{}');
	});
	
	// Insert exponent
	var q_btn_exponent = $('.btn_exponent');
	$(q_btn_exponent).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '^{}');
	});
	
	// Insert subscript
	var q_btn_subscript = $('.btn_subscript');
	$(q_btn_subscript).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '_{}');
	});
	
	// Insert square root
	var q_btn_sqrt = $('.btn_sqrt');
	$(q_btn_sqrt).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '\\sqrt{}');
	});
	
	// Insert integral
	var q_btn_integral = $('.btn_int');
	$(q_btn_integral).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '\\int\\left(\\right)');
	});
	
	// Insert integral a^b
	var q_btn_integral_ab = $('.btn_int_ab');
	$(q_btn_integral_ab).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '\\int_{}^{}\\left(\\right)');
	});
	
	// Insert calculated A,B,C,..
	$(document).on('click', '.btn_calc', function(e){
		var id = parseInt($(this).attr("id").match(/[\d]+$/));
		var tmp_char = "A";
		tmp_char = String.fromCharCode(tmp_char.charCodeAt(0) + id);
		$(get_input_field(this)).mathquill('write', tmp_char);
		$(get_input_field(this)).find('var').each(function(){
		if($(this).html() == tmp_char){
			$(this).addClass('content_calc');
			}
		});
	});
	
	// Erase last input
	var btn_delete = $('.btn_delete');
	$(btn_delete).click(function(e){
		e.preventDefault();
		var custom_del_event = $.Event('keydown');
		custom_del_event.bubbles = true;
		custom_del_event.cancelable = true;
		custom_del_event.keyCode = 8;
		$(get_input_field(this)).trigger(custom_del_event);
		var id = $(this).attr('id');
		var id_group = id[0];
		if(id_group == 'q'){
			var check_char = [];
			var check_id = [];
			for(var i = 0; i < 23; i++){
				if($('#q_btn_abc_' + i).length > 0){
					check_char.push($('#q_btn_abc_' + i).html());
					check_id.push(i);
				}
			}
			for(var n = 0; n < check_char.length; n++){
				found = false;
				$(Q_INPUT).find('var').each(function(){
					if($(this).html() == check_char[n]){
						found = true;
					}
				});
				if(!found){
					$('#q_btn_abc_' + check_id[n]).remove();
					$('#s_btn_abc_' + check_id[n]).remove();
					$('#c_btn_abc_' + check_id[n]).remove();
				}
			}
		}
		//$(get_input_field(this)).find('textarea').focus();
	});
	
	// Clear input
	var btn_clear = $('.btn_clear');
	$(btn_clear).click(function(e){
		e.preventDefault();
		var btn_id = $(this).attr('id');
		btn_id = btn_id[0];
		if(btn_id == 'q'){
			$(Q_INPUT).mathquill('revert').mathquill('editable');
			$('.btn_var_abc').remove();
		}
		else{
			$(get_input_field(this)).mathquill('revert').mathquill('editable');
		}
		//$(get_input_field(this)).find('textarea').focus();
	});
	
	// Add required ids/classes to manually typed variables
	$('.input_mathquill').keyup(function(e){
		var id = $(this).attr('id');
		var id_group = id[0];
		if(e.keyCode == 88 || e.keyCode == 89 || e.keyCode == 90){
			if(id_group != 'c'){
				$('#' + id).find('var').each(function(){
					if($(this).hasClass('content_x') || $(this).hasClass('content_var') || $(this).hasClass('florin') || $(this).html() == 'e'){}
					else{
						if(isUpperCase($(this).html())){}
						else{
							if($(this).html() == 'x' || $(this).html() == 'y' || $(this).html() == 'z'){
								$(this).addClass('content_x');
							}
						}
					}
				});
			}
		}
		else if(e.keyCode >= 65 && e.keyCode <= 87 && e.keyCode != 69 && e.keyCode != 70){
			var var_id = e.keyCode - 65;
			if(id_group == 'q'){
				$('#' + id).find('var').each(function(){
					if($(this).hasClass('content_x') || $(this).hasClass('content_var') || $(this).hasClass('florin') || $(this).html() == 'e'){}
					else{
						if(isUpperCase($(this).html())){}
						else{
							$(this).attr('id', 'R' + var_id).addClass('content_var');
							if($('#q_btn_abc_' + var_id).length){}
							else{
								var tmp_var_typed = "a";
								tmp_var_typed = String.fromCharCode(tmp_var_typed.charCodeAt(0) + var_id);
								$(q_btn_var_dyn).append('<button id="q_btn_abc_'+var_id+'" class="btn btn-danger btn_var_abc">'+tmp_var_typed+'</button>');
								$(s_btn_var_dyn).append('<button id="s_btn_abc_'+var_id+'" class="btn btn-danger btn_var_abc">'+tmp_var_typed+'</button>');
								$(c_btn_var_dyn).append('<button id="c_btn_abc_'+var_id+'" class="btn btn-danger btn_var_abc">'+tmp_var_typed+'</button>');
							}
						}
					}
				});
			}
			else{
				$('#' + id).find('var').each(function(){
					if($(this).hasClass('content_x') || $(this).hasClass('content_var') || $(this).hasClass('florin') || $(this).html() == 'e'){}
					else{
						if(isUpperCase($(this).html())){
							if($('#s_btn_calc_' + var_id).length){
								if($(this).html() == $('#s_btn_calc_' + var_id).html()){
									$(this).addClass('content_calc');
								}
							}
						}
						else{
							if($('#q_btn_abc_' + var_id).length){
								if($(this).html() == $('#q_btn_abc_' + var_id).html()){
									$(this).attr('id', 'R' + var_id).addClass('content_var');
								}
							}
						}
					}
				});
			}
		}
		// Delete unused variable-buttons
		else if(e.keyCode == 8 || e.keyCode == 46)
		{
			if(id_group == 'q'){
				var check_char = [];
				var check_id = [];
				for(var i = 0; i < 23; i++){
					if($('#q_btn_abc_' + i).length > 0){
						check_char.push($('#q_btn_abc_' + i).html());
						check_id.push(i);
					}
				}
				for(var n = 0; n < check_char.length; n++){
					found = false;
					$('#' + id).find('var').each(function(){
						if($(this).html() == check_char[n]){
							found = true;
						}
					});
					if(!found){
						$('#q_btn_abc_' + check_id[n]).remove();
						$('#s_btn_abc_' + check_id[n]).remove();
						$('#c_btn_abc_' + check_id[n]).remove();
					}
				}
			}
		}
		else if(e.keyCode == 13){
			if(id_group == 't'){
				$('#t_btn_ok').click();
			}
			else if(id_group == 'c'){
				$('#c_btn_ok').click();
			}
			else{
				$('#' + id_group + '_btn_proceed').click();
			}
		}
	});
	
	// Proceed to next panel
	var btn_proceed = $('.btn_proceed');
	$(btn_proceed).click(function(e){
		e.preventDefault();
		var btn_id = $(this).attr('id');
		btn_id = btn_id[0];
		if(btn_id == 'q'){
			if(TOPIC_SELECTED){
				$('.btn-group-q').prop('disabled', true);
				$(s_panel).fadeIn();
			}
			else{
				$('#category_selection').addClass('select_error');
			}
		}
		else if(btn_id == 's'){
			$('.btn-group-s').prop('disabled', true);
			$('#a_panel').fadeIn();
		}
		else if(btn_id == 'a'){
			$('.btn-group-a').prop('disabled', true);
			$('#o_panel').fadeIn();
		}
	});
	
	// New solution step
	var s_btn_next = $('#s_btn_next');
	$(s_btn_next).click(function(e){
		e.preventDefault();
		if(STEP < ($('.step').length)){
			$('#s_btn_del_' + STEP).hide();
			STEP++;
			$('#step_' + STEP).fadeIn();
		}
	});
	
	// Add another answer
	var a_btn_next = $('#a_btn_next');
	$(a_btn_next).click(function(e){
		e.preventDefault();
		if(ANSWER < ($('.answer').length)){
			if(ANSWER == 1){
				$('#ans_title_1').show();
			}
			$('#a_btn_del_' + ANSWER).hide();
			ANSWER++;
			$('#answer_' + ANSWER).fadeIn();
		}
	});

	// Add another text-substitution
	var e_btn_next = $('#e_btn_next');
	e_btn_next.click(function(e){
		e.preventDefault();
		var e_form = $('#e_form');
		$('#e_btn_del_' +SUB).hide();
		SUB++;
		e_form.append('<div id="e_sub_'+SUB+'" style="display:none"><hr><div class="form-group"><label class="col-md-4 control-label">Bytt ut ord/setning:</label><div class="col-md-7"><input id="e_from_'+SUB+'" type="text" class="form-control" placeholder="Epler"></div><div class="col-md-1"><a id="e_btn_del_'+SUB+'" class="glyphicon glyphicon-remove del_sub" style="float:right"></a></div></div><div class="form-group"><label class="col-md-4 control-label">Med ord/setning:</label><div class="col-md-7"><textarea id="e_to_'+SUB+'" type="text" class="form-control" rows="2" placeholder="Bananer, P&#xE6;rer, Appelsiner, Druer"></textarea></div></div></div>');
		$('#e_sub_' + SUB).fadeIn();
	});

	// Delete last text-substitution
	$(document).on('click', '.del_sub', function(e){
		e.preventDefault();
		$('#e_sub_' + SUB).remove();
		SUB--;
		$('#e_btn_del_' +SUB).show();
	});

	// Delete solution step
	var s_btn_del_step = $('.del_step');
	$(s_btn_del_step).click(function(e){
		e.preventDefault();
		var btn_id = parseInt($(this).attr("id").match(/[\d]+$/));
		$(get_input_field(this)).mathquill('revert').mathquill('editable');
		$('#step_' + btn_id).fadeOut();
		STEP--;
		$('#s_btn_del_' + STEP).show();
	});
	
	// Delete alternative answer
	var a_btn_del_step = $('.del_answer');
	$(a_btn_del_step).click(function(e){
		e.preventDefault();
		var btn_id = parseInt($(this).attr("id").match(/[\d]+$/));
		if(ANSWER == 2){
			$('#ans_title_1').hide();
		}
		$(get_input_field(this)).mathquill('revert').mathquill('editable');
		$('#answer_' + btn_id).fadeOut();
		ANSWER--;
		$('#a_btn_del_' + ANSWER).show();
	});
	
	// Close panel
	var btn_close = $('.btn_close');
	$(btn_close).click(function(e){
		e.preventDefault();
		var btn_id = $(this).attr('id');
		btn_id = btn_id[0];
		if(btn_id == 's'){
			$('#o_panel').fadeOut();
			$('.btn-group-a').prop('disabled', false);
			for(var i = ANSWER; i > 1; i--){
				$(A_INPUT + ANSWER).mathquill('revert').mathquill('editable');
				$('#answer_' + i).fadeOut();
			}
			ANSWER = 1;
			$(A_INPUT + ANSWER).mathquill('revert').mathquill('editable');
			$('#a_panel').fadeOut();
			$('.btn-group-s').prop('disabled', false);
			for(var i = STEP; i > 1; i--){
				$(get_input_field(this)).mathquill('revert').mathquill('editable');
				$('#step_' + i).fadeOut();
			}
			STEP = 1;
			$(get_input_field(this)).mathquill('revert').mathquill('editable');
			$(s_panel).fadeOut();
			$('.btn-group-q').prop('disabled', false);
		}
		else if(btn_id == 'c'){
			$(C_INPUT).mathquill('revert').mathquill('editable');
		}
		else if(btn_id == 'a'){
			$('#o_panel').fadeOut();
			$('.btn-group-a').prop('disabled', false);
			for(var i = ANSWER; i > 1; i--){
				$(get_input_field(this)).mathquill('revert').mathquill('editable');
				$('#answer_' + i).fadeOut();
			}
			ANSWER = 1;
			$(get_input_field(this)).mathquill('revert').mathquill('editable');
			$('#a_panel').fadeOut();
			$('#ans_title_1').hide();
			$('.btn-group-s').prop('disabled', false);
		}
		else if(btn_id == 'o'){
			$('#o_panel').fadeOut();
			$('.btn-group-a').prop('disabled', false);
		}
	});
	
	// Remove calculated reference buttons
	$(document).on('click', '.btn_calc_del', function(e){
		e.preventDefault();
		$('.btn_calc').remove();
		$('#s_btn_calc_delete').remove();
		$('#a_btn_calc_delete').remove();
		c_count = 0;
		array_calc = [];
	});
	
	// Retrieve and insert calculation to solution
	var c_btn_ok = $('#c_btn_ok');
	$(c_btn_ok).click(function(e){
		e.preventDefault();
		var total_elements = $(C_INPUT).children().length-1;
		if(total_elements != 0){
			if(c_count == 0){
				$('#s_btn_calc_dyn').append('<button id="s_btn_calc_delete" class="btn btn-success btn-xs btn_calc_del"><span class="glyphicon glyphicon-remove"></span></button>');
				$('#a_btn_calc_dyn').append('<button id="a_btn_calc_delete" class="btn btn-success btn-xs btn_calc_del"><span class="glyphicon glyphicon-remove"></span></button>');
			}
			var c_var = "A";
			c_var = String.fromCharCode(c_var.charCodeAt(0) + c_count);
			
			var c_latex = $(C_INPUT).mathquill('latex');
			var la = latex_to_asciimath(c_latex);
			la = la.replace(/\?/g,'');
			la = la.replace(/\@/g,'');
			array_calc.push('@?' + la + '?@');
			$(C_INPUT).mathquill('revert').mathquill('editable');

			$('<button id="s_btn_calc_'+c_count+'" class="btn btn-success btn_calc">'+c_var+'</button>').insertBefore('#s_btn_calc_delete');
			$('#s_btn_calc_' + c_count).popover({
				html: true,
				content: '<img src="http://latex.codecogs.com/svg.latex?'+c_latex+'" border="0"/>',
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
			$('<button id="a_btn_calc_'+c_count+'" class="btn btn-success btn_calc">'+c_var+'</button>').insertBefore('#a_btn_calc_delete');
			$('#a_btn_calc_' + c_count).popover({
				html: true,
				content: '<img src="http://latex.codecogs.com/svg.latex?'+c_latex+'" border="0"/>',
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
			$('#c_btn_calc_dyn').append('<button id="c_btn_calc_'+c_count+'" class="btn btn-success btn_calc">'+c_var+'</button>');
			$('#c_btn_calc_' + c_count).popover({
				html: true,
				content: '<img src="http://latex.codecogs.com/svg.latex?'+c_latex+'" border="0"/>',
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
			c_count++;
		}
	});
	
	// Retrieve all values and save to database
	var o_btn_save = $('#o_btn_save');
	$(o_btn_save).click(function(e){
		e.preventDefault();
		var array_submit = {};
		array_submit['topic']				= $('#category_selection').find(':selected').attr('id');
		array_submit['question_text']		= '`' + latex_to_asciimath($(Q_INPUT).mathquill('latex')) + '`';
		var tmp_solution = [];
		for(var i = 1; i <= STEP; i++){
			if($('#s_text_' + i).val() != ''){
				tmp_solution.push(latex_to_asciimath('\\text{' + $('#s_text_' + i).val() + '}') + '`\\n`' + latex_to_asciimath($(S_INPUT + i).mathquill('latex')));
			}
			else{
				tmp_solution.push(latex_to_asciimath($(S_INPUT + i).mathquill('latex')));
			}
		}
		array_submit['solution']			= '`' + tmp_solution.join('`\\n`') + '`';
		var tmp_answer = [];
		for(var i = 1; i <=ANSWER; i++){
			tmp_answer.push(latex_to_asciimath($(A_INPUT + i).mathquill('latex')));
		}
		array_submit['answer']				= '`' + tmp_answer.join('`§`') + '`';
		var tmp_r_domain = [];
		tmp_r_domain.push($('#opt_range_from').val());
		tmp_r_domain.push($('#opt_range_to').val());
		array_submit['random_domain']		= tmp_r_domain.join(" ");
		array_submit['number_of_decimals']	= $('#opt_decimal').val();
		var tmp_allow_zero = "";
		if($('#opt_allow').is(':checked')){
			tmp_allow_zero = 'true';
		}
		else{
			tmp_allow_zero = 'false';
		}
		array_submit['answer_can_be_zero']	= tmp_allow_zero;
		var array_dict = [];
		var e_empty = true;
		for(var i = 1; i <= SUB; i++){
			var e_from = $('#e_from_' + i).val();
			var e_to = $('#e_to_' + i).val();
			if(e_from != '' && e_to != ''){
				array_dict.push(e_from + '§' + e_to);
				e_empty = false;
			}
		}
		array_dict.sort(function(a,b){
			var s_a = a.split('§');
			var s_b = b.split('§');
			return s_b[0].length - s_a[0].length; // ASC -> a - b; DESC -> b - a
		});
		if(e_empty){
			array_submit['dictionary'] = "";
		}
		else{
			array_submit['dictionary'] = array_dict.join('§');
		}
		array_submit["csrfmiddlewaretoken"] = getCookie('csrftoken');
		array_submit['type'] = 'normal';

		post(/submit/, array_submit);
	});

	//create a drop down list from db values
	var formated_db_topics = "";
	var db_topics = $('#db_topics').html();
	db_topics = db_topics.split('§');
	for(i = 0; i < db_topics.length; i+=2){
		formated_db_topics = db_topics[i+1].charAt(0).toUpperCase() + db_topics[i+1].slice(1);
		category_selection.append('<option id="'+db_topics[i] + '">'+ formated_db_topics +'</option>');
	}

});

/**
* Checks which input field to type in
*/
function get_input_field(obj){
	var btn_id = $(obj).attr('id');
	btn_id = btn_id[0];
	if(btn_id == 'q'){
		return Q_INPUT;
	}
	else if(btn_id == 's'){
		return S_INPUT + STEP;
	}
	else if(btn_id == 'c'){
		return C_INPUT;
	}
	else if(btn_id == 'a'){
		return A_INPUT + ANSWER;
	}
}

/**
* Convert latex to asciimath
*/
function latex_to_asciimath(latex){
	var la = latex;
	la = la.replace(/{/g,'(');
	la = la.replace(/}/g,')');
	la = la.replace(/\\cdot/g,'*');
	la = la.replace(/\\left/g,'');
	la = la.replace(/\\right/g,'');
	
	var i = 0;
	var counter = 0;
	var recorder = true;
	var dict_letters = {'a' : 'R0', 'b' : 'R1', 'c' : 'R2', 'd' : 'R3', 'g' : 'R6', 'h' : 'R7', 'i' : 'R8', 'j' : 'R9', 'k' : 'R10', 
						'l' : 'R11', 'm' : 'R12', 'n' : 'R13', 'o' : 'R14', 'p' : 'R15', 'q' : 'R16', 'r' : 'R17', 's' : 'R18', 't' : 'R19',
						'u' : 'R20', 'v' : 'R21', 'w' : 'R22', 'A' : array_calc[0] , 'B' : array_calc[1],'C' : array_calc[2],'D' : array_calc[3],
						'E' : array_calc[4],'F' : array_calc[5],'G' : array_calc[6],'H' : array_calc[7],'I' : array_calc[8], 'J' : array_calc[9],
						'K' : array_calc[10],'L' : array_calc[11],'M' : array_calc[12],'N' : array_calc[13],'O' : array_calc[14], 'P' : array_calc[15],
						'Q' : array_calc[16],'R' : array_calc[17],'S' : array_calc[18],'T' : array_calc[19],'U' : array_calc[20], 'V' : array_calc[21]};
	var la2 = "";
	while(i < la.length){
		if(la[i] == '\\'){
			if(la[i + 1] == 't' && la[i + 2] == 'e' && la[i + 3] == 'x' && la[i + 4] == 't'){
				while(true){
					if(la[i] == ')' && counter == 0){
						break
					}
					if(la[i] == '('){
						counter++;
					}
					else if(la[i+1] == ')'){
						counter--;
					}
					la2 += la[i];
					i++;
				}
			}
			else{
				while(la[i] != '(' && la[i] != ' '){	
					la2 += la[i];
					i++;
				}
			}
		}
		if(la[i] in dict_letters){
			la2 += dict_letters[la[i]];
		}
		else if(la[i] == 'x' || la[i] == 'y' || la[i] == 'z'){
			if(la[i-1] in dict_letters){
				la2 += '*' + la[i];
			}
			else{
				la2 += la[i];
			}
		}
		else{
			la2 += la[i];
		}		
		i++;
	}
	la = la2;
	
	i = 0;
	counter = 0;
	recorder = false;
	while(i < la.length){ //logic for insering a / in fractals
		if(la.charAt(i) == 'c' && la.charAt(i-1) == 'a' && la.charAt(i-2) == 'r' && la.charAt(i-3) == 'f' && la.charAt(i-4) == '\\'){
			recorder = true;
		}
		if(recorder){
			if(la.charAt(i) == '('){
				counter++;
			}
			else if(la.charAt(i) == ')'){
				counter--;
			}
			if(la.charAt(i) == ')' && counter == 0){
				la = la.substring(0, i+1) + "/" + la.substring(i+1,la.length);
				recorder = false;
			}
		}
		i++;
	}
	la = la.replace(/\\/g,'');
	la = la.replace(/cdot/g,'*');	
	la = la.replace(/frac/g,'');
	return la;
}

/**
* Check if string is all upper-case
*/
function isUpperCase(str){
    return str === str.toUpperCase();
}

//$('#q_input_mathquill').append('<span>x^2</span>').mathquill('editable');
//$('#q_input_mathquill').mathquill('cmd', '\\sqrt');
//$('<span>\sqrt{2}</span>').mathquill().appendTo('#q_input_mathquill').mathquill('editable');
//$('<span/>').mathquill().appendTo('#q_input_mathquill').mathquill('latex','a_n x^n');
//$('#q_input_mathquill').append('<span>$</span>').mathquill('editable');

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}