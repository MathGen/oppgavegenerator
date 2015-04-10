// Common variables
var Q_INPUT					= '#q_input_mathquill';
var S_INPUT					= '#s_input_mathquill_1';
var A_INPUT					= '#a_input_mathquill_1';
var C_INPUT					= '#c_input_mathquill';
var W_INPUT					= '#w_input_mathquill_0';
var M_INPUT					= '#m_input_mathquill_1';
var F_INPUT					= '#f_fill_content_1';
var N_INPUT					= '#con_input_mathquill';
var STEP					= 1;
var ANSWER					= 1;
var SUB						= 1;
var TOPIC_SELECTED			= false;
var MULTI_CHOICE			= 0;
var FILL_IN					= false;
var CON_IN					= false;
var SUBMITTING				= false;
var c_count 				= 0;
var array_calc				= [];
var array_calc_unchanged	= [];
var MODIFY					= false;
var mod_blanks				= 0;
var mod_condition 			= 0;
var mod_multiple			= 0;

$(document).ready(function() {
	// Topic selection validation
	var category_selection = $('#category_selection');
	category_selection.change(function() {
		if(TOPIC_SELECTED == false){
			$('#category_selection').removeClass('select_error');
			TOPIC_SELECTED = true;
		}
	});

	// Check if template is inserted from db to be modified.
	if($('#edit_template').text() == 'true'){
		MODIFY = true;
		TOPIC_SELECTED = true;
		insert_editable_data();
	}

	// Set which input-field is active
	$(document).on('focus', '.input_mathquill', function(e){
		e.preventDefault();
		var input_id = $(this).attr('id');
		var input_group = input_id[0];
		if(input_group == 'q'){
			$(Q_INPUT).removeClass('select_error');
		}
		else if(input_group == 's'){
			S_INPUT = '#' + input_id;
			$(S_INPUT).removeClass('select_error');
		}
		else if(input_group == 'a'){
			A_INPUT = '#' + input_id;
			$(A_INPUT).removeClass('select_error');
		}
		else if(input_group == 'w'){
			W_INPUT = '#' + input_id;
		}
		else if(input_group == 'm'){
			M_INPUT = '#' + input_id;
		}
		else if(input_group == 'f'){
			F_INPUT = '#' + input_id;
		}
    });

	// Insert text
	var t_btn_ok = $('#t_btn_ok');
	$(t_btn_ok).click(function(e){
		e.preventDefault();
		var t_input = $('#t_input').val();
		$(Q_INPUT).mathquill('cmd', '\\text').mathquill('cmd', ' ' + t_input + ' ');
		$('#t_input').val("");
		var custom_tab_event = $.Event('keydown');
		custom_tab_event.bubbles = true;
		custom_tab_event.cancelable = true;
		custom_tab_event.keyCode = 9;
		$(Q_INPUT).trigger(custom_tab_event);
		$('#text_modal').on('hidden.bs.modal', function () {
			$(Q_INPUT).find('textarea').focus();
		});
	});
	
	// Cancel text-input
	var t_btn_cancel = $('.btn_close_text');
	$(t_btn_cancel).click(function(e){
		e.preventDefault();
		$('#t_input').val("");
		$('#text_modal').on('hidden.bs.modal', function () {
			$(Q_INPUT).find('textarea').focus();
		});
	});
	
	// Open text-input with focus
	var btn_text = $('#q_btn_text');
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
		$('#c_btn_var_dyn').append('<button id="c_btn_abc_'+q_var_id+'" class="btn btn-danger btn_var_abc">'+q_var+'</button>');
		$('#a_btn_var_dyn').append('<button id="a_btn_abc_'+q_var_id+'" class="btn btn-danger btn_var_abc">'+q_var+'</button>');
		$('#n_btn_var_dyn').append('<button id="n_btn_abc_'+q_var_id+'" class="btn btn-danger btn_var_abc">'+q_var+'</button>');
		$('#o_adv_domain').append('<tr id="o_adv_'+q_var_id+'" class="active o_adv_dyn"><td style="vertical-align: middle; text-align: right; color: #D9534F">'+q_var+':</td><td><input id="o_adv_from_'+q_var_id+'" type="number" class="form-control input-sm opt_domain_from" placeholder="Fra:"></td><td><input id="o_adv_to_'+q_var_id+'" type="number" class="form-control input-sm opt_domain_to" placeholder="Til:"></td><td></td></tr>');
		q_var = String.fromCharCode(q_var.charCodeAt(0) + 1);
		q_var_id++;
		$(Q_INPUT).find('textarea').focus();
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
		$(get_input_field(this)).find('textarea').focus();
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
		$(get_input_field(this)).find('textarea').focus();
	});
	
	// Insert equal sign
	var btn_equal = $('.btn_equal');
	$(btn_equal).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '=').find('textarea').focus();
	});
	
	// Insert parentheses operator
	var q_btn_par = $('.btn_par');
	$(q_btn_par).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('cmd', '(').find('textarea').focus();
	});

	// Insert left parentheses
	var btn_par_l = $('.btn_par_l');
	btn_par_l.click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '(').find('textarea').focus();
	});

	// Insert right parentheses
	var btn_par_r = $('.btn_par_r');
	btn_par_r.click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', ')').find('textarea').focus();
	});

	// Insert less-than operator
	var btn_less = $('.btn_less');
	btn_less.click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '<').find('textarea').focus();
	});

	// Insert 'and' operator
	$('.btn_and').click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '∧').find('textarea').focus();
	});

	// Insert 'and' alternative operator
	$('.btn_and_alt').click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '&').find('textarea').focus();
	});

	// Insert 'or' operator
	$('.btn_or').click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '∨').find('textarea').focus();
	});

	// Insert 'or' alternative operator
	$('.btn_or_alt').click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '|').find('textarea').focus();
	});

	// Insert greater-than operator
	var btn_greater = $('.btn_greater');
	btn_greater.click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '>').find('textarea').focus();
	});

	// Insert addition operator
	var q_btn_addition = $('.btn_addition');
	$(q_btn_addition).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '+').find('textarea').focus();
	});
	
	// Insert subtraction operator
	var q_btn_subtraction = $('.btn_subtraction');
	$(q_btn_subtraction).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '-').find('textarea').focus();
	});
	
	// Insert multiplication operator
	var q_btn_multiplication = $('.btn_multiplication');
	$(q_btn_multiplication).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '\\cdot').find('textarea').focus();
	});
	
	// Insert division operator
	var q_btn_division = $('.btn_division');
	$(q_btn_division).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('cmd', '\\frac').find('textarea').focus();
	});

	// Insert plus-minus
	var btn_pm = $('.btn_pm');
	btn_pm.click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '\\pm').find('textarea').focus();
	});

	// Insert exponent
	var q_btn_exponent = $('.btn_exponent');
	$(q_btn_exponent).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('cmd', '^').find('textarea').focus();
	});
	
	// Insert subscript
	var q_btn_subscript = $('.btn_subscript');
	$(q_btn_subscript).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('cmd', '_').find('textarea').focus();
	});
	
	// Insert square root
	var q_btn_sqrt = $('.btn_sqrt');
	$(q_btn_sqrt).click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('cmd', '\\sqrt').find('textarea').focus();
	});
	
	// Insert integral
	var q_btn_integral = $('.btn_int');
	$(q_btn_integral).click(function(e){
		e.preventDefault();
		//$(get_input_field(this)).mathquill('write', '\\int\\left(\\right)');
		$(get_input_field(this)).mathquill('cmd', '\\int').find('textarea').focus();
	});
	
	// Insert integral a^b
	var q_btn_integral_ab = $('.btn_int_ab');
	$(q_btn_integral_ab).click(function(e){
		e.preventDefault();
		//$(get_input_field(this)).mathquill('write', '\\int_{}^{}\\left(\\right)');
		$(get_input_field(this)).mathquill('write', '\\int_{}').mathquill('cmd', '^').find('textarea').focus();
		// A custom event to press the left arrow twice so the integral will focus on the subscript-limit.
		var custom_left_event = $.Event('keydown');
		custom_left_event.keyCode = 37;
		$(get_input_field(this)).trigger(custom_left_event).trigger(custom_left_event);

	});

	// Insert binomial
	var btn_binom = $('.btn_binom');
	btn_binom.click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('cmd', '\\binom').find('textarea').focus();
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
		$(get_input_field(this)).find('textarea').focus();
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
				var found = false;
				$(Q_INPUT).find('var').each(function(){
					if($(this).html() == check_char[n]){
						found = true;
					}
				});
				if(!found){
					$('#q_btn_abc_' + check_id[n]).remove();
					$('#s_btn_abc_' + check_id[n]).remove();
					$('#c_btn_abc_' + check_id[n]).remove();
					$('#o_adv_' + check_id[n]).remove();
				}
			}
		}
		$('#q_input_mathquill').find('textarea').focus();
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
			$('.o_adv_dyn').remove();
		}
		else if(btn_id == 'n'){
			refresh_conditions();
		}
		else{
			$(get_input_field(this)).mathquill('revert').mathquill('editable');
		}
		$(get_input_field(this)).find('textarea').focus();
	});
	
	// Keyboard-listener for input-fields
	$(document).on('keyup', '.input_mathquill', function(e){
		var id = $(this).attr('id');
		var id_group = id[0];
		if(e.keyCode == 88 || e.keyCode == 89 || e.keyCode == 90){
			if(id_group != 'c'){
				refresh_char_colors('#' + id);
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
								$('#c_btn_var_dyn').append('<button id="c_btn_abc_'+var_id+'" class="btn btn-danger btn_var_abc">'+tmp_var_typed+'</button>');
								$('#n_btn_var_dyn').append('<button id="n_btn_abc_'+var_id+'" class="btn btn-danger btn_var_abc">'+tmp_var_typed+'</button>');
								$('#o_adv_domain').append('<tr id="o_adv_'+var_id+'" class="active o_adv_dyn"><td style="vertical-align: middle; text-align: right; color: #D9534F">'+tmp_var_typed+':</td><td><input id="o_adv_from_'+var_id+'" type="number" class="form-control input-sm opt_domain_from" placeholder="Fra:"></td><td><input id="o_adv_to_'+var_id+'" type="number" class="form-control input-sm opt_domain_to" placeholder="Til:"></td><td></td></tr>');
							}
						}
					}
				});
			}
			else{
				refresh_char_colors('#' + id);
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
					var found = false;
					$('#' + id).find('var').each(function(){
						if($(this).html() == check_char[n]){
							found = true;
						}
					});
					if(!found){
						$('#q_btn_abc_' + check_id[n]).remove();
						$('#s_btn_abc_' + check_id[n]).remove();
						$('#c_btn_abc_' + check_id[n]).remove();
						$('#n_btn_abc_' + check_id[n]).remove();
						$('#o_adv_' + check_id[n]).remove();
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
				if($(Q_INPUT).mathquill('latex') != ''){
					$('.btn-group-q').prop('disabled', true);
					var s_panel = $('#s_panel');
					s_panel.fadeIn(function(){
						$('.mathquill-embedded-latex').mathquill('redraw');
					});
					scrollTo(s_panel);
					$(S_INPUT).find('textarea').focus();
				}
				else{
					$(Q_INPUT).addClass('select_error');
					error_message('q_input_field', 'Dette feltet kan ikke være tomt.');
				}
			}
			else{
				$('#category_selection').addClass('select_error');
				error_message('category_selection', 'Velg kategori.')
			}
		}
		else if(btn_id == 's'){
			var solution_valid = true;
			for(var step = 1; step <= STEP; step++){
				if($('#s_input_mathquill_' + step).mathquill('latex') == ''){
					solution_valid = false;
					$('#s_input_mathquill_' + step).addClass('select_error');
					error_message('step_' + step, 'Dette feltet kan ikke være tomt.');
				}
				if($('#s_text_' + step).val() == ""){
					solution_valid = false;
					error_message('s_text_' + step, 'Skriv forklaring.');
				}
			}
			if(solution_valid == true){
				$('.btn-group-s').prop('disabled', true);
				var a_panel = $('#a_panel');
				a_panel.fadeIn(function(){
					$('.mathquill-embedded-latex').mathquill('redraw');
				});
				scrollTo(a_panel);
				$(A_INPUT).find('textarea').focus()
			}
		}
		else if(btn_id == 'a'){
			var answer_valid = true;
			for(var ans = 1; ans <= ANSWER; ans++){
				if($('#a_input_mathquill_' + ans).mathquill('latex') == ''){
					answer_valid = false;
					$('#a_input_mathquill_' + ans).addClass('select_error');
					error_message('answer_' + ans, 'Dette feltet kan ikke være tomt.');
				}
			}
			if(answer_valid == true){
				$('.btn-group-a').prop('disabled', true);
				var o_panel = $('#o_panel');
				o_panel.fadeIn(function(){
					$('.mathquill-embedded-latex').mathquill('redraw');
				});
				scrollTo(o_panel);
			}
		}
	});
	
	// New solution step
	var s_btn_next = $('#s_btn_next');
	$(s_btn_next).click(function(e){
		e.preventDefault();
		$('#s_btn_del_' + STEP).hide();
		STEP++;
		$('#s_form').append('<div id="step_' + STEP + '" class="step" style="display: none"><hr>' +
			'<h4>Steg ' + STEP + '<a id="s_btn_del_'+STEP+'" class="glyphicon glyphicon-remove del_step" style="float:right"></a></h4>' +
			'<input id="s_text_' + STEP + '" type="text" class="form-control" placeholder="Forklaring...">' +
			'<div class="input_field s_input_field"><span id="s_input_mathquill_'+STEP+'" class="form-control input_mathquill"></span></div>');
		$('#s_input_mathquill_' + STEP).mathquill('editable');
		$('#step_' + STEP).fadeIn();
		S_INPUT = '#s_input_mathquill_' + STEP;
		scrollTo($('#step_' + STEP));
		$(S_INPUT).find('textarea').focus();
	});
	
	// Add another answer
	var a_btn_next = $('#a_btn_next');
	$(a_btn_next).click(function(e){
		e.preventDefault();
		$('#a_btn_del_' + ANSWER).hide();
		if(ANSWER == 1){
			$('#ans_title_1').show();
		}
		ANSWER++;
		$('#a_form').append('<div id="answer_'+ANSWER+'" class="answer" style="display: none"><hr>' +
			'<h4>Svar '+ANSWER+'<a id="a_btn_del_'+ANSWER+'" class="glyphicon glyphicon-remove del_answer" style="float:right"></a></h4>' +
			'<div class="input_field a_input_field"><span id="a_input_mathquill_'+ANSWER+'" class="form-control input_mathquill"></span></div>');
		$('#a_input_mathquill_' + ANSWER).mathquill('editable');
		$('#answer_' + ANSWER).fadeIn();
		A_INPUT = '#a_input_mathquill_' + ANSWER;
		scrollTo($('#answer_' + ANSWER));
		$(A_INPUT).find('textarea').focus();
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
	$(document).on('click', '.del_step', function(e){
		e.preventDefault();
		var btn_id = parseInt($(this).attr("id").match(/[\d]+$/));
		$('#step_' + btn_id).fadeOut(function(){
			$(this).remove();
		});
		STEP--;
		$('#s_btn_del_' + STEP).show();
		S_INPUT = '#s_input_mathquill_' + STEP;
		if(STEP == 1){
			scrollTo($('#s_panel'));
		}
		else{
			scrollTo($('#step_' + STEP));
		}
		$(S_INPUT).find('textarea').focus();
	});
	
	// Delete alternative answer
	$(document).on('click', '.del_answer', function(e){
		e.preventDefault();
		var btn_id = parseInt($(this).attr("id").match(/[\d]+$/));
		if(ANSWER == 2){
			$('#ans_title_1').hide();
		}
		$('#answer_' + btn_id).fadeOut(function(){
			$(this).remove();
		});
		ANSWER--;
		$('#a_btn_del_' + ANSWER).show();
		A_INPUT = '#a_input_mathquill_' + ANSWER;
		if(ANSWER == 1){
			scrollTo($('#a_panel'));
		}
		else{
			scrollTo($('#answer_' + ANSWER));
		}
		$(A_INPUT).find('textarea').focus();
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
			if(ANSWER > 1){
				for(var ans = 2; ans <= ANSWER; ans++){
					$('#answer_' + ans).remove();
				}
			}
			ANSWER = 1;
			A_INPUT = '#a_input_mathquill_' + ANSWER;
			$('#a_input_mathquill_1').mathquill('revert').mathquill('editable');
			$('#a_panel').fadeOut();
			$('.btn-group-s').prop('disabled', false);
			if(STEP > 1){
				for(var step = 2; step <= STEP; step++){
					$('#step_' + step).remove();
				}
			}
			STEP = 1;
			S_INPUT = '#s_input_mathquill_' + STEP;
			$('#s_input_mathquill_1').mathquill('revert').mathquill('editable');
			$('#s_panel').fadeOut();
			$('.btn-group-q').prop('disabled', false);
			scrollTo($('#q_panel'));
			$(Q_INPUT).find('textarea').focus();
		}
		else if(btn_id == 'c'){
			$(C_INPUT).mathquill('revert').mathquill('editable');
		}
		else if(btn_id == 'a'){
			$('#o_panel').fadeOut();
			$('.btn-group-a').prop('disabled', false);
			if(ANSWER > 1){
				for(var ans = 2; ans <= ANSWER; ans++){
					$('#answer_' + ans).remove();
				}
			}
			ANSWER = 1;
			A_INPUT = '#a_input_mathquill_' + ANSWER;
			$('#a_input_mathquill_1').mathquill('revert').mathquill('editable');
			$('#a_panel').fadeOut();
			$('#ans_title_1').hide();
			$('.btn-group-s').prop('disabled', false);
			if(STEP == 1){
				scrollTo($('#s_panel'));
			}
			else{
				scrollTo($('#step_' + STEP));
			}
			$(S_INPUT).find('textarea').focus();
		}
		else if(btn_id == 'o'){
			$('#o_panel').fadeOut();
			$('.btn-group-a').prop('disabled', false);
			if(ANSWER == 1){
				scrollTo($('#a_panel'));
			}
			else{
				scrollTo($('#answer_' + ANSWER));
			}
			$(A_INPUT).find('textarea').focus();
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

	// Show advanced domain settings
	var btn_adv_domain = $('#o_btn_adv_domain');
	btn_adv_domain.click(function(e){
		e.preventDefault();
		$('#o_adv_domain').fadeToggle();
		$('#o_adv_caret').toggleClass('dropup');
	});

	// Domain input-insertion to advanced settings
	var opt_domain_from = $('#opt_domain_from');
	var opt_domain_to = $('#opt_domain_to');
	opt_domain_from.on('input', function(){
		$('.opt_domain_from').val(opt_domain_from.val());
	});
	opt_domain_to.on('input', function(){
		$('.opt_domain_to').val(opt_domain_to.val());
	});

	// Open variable conditions modal
	var radio_conditions = $('#opt_conditions');
	radio_conditions.click(function(){
		if($(this).is(':checked')){
			$('#conditions_modal').modal('show').on('shown.bs.modal', function () {
				if(CON_IN == false){
					refresh_conditions();
					CON_IN = true;
				}
			});
		}
	});

	// Open multiple-choice modal
	var radio_multiple_choice = $('#opt_multiple_choice');
	radio_multiple_choice.change(function(){
		if ($(this).is(':checked')) {
			refresh_multiple_choice();
			$('#multiple_choice_modal').modal('show');
			$('#multiple_choice_modal').on('shown.bs.modal', function () {
				for(var m = 1; m <= MULTI_CHOICE; m++){
					$('#m_input_mathquill_' + m).mathquill('redraw');
					refresh_char_colors('#m_input_mathquill_' + m);
				}
			});
		}
	});

	// Add new multiple-choices
	var btn_new_multi = $('#m_btn_new');
	btn_new_multi.click(function(e){
		e.preventDefault();
		$('#m_btn_del_' + MULTI_CHOICE).hide();
		MULTI_CHOICE++;
		$('#m_dyn_multi_input').append('<div id="m_field_'+MULTI_CHOICE+'" class="input_field multi_field"><span id="m_input_mathquill_'+MULTI_CHOICE+'" class="mathquill-editable form-control input_mathquill"></span><a id="m_btn_del_'+MULTI_CHOICE+'" class="glyphicon glyphicon-remove pull-right del_multi"></a></div>');
		$('#m_input_mathquill_' + MULTI_CHOICE).mathquill('revert').mathquill('editable');
	});

	// Delete last multiple-choice
	$(document).on('click', '.del_multi', function(e){
		e.preventDefault();
		$('#m_field_' + MULTI_CHOICE).remove();
		MULTI_CHOICE--;
		$('#m_btn_del_' + MULTI_CHOICE).show();
	});

	// Open fill-in-the-blanks modal
	var radio_fill_blanks = $('#opt_fill_blanks');
	radio_fill_blanks.change(function(){
		if($(this).is(':checked')){
			$('#fill_blanks_modal').modal('show').on('shown.bs.modal', function () {
				if(FILL_IN == false){
					refresh_fill_in_content();
					FILL_IN = true;
				}
			});
		}
	});

	// Refresh fill-in-the-blanks content
	$('#f_btn_refresh').click(function(e){
		e.preventDefault();
		refresh_fill_in_content();
	});

	// Replace selected elements with blanks
	$('#f_btn_fill').click(function(e){
		e.preventDefault();
		$(get_input_field(this)).mathquill('write', '■'); // Black square HEX: &#x25A0
		get_diff_latex();
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
			var la = convert_variables(c_latex);
			la = la.replace(/\?/g,'');
			la = la.replace(/@/g,'');
			array_calc.push('@?(' + la + ')?@');
			array_calc_unchanged.push(c_latex);
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
			$('#n_btn_calc_dyn').append('<button id="n_btn_calc_'+c_count+'" class="btn btn-success btn_calc">'+c_var+'</button>');
			$('#n_btn_calc_' + c_count).popover({
				html: true,
				content: '<img src="http://latex.codecogs.com/svg.latex?'+c_latex+'" border="0"/>',
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
			c_count++;
		}
	});

	// Submit template to database event
	var o_btn_save = $('#o_btn_save');
	$(o_btn_save).click(function(e){
		e.preventDefault();
		submit_template();
	});
});

/**
 * Submit template to database
 */
function submit_template(){
	var form_submit = {};
	// TOPIC
	form_submit['topic'] = $('#category_selection').find(':selected').attr('id');

	// QUESTION_TEXT
	form_submit['question_text'] = convert_variables($(Q_INPUT).mathquill('latex'));
	form_submit['question_text_latex'] = $(Q_INPUT).mathquill('latex');

	// SOLUTION
	var tmp_solution = [];
	var tmp_solution_latex = [];
	for (var i = 1; i <= STEP; i++) {
		if ($('#s_text_' + i).val() != '') {
			tmp_solution.push('\\text{' + $('#s_text_' + i).val() + '}' + '\\n' + convert_variables($('#s_input_mathquill_' + i).mathquill('latex')));
			tmp_solution_latex.push($('#s_text_' + i).val() + '§' + $('#s_input_mathquill_' + i).mathquill('latex'));
		}
		else {
			tmp_solution.push(convert_variables($('#s_input_mathquill_' + i).mathquill('latex')));
			tmp_solution_latex.push('§' + $('#s_input_mathquill_' + i).mathquill('latex'));
		}
	}
	form_submit['solution'] = tmp_solution.join('\\n');
	form_submit['solution_latex'] = tmp_solution_latex.join('§');

	// ANSWER
	var tmp_answer = [];
	var tmp_answer_latex = [];
	for (var i = 1; i <= ANSWER; i++) {
		tmp_answer.push(convert_variables($('#a_input_mathquill_' + i).mathquill('latex')));
		tmp_answer_latex.push($('#a_input_mathquill_' + i).mathquill('latex'));
	}
	form_submit['answer'] = tmp_answer.join('§');
	form_submit['answer_latex'] = tmp_answer_latex.join('§');

	// RANDOM_DOMAIN
	// retrieves the list from latest letter in alphabet (w) to earliest (a) as that is the formatting used server side.
	var tmp_r_domain = [];
	for (var i = 22; i >= 0; i--) {
		if ($('#o_adv_' + i).length) {
			tmp_r_domain.push($('#o_adv_from_' + i).val() + " " + $('#o_adv_to_' + i).val());
		}
	}
	form_submit['random_domain'] = tmp_r_domain.join('§');

	// NUMBER_OF_DECIMALS
	form_submit['number_of_decimals'] = $('#opt_decimal').val();

	// ANSWER_CAN_BE_ZERO
	var tmp_allow_zero = "";
	if ($('#opt_allow').is(':checked')) {
		tmp_allow_zero = 'true';
	}
	else {
		tmp_allow_zero = 'false';
	}
	form_submit['answer_can_be_zero'] = tmp_allow_zero;

	// DICTIONARY
	var array_dict = [];
	var e_empty = true;
	for (var i = 1; i <= SUB; i++) {
		var e_from = $('#e_from_' + i).val();
		var e_to = $('#e_to_' + i).val();
		if (e_from != '' && e_to != '') {
			array_dict.push(e_from + '§' + e_to);
			e_empty = false;
		}
	}
	array_dict.sort(function (a, b) {
		var s_a = a.split('§');
		var s_b = b.split('§');
		return s_b[0].length - s_a[0].length; // ASC -> a - b; DESC -> b - a
	});
	if (e_empty) {
		form_submit['dictionary'] = "";
	}
	else {
		form_submit['dictionary'] = array_dict.join('§');
	}

	// CONDITIONS
	if ($('#opt_conditions').is(':checked')) {
		form_submit['conditions'] = convert_variables($('#con_input_mathquill').mathquill('latex'));
		form_submit['conditions_latex'] = $('#con_input_mathquill').mathquill('latex');
	}
	else {
		form_submit['conditions'] = "";
		form_submit['conditions_latex'] = "";
	}

	// CHOICES
	if ($('#opt_multiple_choice').is(':checked')) {
		form_submit['choices'] = get_multiple_choices(false);
		form_submit['choices_latex'] = get_multiple_choices(true);
	}
	else {
		form_submit['choices'] = "";
		form_submit['choices_latex'] = "";
	}

	// FILL_IN
	if ($('#opt_fill_blanks').is(':checked')) {
		form_submit['fill_in'] = convert_variables(get_diff_latex(false));
		var f_content = [];
		for(var f = 1; f <= STEP; f++){
			f_content.push($('#f_fill_content_' + f).mathquill('latex'));
		}
		form_submit['fill_in_latex'] = f_content.join('§');
	}
	else {
		form_submit['fill_in'] = "";
		form_submit['fill_in_latex'] = "";
	}

	// CALCULATION REFERENCE
	form_submit['calculation_ref'] = array_calc.join('§');
	form_submit['unchanged_ref'] = array_calc_unchanged.join('§');

	// CSRF_TOKEN
	form_submit["csrfmiddlewaretoken"] = getCookie('csrftoken');

	// TYPE
	form_submit['type'] = 'normal';

	// PRIMARY-KEY
	if(MODIFY){
		form_submit['pk'] = $('#template_id').text();
	}
	else{
		form_submit['pk'] = "";
	}

	// SUBMIT
	if (submit_validation()) {
		SUBMITTING = true;
		post(/submit/, form_submit);
	}

	//// Testing output
	//var test_output = [];
	//for(var s in form_submit){
	//	test_output.push(s + '\n' + form_submit[s]);
	//}
	//alert(test_output.join('\n'));
}

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
		return S_INPUT;
	}
	else if(btn_id == 'c'){
		return C_INPUT;
	}
	else if(btn_id == 'a'){
		return A_INPUT;
	}
	else if(btn_id == 'w'){
		return W_INPUT;
	}
	else if(btn_id == 'm'){
		return M_INPUT;
	}
	else if(btn_id == 'f'){
		return F_INPUT;
	}
	else if(btn_id == 'n'){
		return N_INPUT;
	}
}

/**
 * Converting variables (a,b,c,d.. etc) to computable ids (R0R,R1R,R2R,.. etc),
 * and calculated references (A,B,C, etc) with its content.
 */
function convert_variables(latex){
	var la = latex;
	la = la.replace(/\\cdots/g, '\\cdot ');
	la = la.replace(/\\cdot/g,'\\cdot ');
	la = la.replace(/\\left/g,'');
	la = la.replace(/\\right/g,'');
	la = la.replace(/\\&/g, '&');
	la = la.replace(/\\ln/g, '\\ln ');
	var counter = 0;
	var dict_letters = {'a' : 'R0R', 'b' : 'R1R', 'c' : 'R2R', 'd' : 'R3R', 'g' : 'R6R', 'h' : 'R7R', 'i' : 'R8R', 'j' : 'R9R', 'k' : 'R10R',
						'l' : 'R11R', 'm' : 'R12R', 'n' : 'R13R', 'o' : 'R14R', 'p' : 'R15R', 'q' : 'R16R', 'r' : 'R17R', 's' : 'R18R', 't' : 'R19R',
						'u' : 'R20R', 'v' : 'R21R', 'w' : 'R22R', 'A' : array_calc[0] , 'B' : array_calc[1],'C' : array_calc[2],'D' : array_calc[3],
						'E' : array_calc[4],'F' : array_calc[5],'G' : array_calc[6],'H' : array_calc[7],'I' : array_calc[8], 'J' : array_calc[9],
						'K' : array_calc[10],'L' : array_calc[11],'M' : array_calc[12],'N' : array_calc[13],'O' : array_calc[14], 'P' : array_calc[15],
						'Q' : array_calc[16],'R' : array_calc[17],'S' : array_calc[18],'T' : array_calc[19],'U' : array_calc[20], 'V' : array_calc[21]};
	var la2 = "";
	// Iteration for adding required {} to single exponents and subscripts.
	for(var j = 0; j < la.length; j++){
		if(la[j] == '^' || la[j] == '_'){
			if(la[j+1] != '{'){
				la = la.substring(0, j+1) + '{' + la[j+1] + '}' + la.substring(j+2, la.length);
			}
		}
	}
	// Iteration for converting variables to computable values, and fixing conflicts with latex-commands.
	for(var i = 0; i < la.length; i++){
		if(la[i] == '\\'){
			if(la[i + 1] == 't' && la[i + 2] == 'e' && la[i + 3] == 'x' && la[i + 4] == 't'){
				while(true){
					if(la[i] == '}' && counter == 0){
						break
					}
					if(la[i] == '{'){
						counter++;
					}
					else if(la[i+1] == '}'){
						counter--;
					}
					la2 += la[i];
					i++;
				}
			}
			else if(la[i+1] == 'n'){
				la2 += '\\n';
				i++;
			}
			else{
				while(la[i] != '{' && la[i] != ' ' && la[i] != '_' && la[i] != '^'){
					la2 += la[i];
					i++;
					if(la[i] == '\\'){
						break
					}
				}
			}
		}
		if(la[i] in dict_letters){
			if((la[i-1] in dict_letters || la[i-1] == ')' || !isNaN(la[i-1])) && la[i-2] != '\^' && la[i-2] != '\\'){
				if(la[i-1] != ' ' && la[i-2] != 't' && la[i-3] != 'o' && la[i-4] != 'd' && la[i-5] != 'c'){
					la2 += '\\cdot ' + dict_letters[la[i]];
				}
				else{
					la2 += dict_letters[la[i]];
				}
			}
			else{
				if(la[i-1] == '\@' && la[i-2] == 'x' && la[i-3] == 'x' && la[i-4] == 'x' && la[i-5] == 'x' && la[i-6] == '\@'){
					if((la[i-7] in dict_letters || la[i-7] == ')' || !isNaN(la[i-7])) && la[i-8] != '\^' && la[i-8] != '\\'){
						la2 += '\\cdot ' + dict_letters[la[i]];
					}
					else{
						la2 += dict_letters[la[i]];
					}
				}
				else{
					if(la[i-1] != '\\'){
						la2 += dict_letters[la[i]];
					}
				}
			}
			if(la[i+1] == '('){
				la2 += '\\cdot ';
			}
		}
		else if(la[i] == 'x' || la[i] == 'y' || la[i] == 'z'){
			if((la[i-1] in dict_letters || la[i-1] == ')' || !isNaN(la[i-1])) && la[i-2] != '\^' && la[i-2] != '\\'){
				if(la[i-1] != ' ' && la[i-2] != 't' && la[i-3] != 'o' && la[i-4] != 'd' && la[i-5] != 'c') {
					la2 += '\\cdot ' + la[i];
				}
				else{
					la2 += la[i];
				}
			}
			else{
				if(la[i-1] == '\@' && la[i-2] == 'x' && la[i-3] == 'x' && la[i-4] == 'x' && la[i-5] == 'x' && la[i-6] == '\@'){
					if((la[i-7] in dict_letters || la[i-7] == ')' || !isNaN(la[i-7])) && la[i-8] != '\^' && la[i-8] != '\\'){
						la2 += '\\cdot ' + la[i];
					}
					else{
						la2 += la[i];
					}
				}
				else{
					if(la[i-1] != '\\'){
						la2 += la[i];
					}
				}
			}
			if(la[i+1] == '('){
				la2 += '\\cdot ';
			}
		}
		else{
			la2 += la[i];
		}
	}
	la = la2;
	return la;
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
	la = la.replace(/∧/g, '&');
	la = la.replace(/∨/g, '|');
	
	var i = 0;
	var counter = 0;
	var recorder = true;
	var dict_letters = {'a' : 'R0R', 'b' : 'R1R', 'c' : 'R2R', 'd' : 'R3R', 'g' : 'R6R', 'h' : 'R7R', 'i' : 'R8R', 'j' : 'R9R', 'k' : 'R10R',
						'l' : 'R11R', 'm' : 'R12R', 'n' : 'R13R', 'o' : 'R14R', 'p' : 'R15R', 'q' : 'R16R', 'r' : 'R17R', 's' : 'R18R', 't' : 'R19R',
						'u' : 'R20R', 'v' : 'R21R', 'w' : 'R22R', 'A' : array_calc[0] , 'B' : array_calc[1],'C' : array_calc[2],'D' : array_calc[3],
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
				while(la[i] != '(' && la[i] != ' ' && la[i] != '_' && la[i] != '^'){
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

/**
 * Scroll to specific element given by id.
 * @param id - id of element to scroll to.
 */
function scrollTo(id){
	$('html,body').animate({scrollTop: id.offset().top - 65}); // -65 because of the navbar.
}

/**
 * Add a error message under the given element.
 * @param element_id - id of element to apply error message to.
 * @param message - the error message.
 */
function error_message(element_id, message){
	var element = $('#' + element_id);
	$(document).ready(function(){
		element.after('<p class="error_content">* '+message+'</p>');
		$('.error_content').show(100).delay(5000).hide(100).queue(function(){
			$(this).remove();
		});
	});
}

/**
 * Validates required fields before submitting.
 * @returns {boolean} returns true if the validation pass.
 */
function submit_validation(){
	var valid = true;
	if($(Q_INPUT).mathquill('latex') == ''){
		valid = false;
		$(Q_INPUT).addClass('select_error');
		error_message('q_input_field', 'Dette feltet kan ikke være tomt.');
	}
	for(var step = 1; step <= STEP; step++){
		if($('#s_input_mathquill_' + step).mathquill('latex') == ''){
			valid = false;
			$('#s_input_mathquill_' + step).addClass('select_error');
			error_message('step_' + step, 'Dette feltet kan ikke være tomt.');
		}
		if($('#s_text_' + step).val() == ""){
			valid = false;
			error_message('s_text_' + step, 'Skriv forklaring.');
		}
	}
	for(var ans = 1; ans <= ANSWER; ans++){
		if($('#a_input_mathquill_' + ans).mathquill('latex') == ''){
			valid = false;
			$('#a_input_mathquill_' + ans).addClass('select_error');
			error_message('answer_' + ans, 'Dette feltet kan ikke være tomt.');
		}
	}
	for(var adv = 22; adv >= 0; adv--){
		if($('#o_adv_from_' + adv).length){
			if($('#o_adv_from_' + adv).val() == ''){
				valid = false;
				error_message('o_adv_from_' + adv, 'Fyll ut!');
				$('#o_adv_domain').fadeIn();
				$('#o_adv_caret').addClass('dropup');
			}
			else if($('#o_adv_to_' + adv).val() == ''){
				valid = false;
				error_message('o_adv_to_' + adv, 'Fyll ut!');
				$('#o_adv_domain').fadeIn();
				$('#o_adv_caret').addClass('dropup');
			}
		}
	}
	if($('#opt_decimal').val() == ''){
		valid = false;
		error_message('opt_decimal', 'Fyll ut!');
	}
	return valid;
}

/**
 * Retrieve multiple choices
 * @returns {string} returns all multiple choices as a string.
 */
function get_multiple_choices(latex_bool){
	var multiple_choices = [];
	if(!latex_bool){
		for(var m = 1; m <= MULTI_CHOICE; m++){
			multiple_choices.push(convert_variables($('#m_input_mathquill_' + m).mathquill('latex')));
		}
	}
	else{
		for(var ml = 1; ml <= MULTI_CHOICE; ml++){
			multiple_choices.push($('#m_input_mathquill_' + ml).mathquill('latex'))
		}
	}
	return multiple_choices.join('§');
}

/**
 * Reset the conditions input-field.
 */
function refresh_conditions(){
	var con_input = $('#con_dyn_input');
	$('#con_input_field').remove();
	con_input.append('<div id="con_input_field" class="input_field"><span id="con_input_mathquill" class="form-control input_mathquill"></span></div>');
	$('#con_input_mathquill').mathquill('editable');
	if(MODIFY == true && mod_condition < 2){
		mod_condition++;
		var condition = $('#conditions').text();
		$('#con_input_mathquill').mathquill('write', condition);
		refresh_char_colors('#con_input_mathquill');
	}
}

/**
 * Refreshing the contents of fill-in-the-blanks from the solutions.
 */
function refresh_fill_in_content(){
	var f_dyn_fill = $('#f_dyn_fill_input');
	$('.f_fill_content').remove();
	if(MODIFY && mod_blanks < 2){
		mod_blanks++;
		var f_latex = $('#fill_in').text();
		f_latex = f_latex.split('§');
		for(var f = 1; f <= f_latex.length; f++){
			if(f > 1){
				f_dyn_fill.append('<hr class="f_fill_content">');
			}
			f_dyn_fill.append('<div id="f_fill_content_' + f + '" class="form-control f_fill_content input_mathquill" style="border: 0; box-shadow: none">' + f_latex[f-1] + '</div>');
			$('#f_fill_content_' + f).mathquill('editable');
		}
	}
	else{
		for (var f = 1; f <= STEP; f++) {
			if (f > 1) {
				f_dyn_fill.append('<hr class="f_fill_content">');
			}
			var f_latex = $('#s_input_mathquill_' + f).mathquill('latex');
			f_dyn_fill.append('<div id="f_fill_content_' + f + '" class="form-control f_fill_content input_mathquill" style="border: 0; box-shadow: none">' + f_latex + '</div>');
			$('#f_fill_content_' + f).mathquill('editable');
		}
	}
	$('.f_fill_content').unbind('keypress');
	$('.f_fill_content').unbind('keydown');
	refresh_char_colors('.f_fill_content');
	$('#f_diff_latex').html("");
}

/**
 * Refreshing multiple-choice contents. If in modify get previous content.
 */
function refresh_multiple_choice(){
	if(MULTI_CHOICE == 0 && MODIFY == false) {
		MULTI_CHOICE++;
		$('#m_dyn_multi_input').append('<div class="input_field"><span id="m_input_mathquill_1" class="mathquill-editable form-control input_mathquill"></span></div>');
		$('#m_input_mathquill_1').mathquill('revert').mathquill('editable');
	}
	else if(MULTI_CHOICE == 0 && MODIFY == true && mod_multiple < 2){
		mod_multiple++;
		var m_choice = $('#choices').text();
		m_choice = m_choice.split('§');
		$('#m_dyn_multi_input').append('<div class="input_field"><span id="m_input_mathquill_1" class="mathquill-editable form-control input_mathquill"></span></div>');
		$('#m_input_mathquill_1').mathquill('revert').mathquill('editable');
		MULTI_CHOICE = m_choice.length;
		if(MULTI_CHOICE > 1){
			for(var m = 2; m <= MULTI_CHOICE; m++){
				$('#m_btn_del_' + (m-1)).hide();
				$('#m_dyn_multi_input').append('<div id="m_field_'+m+'" class="input_field multi_field"><span id="m_input_mathquill_'+m+'" class="mathquill-editable form-control input_mathquill"></span><a id="m_btn_del_'+m+'" class="glyphicon glyphicon-remove pull-right del_multi"></a></div>');
				$('#m_input_mathquill_' + m).mathquill('revert').mathquill('editable');
			}
		}
		for(var m = 1; m <= MULTI_CHOICE; m++){
			$('#m_input_mathquill_' + m).mathquill('write', m_choice[(m-1)]);
		}
	}
}

/**
 * Adding colors to used variables, unknown characters and calculated references.
 * @param selector - Which input field to refresh.
 */
function refresh_char_colors(selector){
	var input_id = $(selector).attr('id');
	input_id = input_id[0];
	$(selector).find('var').each(function(){
		var f_var = $(this);
		if(f_var.hasClass('content_x') || $(this).hasClass('content_var') || $(this).hasClass('florin') || $(this).html() == 'e'){}
		else{
			if(f_var.html() == 'x' || f_var.html() == 'y' || f_var.html() == 'z'){
				f_var.addClass('content_x');
			}
			else if(f_var.html().match(/^[a-z]*$/)){
				$('.btn_var_abc').each(function(){
					if($(this).html() == f_var.html()){
						f_var.addClass('content_var');
					}
				});
				if(input_id == 'q'){
					var var_id = f_var.html().charCodeAt(0) - 97; // Getting the button id (a:0, b:1, c:2)
					if($('#q_btn_abc_' + var_id).length){}
					else {
						$('#q_btn_var_dyn').append('<button id="q_btn_abc_' + var_id + '" class="btn btn-danger btn_var_abc">' + f_var.html() + '</button>');
						$('#s_btn_var_dyn').append('<button id="s_btn_abc_' + var_id + '" class="btn btn-danger btn_var_abc">' + f_var.html() + '</button>');
						$('#c_btn_var_dyn').append('<button id="c_btn_abc_' + var_id + '" class="btn btn-danger btn_var_abc">' + f_var.html() + '</button>');
						$('#n_btn_var_dyn').append('<button id="n_btn_abc_' + var_id + '" class="btn btn-danger btn_var_abc">' + f_var.html() + '</button>');
						$('#o_adv_domain').append('<tr id="o_adv_' + var_id + '" class="active o_adv_dyn"><td style="vertical-align: middle; text-align: right; color: #D9534F">' + f_var.html() + ':</td><td><input id="o_adv_from_' + var_id + '" type="number" class="form-control input-sm opt_domain_from" placeholder="Fra:"></td><td><input id="o_adv_to_' + var_id + '" type="number" class="form-control input-sm opt_domain_to" placeholder="Til:"></td><td></td></tr>');
					}
				}
			}
			else if(f_var.html().match(/^[A-Z]*$/)){
				$('.btn_calc').each(function(){
					if($(this).html() == f_var.html()){
						f_var.addClass('content_calc');
					}
				});
			}
		}
	});
}

/**
 * Compare two latex strings, converting it to asciimath, and wrap parts of string that differs with a tag.
 * @returns {*|jQuery} - The asciimath string with blank tags.
 */
function get_diff_latex(latex_bool){
	var dmp = new diff_match_patch();
	dmp.Diff_Timeout = 1;
	dmp.Diff_EditCost = 4;
	var latex_before = [];
	var latex_after = [];
	if(!latex_bool) {
		for (var la_orig = 1; la_orig <= STEP; la_orig++) {
			//latex_before.push(latex_to_asciimath($('#s_input_mathquill_' + la_orig).mathquill('latex')));
			//latex_after.push(latex_to_asciimath($('#f_fill_content_' + la_orig).mathquill('latex')));
			latex_before.push('\\text{' + $('#s_text_' + la_orig).val() + '}' + '\\n' + $('#s_input_mathquill_' + la_orig).mathquill('latex'));
			latex_after.push('\\text{' + $('#s_text_' + la_orig).val() + '}' + '\\n' + $('#f_fill_content_' + la_orig).mathquill('latex'));
		}
		var d = dmp.diff_main(latex_before.join('\\n'), latex_after.join('\\n')); // Two strings to compare.
	}
	else{
		for (var la_edit = 1; la_edit <= STEP; la_edit++) {
			latex_before.push($('#s_input_mathquill_' + la_edit).mathquill('latex'));
			latex_after.push($('#f_fill_content_' + la_edit).mathquill('latex'));
		}
		var d = dmp.diff_main(latex_before.join('§'), latex_after.join('§')); // Two strings to compare.
	}
	//dmp.diff_cleanupSemantic(d);
	var ds = dmp.diff_prettyHtml(d);
	$('#f_diff_latex').html("").append(ds);
	return $('#f_diff_latex').text();
}

/**
 * Before unload, ask user to confirm redirecting.
 */
$(window).bind('beforeunload', function(e){
	if(TOPIC_SELECTED && !SUBMITTING){
		return 'Warning!';
	}
});

/**
 * Focus on calculation:input-field, when modal is shown.
 */
$('#calc_modal').on('shown.bs.modal', function () {
	$(C_INPUT).find('textarea').focus();
});

/**
 * Retrieving data from selected task to be modified. Inserting data to all required fields, and prepares for editing.
 */
function insert_editable_data(){
	// Inserting calculated references.
	var calc_str = $('#calculation_references').text();
	var calc_str = calc_str.split('§');
	for(var a = 0; a < calc_str.length; a++){
		array_calc.push(calc_str[a]);
	}
	var calc_pop = $('#unchanged_ref').text();
	var calc_pop = calc_pop.split('§');
	for(var b = 0; b < calc_pop.length; b++){
		array_calc_unchanged.push(calc_pop[b]);
	}
	c_count = array_calc_unchanged.length;
	if(c_count > 0){
		$('#s_btn_calc_dyn').append('<button id="s_btn_calc_delete" class="btn btn-success btn-xs btn_calc_del"><span class="glyphicon glyphicon-remove"></span></button>');
		$('#a_btn_calc_dyn').append('<button id="a_btn_calc_delete" class="btn btn-success btn-xs btn_calc_del"><span class="glyphicon glyphicon-remove"></span></button>');
		// Logic for adding the calculated-reference buttons with popovers.
		for(var c_index = 0; c_index < c_count; c_index++){
			var c_var = "A";
			c_var = String.fromCharCode(c_var.charCodeAt(0) + c_index);
			$('<button id="s_btn_calc_'+c_index+'" class="btn btn-success btn_calc">'+c_var+'</button>').insertBefore('#s_btn_calc_delete');
			$('#s_btn_calc_' + c_index).popover({
				html: true,
				content: '<img src="http://latex.codecogs.com/svg.latex?'+calc_pop[c_index]+'" border="0"/>',
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
			$('<button id="a_btn_calc_'+c_index+'" class="btn btn-success btn_calc">'+c_var+'</button>').insertBefore('#a_btn_calc_delete');
			$('#a_btn_calc_' + c_index).popover({
				html: true,
				content: '<img src="http://latex.codecogs.com/svg.latex?'+calc_pop[c_index]+'" border="0"/>',
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
			$('#c_btn_calc_dyn').append('<button id="c_btn_calc_'+c_index+'" class="btn btn-success btn_calc">'+c_var+'</button>');
			$('#c_btn_calc_' + c_index).popover({
				html: true,
				content: '<img src="http://latex.codecogs.com/svg.latex?'+calc_pop[c_index]+'" border="0"/>',
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
			$('#n_btn_calc_dyn').append('<button id="n_btn_calc_'+c_index+'" class="btn btn-success btn_calc">'+c_var+'</button>');
			$('#n_btn_calc_' + c_index).popover({
				html: true,
				content: '<img src="http://latex.codecogs.com/svg.latex?'+calc_pop[c_index]+'" border="0"/>',
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
		}
	}

	// Refreshing colors and adding required variable-buttons to the question.
	refresh_char_colors('#q_input_mathquill');

	// Insert solution
	var edit_solution = $('#solution').text();
	edit_solution = edit_solution.split('§');
	var edit_step = edit_solution.length / 2;
	$('#s_input_mathquill_1').mathquill('write', edit_solution[1]);
	if(edit_step > 1){
		var i_la = 3;
		for(var index_s = 2; index_s <= edit_step; index_s++){
			$('#s_btn_del_' + STEP).hide();
			STEP = index_s;
			$('#s_form').append('<div id="step_' + STEP + '" class="step" style="display: none"><hr>' +
				'<h4>Steg ' + STEP + '<a id="s_btn_del_'+STEP+'" class="glyphicon glyphicon-remove del_step" style="float:right"></a></h4>' +
				'<input id="s_text_' + STEP + '" type="text" class="form-control" placeholder="Forklaring...">' +
				'<div class="input_field s_input_field"><span id="s_input_mathquill_'+STEP+'" class="form-control input_mathquill">'+ edit_solution[i_la] +'</span></div>');
			$('#s_input_mathquill_' + STEP).mathquill('editable');
			$('#step_' + STEP).show();
			i_la += 2;
		}
	}
	var i_s = 0;
	for(var index_s_text = 1; index_s_text <= edit_solution.length; index_s_text++){
		$('#s_text_' + index_s_text).val(edit_solution[i_s]);
		i_s += 2;
	}

	// Insert answer
	var edit_answer = $('#answer').text();
	edit_answer = edit_answer.split('§');
	$('#a_input_mathquill_1').mathquill('write', edit_answer[0]);
	if(edit_answer.length > 1){
		for(var index_a = 2; index_a <= edit_answer.length; index_a++){
			$('#a_btn_del_' + ANSWER).hide();
			ANSWER = index_a;
			$('#ans_title_1').show();
			$('#a_form').append('<div id="answer_'+ANSWER+'" class="answer" style="display: none"><hr>' +
				'<h4>Svar '+ANSWER+'<a id="a_btn_del_'+ANSWER+'" class="glyphicon glyphicon-remove del_answer" style="float:right"></a></h4>' +
				'<div class="input_field a_input_field"><span id="a_input_mathquill_'+ANSWER+'" class="form-control input_mathquill">'+ edit_answer[index_a] +'</span></div>');
			$('#a_input_mathquill_' + ANSWER).mathquill('editable');
			$('#answer_' + ANSWER).show();
		}
	}

	refresh_char_colors('.input_mathquill');

	// Insert random-domain
	var edit_random_domain = $('#random_domain').text();
	edit_random_domain = edit_random_domain.split('§');
	var rd_exist = [];
	for(var r = 22; r >= 0; r--){
		if($('#o_adv_from_' + r).val() != ''){
			rd_exist.push(r);
		}
	}
	for(var rd = 0; rd < edit_random_domain.length; rd++){
		var edit_r = edit_random_domain[rd].split(" ");
		if(rd == 0){
			$('#opt_domain_from').val(edit_r[0]);
			$('#opt_domain_to').val(edit_r[1]);
		}
		$('#o_adv_from_' + rd_exist[rd]).val(edit_r[0]);
		$('#o_adv_to_' + rd_exist[rd]).val(edit_r[1]);
	}

	// Insert number of decimals
	$('#opt_decimal').val(0);

	// Set checked on required alt.tasks.
	if($('#conditions').text() != ""){
		$('#opt_conditions').prop('checked', true);
		refresh_conditions();
	}
	if($('#choices').text() != ""){
		$('#opt_multiple_choice').prop('checked', true);
		refresh_multiple_choice();
	}
	if($('#fill_in').text() != ""){
		$('#opt_fill_blanks').prop('checked', true);
		refresh_fill_in_content();
	}
}

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