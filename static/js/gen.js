// Common variables
var Q_INPUT					= '#q_input_mathquill';		// Question input-field
var S_INPUT					= '#s_input_mathquill_1';	// Default solution input-field
var A_INPUT					= '#a_input_mathquill_1';	// Default answer input-field
var C_INPUT					= '#c_input_mathquill';		// Calculation input-field
var W_INPUT					= '#w_input_mathquill_0';	// Default user-answer input-field
var M_INPUT					= '#m_input_mathquill_1';	// Default multiple-choice input-field
var F_INPUT					= '#f_fill_content_1';		//
var N_INPUT					= '#n_input_mathquill';		// Condition input-field
var T_INPUT					= '#t_input';				// Text-input in text-modal
var ACTIVE_INPUT			= '#q_input_mathquill';     // Current active input-field
var STEP					= 1;						// Number of steps in solution.
var ANSWER					= 1;						// Number of answers.
var SUB						= 1;						// Number of text-substitutions.
var TITLE_INSERTED			= false;
var MULTI_CHOICE			= 0;
var FILL_IN					= false;
var CON_IN					= false;
var SUBMITTING				= false;
var VARIABLES				= {};						// Object containing variables in use.
var MAX_VARIABLES			= 18;						// Max amount of unique variables.
var VAR_INIT				= false;
var dict_calc				= {};
var dict_calc_unchanged		= {};
var MODIFY					= false;
var SUBMIT_AS_NEW			= false;
var mod_blanks				= 0;
var mod_condition 			= 0;
var mod_multiple			= 0;
var VARIABLE_COUNT			= 0;
var edit_calc               = false;
var edit_calc_id            = 999;

$(document).ready(function() {
	// Draw math
	redraw_mathquill_elements();

	// KeyPad listeners
	$(document).on('click', '.btn_keypad', function(e){
		e.preventDefault();
		var keypad_cmd = "";
		ACTIVE_INPUT = get_input_field(this);
		if($(this).hasClass('keypad_int')){
			keypad_cmd = $(this).val();
			write_to_mathfield(ACTIVE_INPUT, keypad_cmd);
			simulate_keystroke(ACTIVE_INPUT, 'Left', 2);
		}
		else if($(this).hasClass('keypad_write')){
			keypad_cmd = $(this).val();
			write_to_mathfield(ACTIVE_INPUT, keypad_cmd);
		}
		else{
			if($(this).attr('value')){
				keypad_cmd = $(this).val();
			}
			else if($(this).hasClass('btn_var_abc') || $(this).hasClass('btn_calc')){
				keypad_cmd = $(this).text().replace(/x/g, "");
			}
			else{
				keypad_cmd = MathQuill.StaticMath($(this)[0]).latex();
			}
			cmd_to_mathfield(ACTIVE_INPUT, keypad_cmd);
		}
		refresh_char_colors(ACTIVE_INPUT);
	});

	// Custom Matrix popover
	$(document).on('click', '.btn_custom_matrix[rel=matrix-popover]', function(e){
		e.preventDefault();
		ACTIVE_INPUT = get_input_field(this);
	}).popover({
		html: true,
		selector: '[rel="matrix-popover"]',
		content: function(){
			return $('#popover_content_matrix')[0].outerHTML;
		},
		title: function(){
			return $('#popover_title_matrix').text();
		},
		container: 'body'
	});

	// Draw preview of custom matrix
	$(document).on('mouseenter', '#popover_content_matrix td', function(){
		preview_custom_matrix($(this));
		$('.popover-title').text($('#popover_title_matrix').text() + get_custom_matrix_size($(this)));
	});

	// Draw custom matrix
	$(document).on('click', '#popover_content_matrix td', function(){
		var matrix_size = get_custom_matrix_size($(this)).split('x');
		var latex = get_custom_matrix_latex(matrix_size[0], matrix_size[1]);
		write_to_mathfield(ACTIVE_INPUT, latex);
		simulate_keystroke(ACTIVE_INPUT, 'Left', parseInt(matrix_size[0]*matrix_size[1]));
		$(this).closest('.popover').popover('hide');
	});

	// Template title validation
	$('#template_title').change(function() {
		if(TITLE_INSERTED == false){
			$('#template_title').removeClass('select_error');
			TITLE_INSERTED = true;
		}
	});

	// Check if template is inserted from db to be modified.
	if($('#edit_template').text() == 'true'){
		MODIFY = true;
		TITLE_INSERTED = true;
		VAR_INIT = true;
		insert_editable_data();
	}

	// Set which input-field is active
	$(document).on('focus', '.input_mathquill', function(e){
		e.preventDefault();
		var input_id = $(this).attr('id');
		if(input_id != undefined) {
			var input_group = input_id[0];

			if (input_group == 'q') {
				ACTIVE_INPUT = '#' + input_id;
				$(Q_INPUT).removeClass('select_error');
			}
			else if (input_group == 's') {
				S_INPUT = '#' + input_id;
				ACTIVE_INPUT = '#' + input_id;
				$(S_INPUT).removeClass('select_error');
			}
			else if (input_group == 'a') {
				A_INPUT = '#' + input_id;
				ACTIVE_INPUT = '#' + input_id;
				$(A_INPUT).removeClass('select_error');
			}
			else if (input_group == 'm') {
				M_INPUT = '#' + input_id;
				ACTIVE_INPUT = '#' + input_id;
			}
			else if (input_group == 'f') {
				F_INPUT = '#' + input_id;
				ACTIVE_INPUT = '#' + input_id;
			}
		}
    });

 	// Set which input-field is active on user-side.
	$(document).on('focus', '.input_blanks', function(e){
		e.preventDefault();
		var input_id = $(this).attr('id');
		if(input_id != undefined) {
			var input_group = input_id[0];
			if (input_group == 'w') {
				W_INPUT = '#' + input_id;
				ACTIVE_INPUT = W_INPUT;
			}
		}
    });

	// TEXT-PANEL: Insert text
	$('#t_btn_ok').click(function(e){
		e.preventDefault();
		var t_input = $(T_INPUT).val();
		$(T_INPUT).val("");
		write_to_mathfield(ACTIVE_INPUT, '\\text{'+ t_input +' }');
		$('#text_modal').on('hidden.bs.modal', function () {
			$(ACTIVE_INPUT).find('textarea').focus();
		});
	});
	
	// TEXT-PANEL: Cancel text-input
	$('.btn_close_text').click(function(e){
		e.preventDefault();
		$(T_INPUT).val("");
		$('#text_modal').on('hidden.bs.modal', function () {
			$(ACTIVE_INPUT).find('textarea').focus();
		});
	});
	
	// TEXT-PANEL: Open text panel
	$('.btn_text').click(function(){
		ACTIVE_INPUT = get_input_field(this);
		$('#text_modal').on('shown.bs.modal', function () {
			$(T_INPUT).focus();
		});
	});

	// VARIABLES: Insert new variable
	$('.btn_var').click(function(e){
		e.preventDefault();
		if(Object.keys(VARIABLES).length <= MAX_VARIABLES) {
			var var_available = false;
			var q_var = "a";
			var q_var_id = 0;
			while (var_available == false) {
				if ($('#q_btn_abc_' + q_var_id).length || q_var == "r" || q_var == "x" || q_var == "y" || q_var == "z") {
					q_var = String.fromCharCode(q_var.charCodeAt(0) + 1);
					q_var_id++;
				}
				else {
					var_available = true;
				}
			}
			init_new_variable(q_var);
			redraw_mathquill_elements();
			$(Q_INPUT).find('textarea').focus();
		}
		else{
			alert('Ikke tillat med flere variabler.');
		}
	});

    // VARIABLES: Insert custom variable.
	$(document).on('focusout', '.input_new_variable', function() {
		var variable = $(this).val();
        if (variable) {
            if (variable.match(/^[a-z]+$/g)) {
                var id = get_converted_variable(variable).replace(/R/g, "");
                if($('#q_btn_abc_' + id).length){
                    error_message('.input_new_variable', "Tegn allerede i bruk!");
                } else if(variable == "r" || variable == "x" || variable == "y" || variable == "z"){ // Ugyldige tegn!
                    error_message('.input_new_variable', "Ugyldig tegn!");
                } else {
                    init_new_variable(variable);
                }
                $(this).val("");
            } else {
                error_message('.input_new_variable', "Ugyldig tegn!");
                $(this).val("");
            }
        }
	}).on('keyup', '.input_new_variable', function(e){
		if(/(13)/.test(e.which)) { // Add tag if one of these keys are pressed.
            $(this).focusout();
		}
	});

	// VARIABLES: Remove variable a,b,c,..
	$(document).on('click', '.btn_var_del', function(e){
		var id = parseInt($(this).attr('id').match(/[\d]+$/));
		$('#q_btn_abc_' + id).remove();
		$('.btn_var_' + id).remove();
		$('#o_adv_' + id).remove();
		refresh_all_char_colors();
		refresh_variables();
		e.stopPropagation();
	});

	// Erase last input
	$('.btn_delete').click(function(e){
		e.preventDefault();
		simulate_keystroke(get_input_field(this),'Backspace');
		$(ACTIVE_INPUT).find('textarea').focus();
	});
	
	// Clear input
	$(document).on('click', '.btn_clear', function(e){
		e.preventDefault();
		var btn_id = $(this).attr('id');
		btn_id = btn_id[0];
		if(btn_id == 'q'){
			MathQuill.MathField($(Q_INPUT)[0]).revert();
			MathQuill.MathField($(Q_INPUT)[0]).focus();
		}
		else if(btn_id == 'n'){
			refresh_conditions();
		}
		else if(btn_id == 's'){
			var sol_input = $(this).attr('id').replace(/s_btn_clear_/g, '');
			MathQuill.MathField($('#s_input_mathquill_' + sol_input)[0]).revert();
			MathQuill.MathField($('#s_input_mathquill_' + sol_input)[0]).focus();
		}
		else if(btn_id == 'a'){
			var ans_input = $(this).attr('id').replace(/a_btn_clear_/g, '');
			MathQuill.MathField($('#a_input_mathquill_' + ans_input)[0]).revert();
			MathQuill.MathField($('#a_input_mathquill_' + ans_input)[0]).focus();
		}
		else{
			MathQuill.MathField($(ACTIVE_INPUT)[0]).revert();
			MathQuill.MathField($(ACTIVE_INPUT)[0]).focus();
		}
	});
	
	// Keyboard-listener for input-fields
	$(document).on('keyup', '.input_mathquill', function(e){
		var id = $(this).attr('id');
		if(id != undefined) {
			var id_group = id[0];
            if (e.keyCode >= 65 && e.keyCode <= 90){
                refresh_char_colors('#' + id);
            }
			else if (e.keyCode == 13) {
				if (id_group == 't') {
					$('#t_btn_ok').click();
				}
				else if (id_group == 'c') {
					$('#c_btn_ok').click();
				}
				else if (id_group == 'n') {
					$('#n_btn_ok').click();
				}
				else if(((id_group == 'q') || (id_group == 's') || (id_group == 'a')) && (id[1] != "e")){
					$('#' + id_group + '_btn_proceed').click();
				}
			}
		}
	}).on('keyup', '.dcg-template-mathquill', function(){
		refresh_char_colors('.dcg-template-mathquill');
	});

	// Proceed to next panel
	$('.btn_proceed').click(function(e){
		e.preventDefault();
		var btn_id = $(this).attr('id');
		btn_id = btn_id[0];
		if(btn_id == 'q'){
			if(TITLE_INSERTED){
				if(MathQuill.MathField($(Q_INPUT)[0]).latex() != ''){
					$('.btn-group-q').prop('disabled', true);
					var s_panel = $('#s_panel');
					s_panel.fadeIn(function(){
						redraw_mathquill_elements();
					});
					scroll_to(s_panel);
					$(S_INPUT).find('textarea').focus();
				}
				else{
					$(Q_INPUT).addClass('select_error');
					error_message('q_input_field', 'Dette feltet kan ikke være tomt.');
				}
			}
			else{
				$('#template_title').addClass('select_error');
				error_message('template_title', 'Skriv inn tittel.');
			}
		}
		else if(btn_id == 's'){
			var solution_valid = true;
			for(var step = 1; step <= STEP; step++){
				if(MathQuill.MathField($('#s_input_mathquill_' + step)[0]).latex() == ''){
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
					redraw_mathquill_elements();
				});
				scroll_to(a_panel);
				$(A_INPUT).find('textarea').focus()
			}
		}
		else if(btn_id == 'a'){
			var answer_valid = true;
			for(var ans = 1; ans <= ANSWER; ans++){
				if(MathQuill.MathField($('#a_input_mathquill_' + ans)[0]).latex() == ''){
					answer_valid = false;
					$('#a_input_mathquill_' + ans).addClass('select_error');
					error_message('answer_' + ans, 'Dette feltet kan ikke være tomt.');
				}
			}
			if(answer_valid == true){
				$('.btn-group-a').prop('disabled', true);
				var o_panel = $('#o_panel');
				o_panel.fadeIn(function(){
					redraw_mathquill_elements();
				});
				scroll_to(o_panel);
			}
		}
	});

	// SOLUTION-PANEL: Add new solution step
	$('#s_btn_next').click(function(e){
		e.preventDefault();
		$('#s_btn_del_' + STEP).hide();
		STEP++;
		$('#s_form').append(
			'<div id="step_'+STEP+'" class="step" style="display:none"><hr>' +
				'<h4>Steg '+STEP+'<a id="s_btn_del_'+STEP+'" class="glyphicon glyphicon-remove del_step" style="float:right"></a></h4>' +
				'<div class="input_field s_input_field">' +
					'<span id="s_input_mathquill_'+STEP+'" class="math-field form-control input_mathquill"></span>' +
					'<button id="s_btn_clear_'+STEP+'" class="btn btn-default btn_clear" style="margin-left:3px; border:none">' +
						'<span class="glyphicon glyphicon-trash" style="resize:vertical"></span>' +
					'</button>' +
				'</div>' +
			'</div>'
		);
		redraw_mathquill_elements();
		$('#step_' + STEP).fadeIn();
		S_INPUT = '#s_input_mathquill_' + STEP;
		scroll_to($('#step_' + STEP));
		$(S_INPUT).find('textarea').focus();
	});

	// ANSWER-PANEL: Add another answer
	$('#a_btn_next').click(function(e){
		e.preventDefault();
		$('#a_btn_del_' + ANSWER).hide();
		if(ANSWER == 1){
			$('#ans_title_1').show();
		}
		ANSWER++;
		$('#a_form').append(
			'<div id="answer_'+ANSWER+'" class="answer" style="display:none"><hr>' +
				'<h4>Svar '+ANSWER+'<a id="a_btn_del_'+ANSWER+'" class="glyphicon glyphicon-remove del_answer" style="float:right"></a></h4>' +
				'<div class="input_field a_input_field">' +
					'<span id="a_input_mathquill_'+ANSWER+'" class="math-field form-control input_mathquill"></span>' +
					'<button id="a_btn_clear_'+ANSWER+'" class="btn btn-default btn_clear" style="margin-left:3px; border:none">' +
						'<span class="glyphicon glyphicon-trash" style="resize:vertical"></span>' +
					'</button>' +
				'</div>' +
			'</div>'
		);
		redraw_mathquill_elements();
		$('#answer_' + ANSWER).fadeIn();
		A_INPUT = '#a_input_mathquill_' + ANSWER;
		scroll_to($('#answer_' + ANSWER));
		$(A_INPUT).find('textarea').focus();
	});

	// Add another text-substitution
	$('#e_btn_next').click(function(e){
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
			scroll_to($('#s_panel'));
		}
		else{
			scroll_to($('#step_' + STEP));
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
			scroll_to($('#a_panel'));
		}
		else{
			scroll_to($('#answer_' + ANSWER));
		}
		$(A_INPUT).find('textarea').focus();
	});

	// Close panel
	$('.btn_close').click(function(e){
		e.preventDefault();
		var btn_id = $(this).attr('id');
		btn_id = btn_id[0];
		close_panel(btn_id);
	});
	
	// Remove calculated reference buttons
	$(document).on('click', '.btn_calc_del', function(e){
		var id = parseInt($(this).attr('class').match(/[\d]+$/));
		$('.btn_calc_ref_' + id).popover('destroy').remove();
		delete dict_calc[id];
		delete dict_calc_unchanged[id];
		refresh_all_char_colors();
		e.stopPropagation();
	});

    // Edit calculation
    $(document).on('click', '.btn_calc_edit', function(e){
        e.stopPropagation();
        var id = parseInt($(this).attr('class').match(/[\d]+$/));
        $('.calc_variable').val(String.fromCharCode(65 + id)); // Get the correct variable from the id (A=0, B=1, C=2, etc).
        $('#calc_modal').modal('show').one('shown.bs.modal', function(){
            edit_calc = true;
            edit_calc_id = id;
            var latex = dict_calc_unchanged[id];
            write_to_mathfield(C_INPUT, latex);
            redraw_mathquill_elements();
            refresh_char_colors(C_INPUT);
        });
    });

	// Show advanced domain settings
	$('#o_btn_adv_domain').click(function(e){
		e.preventDefault();
		$('#o_adv_domain').fadeToggle();
		$('#o_adv_caret').toggleClass('dropup');
	});

	// Toggle the advance domain settings for one variable between a selection in a range and a selection with a list of numbers.
	$(document).on('change', '.o_btn_adv_sequence', function(){
		var id = $(this).attr('id').replace(/o_adv_sequence_/g, "");
		if($(this).is(':checked')){
			$('#o_adv_'+id).children().nextAll().slice(0, 3).each(function(){
				$(this).fadeOut(function(){
					$('#o_adv_sequence_container_'+id).fadeIn();
				});
			});
		} else {
			$('#o_adv_sequence_container_'+id).fadeOut(function(){
				$('#o_adv_'+id).children().nextAll().slice(0, 3).each(function(){
					$(this).fadeIn();
				});
			});
		}
	});

	// Adding sequential domains.
	$(document).on('focusout', '.seq_input', function() {
		var seq = get_latex_from_mathfield(this);
		if (seq) {
			$(this).before('<span class="o_seq"><span class="math-field static-math-sm">' + seq + '</span><a class="btn btn_tag_del">x</a></span>');
			MathQuill.MathField($(this)[0]).select().write(""); // reset the mathquill-input
			redraw_mathquill_elements();
		}
	}).on('keyup', '.seq_input', function(e){
		if(/(188|13)/.test(e.which)) { // Add tag if one of these keys are pressed.
            $(this).focusout();
		}
	});

	// Domain input-insertion to advanced settings
	$('#opt_domain_from').on('input', function(){
		$('.opt_domain_from').val($('#opt_domain_from').val());
	});
	$('#opt_domain_to').on('input', function(){
		$('.opt_domain_to').val($('#opt_domain_to').val());
	});
	$('#opt_domain_dec').on('input', function(){
		$('.opt_domain_dec').val($('#opt_domain_dec').val());
	});

	// Open condition modal
	$('#opt_conditions').click(function(){
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
	$('#opt_multiple_choice').change(function(){
		if ($(this).is(':checked')) {
			refresh_multiple_choice();
			$('#multiple_choice_modal').modal('show').on('shown.bs.modal', function () {
				refresh_multiple_choice_template();
				for(var n = 1; n <= STEP; n ++){
					refresh_char_colors('#m_sol_template_' + n);
				}
				for(var m = 1; m <= MULTI_CHOICE; m++){
					MathQuill.MathField($('#m_input_mathquill_' + m)[0]).reflow();
					refresh_char_colors('#m_input_mathquill_' + m);
				}
				redraw_mathquill_elements();
			});
		}
	});

	// Add new multiple-choices
	$('#m_btn_new').click(function(e){
		e.preventDefault();
		$('#m_btn_del_' + MULTI_CHOICE).hide();
		MULTI_CHOICE++;
		$('#m_dyn_multi_input').append(
			'<div id="m_field_'+MULTI_CHOICE+'" class="input_field multi_field">' +
				'<span id="m_input_mathquill_'+MULTI_CHOICE+'" class="math-field form-control input_mathquill"></span>'+
				'<a id="m_btn_del_'+MULTI_CHOICE+'" class="glyphicon glyphicon-remove pull-right del_multi"></a>' +
			'</div>' +
			'<label for="m_checkbox_'+MULTI_CHOICE+'">Forenkle:<input id="m_checkbox_'+MULTI_CHOICE+'" type="checkbox"></label>'
		);
		redraw_mathquill_elements();
	});

	// Delete last multiple-choice
	$(document).on('click', '.del_multi', function(e){
		e.preventDefault();
		$('#m_field_' + MULTI_CHOICE).remove();
		$('#m_checkbox_' + MULTI_CHOICE).parent().remove();
		MULTI_CHOICE--;
		$('#m_btn_del_' + MULTI_CHOICE).show();
	});

	// Open fill-in-the-blanks modal
	$('#opt_fill_blanks').change(function(){
		if($(this).is(':checked')){
			$('#fill_blanks_modal').modal('show').on('shown.bs.modal', function () {
				if(FILL_IN == false){
					refresh_fill_in_content();
					FILL_IN = true;
				}
				redraw_mathquill_elements();
			});
		}
	});

	// Refresh fill-in-the-blanks content
	$('#f_btn_refresh').click(function(e){
		e.preventDefault();
		refresh_fill_in_content();
		redraw_mathquill_elements();
	});

	// Replace selected elements with blanks
	$('#f_btn_fill').mousedown(function(e){
		e.preventDefault();
		write_to_mathfield(get_input_field(this), '■'); // Black square HEX: &#x25A0
		//alert(get_diff_latex());
	});

	// Redraws the rendered-math in keypad in the calculation-modal
	$('#calc_modal').on('shown.bs.modal', function () {
		redraw_mathquill_elements();
		ACTIVE_INPUT = C_INPUT;
		MathQuill.MathField($(C_INPUT)[0]).focus();
	});

	// Initiate the slider which sets the templates difficulty for normal/multiple-choice/fill-in-the-blanks.
	reset_difficulty('normal');
	reset_difficulty('multiple');
	reset_difficulty('blanks');

	// Adding new required input tag.
	$('#tags_required').find('.input_mathquill').on('focusout', function(){
		var tag = get_latex_from_mathfield(this);
		if(tag){
			$(this).before('<span class="tag_r"><span class="math-field static-math-sm">'+tag+'</span><a class="btn btn_tag_del">x</a></span>');
			MathQuill.MathField($(this)[0]).select().write(""); // reset the mathquill-input
			redraw_mathquill_elements();
		}
	}).on('keyup', function(e){
		if(/(13)/.test(e.which)) { // Add tag if one of these keys are pressed.
			e.stopPropagation();
			$(this).focusout();
		}
	});

	// Adding new illegal input tag.
	$('#tags_illegal').find('.input_mathquill').on('focusout', function(){
		var tag = get_latex_from_mathfield(this);
		if(tag){
			$(this).before('<span class="tag_i"><span class="math-field static-math-sm">'+tag+'</span><a class="btn btn_tag_del">x</a></span>');
			MathQuill.MathField($(this)[0]).select().write(""); // reset the mathquill-input
			redraw_mathquill_elements();
		}
	}).on('keyup', function(e){
		if(/(13)/.test(e.which)) { // Add tag if one of these keys are pressed.
			e.stopPropagation();
			$(this).focusout();
		}
	});

	// Adding new tag from the value in the input-field.
	$('#tags').find('input').on('focusout', function(){
		var tag = $(this).val().replace(/[^a-zA-Z0-9\+\-\.#ÆØÅæøåA]/g,''); // Allowed characters
		if(tag){
			$(this).before('<span class="tag">'+ tag.toLowerCase() +'<a class="btn btn_tag_del">x</a></span>');
		}
		$(this).val("");
	}).on('keyup', function(e){
		if(/(188|13)/.test(e.which)) $(this).focusout(); // Add tag if one of these keys are pressed.
	});

	// Delete a tag
	$(document).on('click', '.btn_tag_del', function(e){
		e.preventDefault();
		$(this).parent().remove();
	});

	// Retrieve and insert calculation to solution
	$('#c_btn_ok').click(function(e){
		e.preventDefault();
        if(edit_calc){
            $('.btn_calc_ref_' + edit_calc_id).popover('destroy').remove();
		    delete dict_calc[edit_calc_id];
		    delete dict_calc_unchanged[edit_calc_id];
            edit_calc = false;
        }
		if(get_latex_from_mathfield(C_INPUT) != "") {
            var calc_var = $('.calc_variable');
            var variable = calc_var.val();
            if (variable) {
                if (variable.match(/^[A-Z]+$/g)) {
                    var id = variable.charCodeAt(0) - 65; // Get the unique variable-id (A=0, B=1, C=2, etc).
                    if ($('.btn_calc_ref_' + id).length) {
                        error_message('.calc_variable', "Tegn allerede i bruk!");
                    } else {
                        init_new_calculation(variable, id);
                        $('#calc_modal').modal('hide');
                    }
                    calc_var.val("");
                } else {
                    error_message('.calc_variable', "Ugyldig tegn!");
                    calc_var.val("");
                }
            } else {
                error_message('.calc_variable', "Velg variabel!");
            }
        } else {
            error_message(C_INPUT, "Fyll ut!");
        }
	});

	// Submit template to database / Update
	$('#o_btn_save').click(function(e){
		e.preventDefault();
		if(submit_validation()){
			SUBMITTING = true;
			submit_template();
		}
	});

	// Submit template as a new template / Modified
	$('#o_btn_save_new').click(function(e){
		e.preventDefault();
		if(submit_validation()){
			SUBMIT_AS_NEW = true;
			SUBMITTING = true;
			submit_template();
		}
	});
});

/**
 * Submit template to database.
 * Iterating and collect all data from user-inputs in both parsed and original LaTeX form (for editing).
 * Store each data in corresponding dictionaries(objects), before posting to database.
 */
function submit_template(){
	var form_submit = {};
	// TITLE
	form_submit['name'] = $('#template_title').val();

	// QUESTION_TEXT
	form_submit['question_text'] = convert_variables(get_latex_from_mathfield(Q_INPUT));
	form_submit['question_text_latex'] = get_latex_from_mathfield(Q_INPUT);

	// SOLUTION
	var tmp_solution = [];
	var tmp_solution_latex = [];
	for (var i = 1; i <= STEP; i++) {
		tmp_solution.push(convert_variables(get_latex_from_mathfield('#s_input_mathquill_' + i)));
		tmp_solution_latex.push(get_latex_from_mathfield('#s_input_mathquill_' + i));
	}
	form_submit['solution'] = tmp_solution.join('§');
	form_submit['solution_latex'] = tmp_solution_latex.join('§');

	// ANSWER
	var tmp_answer = [];
	var tmp_answer_latex = [];
	for (var i = 1; i <= ANSWER; i++) {
		tmp_answer.push(convert_variables(get_latex_from_mathfield('#a_input_mathquill_' + i)));
		tmp_answer_latex.push(get_latex_from_mathfield('#a_input_mathquill_' + i));
	}
	form_submit['answer'] = tmp_answer.join('§');
	form_submit['answer_latex'] = tmp_answer_latex.join('§');

	// RANDOM_DOMAIN
	if(VARIABLE_COUNT > 0){
        var domain_dict = {};
		$('.o_adv_dyn').each(function(){
			var v = $(this).attr('id').replace(/o_adv_/g, "");
            var name = "";
            if ($('#o_adv_sequence_'+ v).is(':checked')) {
                name = convert_variables($('#o_adv_' + v).children().first().text().replace(/:/g, ""));
                var sequence = [];
                $('#o_adv_sequence_container_'+ v).find('.o_seq').each(function () {
                    sequence.push(get_latex_from_mathfield($(this).find('.static-math-sm')));
                });
                domain_dict[name] = [sequence, true];
            } else {
                name = convert_variables($('#o_adv_' + v).children().first().text().replace(/:/g, ""));
                var from = $('#o_adv_from_' + v).val();
                var to = $('#o_adv_to_' + v).val();
                var dec = $('#o_adv_dec_' + v).val();
                domain_dict[name] = [[from, to, dec], false];
            }
        });
        form_submit['random_domain'] = JSON.stringify(domain_dict);
	}
	else{
		form_submit['random_domain'] = "";
	}

	// MARGIN OF ERROR
	var margin = $('#opt_margin_of_error');
	if(margin.val() != ""){
		form_submit['margin_of_error'] = margin.val();
	} else {
		form_submit['margin_of_error'] = 0;
	}

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
		form_submit['conditions'] = parse_conditions(convert_variables(get_latex_from_mathfield(N_INPUT)));
		form_submit['conditions_latex'] = get_latex_from_mathfield(N_INPUT);
	}
	else {
		form_submit['conditions'] = "";
		form_submit['conditions_latex'] = "";
	}

	// GRAPH
	var expressions = [];
	var colors = [];
	var graph_settings = "";
	if ($('#opt_graph').is(':checked')) {
		if(MODIFY && !GRAPH_MODIFIED){
			expressions = JSON.parse($('#get_graph').text());
			colors = JSON.parse($('#get_graph_color').text());
			graph_settings = JSON.parse($('#get_graph_settings').text());
		} else {
			var dcg_expr = dcg_get_expressions();
			expressions = dcg_expr['latex'];
			colors = dcg_expr['color'];
			graph_settings = dcg_get_graph_settings();
		}
		form_submit['unchanged_graph'] = JSON.stringify(expressions);
		for(var e = 0; e < expressions.length; e++){
			expressions[e] = convert_variables(expressions[e]);
		}
		form_submit['graph'] = JSON.stringify(expressions);
		form_submit['graph_color'] = JSON.stringify(colors);
		form_submit['graph_settings'] = JSON.stringify(graph_settings);
	} else {
		form_submit['graph'] = JSON.stringify(expressions);
		form_submit['unchanged_graph'] = JSON.stringify(expressions);
		form_submit['graph_color'] = JSON.stringify(colors);
		form_submit['graph_settings'] = "";
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
		form_submit['fill_in'] = convert_variables(get_diff_latex());
		var f_content = [];
		for(var f = 1; f <= STEP; f++){
			f_content.push(get_latex_from_mathfield('#f_fill_content_' + f));
		}
		form_submit['fill_in_latex'] = f_content.join('§');
	}
	else {
		form_submit['fill_in'] = "";
		form_submit['fill_in_latex'] = "";
	}

	// CALCULATION REFERENCE
	var calc = [];
	var calc_ref = [];
	for(var c in dict_calc){
		calc.push(c + '§' + dict_calc[c]);
		calc_ref.push(c + '§' + dict_calc_unchanged[c]);
	}
	form_submit['calculation_ref'] = calc.join('§');
	form_submit['unchanged_ref'] = calc_ref.join('§');

	// USED VARIABLES
	var variables = [];
	for(var vars in VARIABLES){
		variables.push(VARIABLES[vars]);
	}
	form_submit['used_variables'] = variables.join(' ');

	// DIFFICULTY
	form_submit['difficulty'] = (parseInt($('#difficulty_amount').text()));
	form_submit['difficulty_multiple'] = (parseInt($('#m_difficulty_amount').text()));
	form_submit['difficulty_blanks'] = (parseInt($('#f_difficulty_amount').text()));

	// ILLEGAL SIGNS
	var disallowed = [];
	var unchanged_disallowed = [];
	$('.tag_i').each(function(){
		disallowed.push(convert_variables(get_latex_from_mathfield($(this).find('.static-math-sm'))));
		unchanged_disallowed.push(get_latex_from_mathfield($(this).find('.static-math-sm')));
	});
	form_submit['disallowed'] = JSON.stringify(disallowed);
	form_submit['unchanged_disallowed'] = JSON.stringify(unchanged_disallowed);

	// REQUIRED SIGNS
	var required = [];
	var unchanged_required = [];
	$('.tag_r').each(function(){
		required.push(convert_variables(get_latex_from_mathfield($(this).find('.static-math-sm'))));
		unchanged_required.push(get_latex_from_mathfield($(this).find('.static-math-sm')));
	});
	form_submit['required'] = JSON.stringify(required);
	form_submit['unchanged_required'] = JSON.stringify(unchanged_required);

	// TAGS
	var tags = [];
	$('.tag').each(function(){
		tags.push($(this).text().slice(0,-1));
	});
	form_submit['tags_list'] = tags.join('§');

	// CSRF_TOKEN
	form_submit["csrfmiddlewaretoken"] = getCookie('csrftoken');

	// TYPE
	form_submit['type'] = 'normal';

	// PRIMARY-KEY
	if(MODIFY && !SUBMIT_AS_NEW){
		form_submit['pk'] = $('#template_id').text();
	}
	else{
		form_submit['pk'] = "";
	}

	//// Testing output TODO: When finished testing, switch to submit method.
	//var test_output = [];
	//for(var s in form_submit){
	//	test_output.push(s + '\n' + form_submit[s]);
	//}
	//alert(test_output.join('\n'));

	// SUBMIT
	post(/submit/, form_submit);
}

/**
 * Initialize a new variable. Store it and make it available with buttons.
 * @param {String} variable - The letter to store as a variable.
 */
function init_new_variable(variable){
    var id = get_converted_variable(variable).replace(/R/g, "");
    $('#q_btn_var_dyn').append('' +
        '<div id="q_btn_abc_' + id + '" class="btn btn-danger btn_var_abc btn_var_abc_q btn_keypad">' + variable +
            '<a id="q_btn_abc_del_' + id + '" class="btn btn-danger btn-xs btn_var_del">x</a>' +
        '</div>');
    $('.btn_var_dyn').append('<button class="btn btn-danger btn_var_abc btn_var_' + id + ' btn_keypad">' + variable + '</button>');
    $('#o_adv_domain').append(
        '<tr id="o_adv_' + id + '" class="active o_adv_dyn">' +
            '<td style="vertical-align: middle; text-align: right; color: #D9534F">' + variable + ':</td>' +
            '<td><input id="o_adv_from_' + id + '" type="number" class="form-control input-sm opt_domain_from" placeholder="Fra:"></td>' +
            '<td><input id="o_adv_to_' + id + '" type="number" class="form-control input-sm opt_domain_to" placeholder="Til:"></td>' +
            '<td style="border-left: thin dashed lightgray"><input id="o_adv_dec_' + id + '" type="number" class="form-control input-sm opt_domain_dec" placeholder="Desimaler:"></td>' +
            '<td id="o_adv_sequence_container_' + id + '" style="display:none" colspan="3" class="sequence_input"><span id="sequence_input_' + id + '" class="math-field form-control input_mathquill seq_input"></span></td>' +
            '<td style="vertical-align: middle"><input id="o_adv_sequence_' + id + '" class="o_btn_adv_sequence" type="checkbox"> Sekvens</td>' +
        '</tr>');
    update_variable_count();
    refresh_all_char_colors();
    refresh_variables();
}

/**
 * Initialize a new calculation with a variable as a reference. Store it and make it available with buttons.
 * @param {String} variable - The variable-reference of the calculation (A, B, C, etc).
 * @param {Number} id - The id of the variable-reference.
 */
function init_new_calculation(variable, id){
    var c_latex = MathQuill.MathField($(C_INPUT)[0]).latex();
    var la = convert_variables(c_latex);
    la = la.replace(/\?/g, '');
    la = la.replace(/@/g, '');
    dict_calc[id] = '@?(' + la + ')?@';
    dict_calc_unchanged[id] = c_latex;
    MathQuill.MathField($(C_INPUT)[0]).revert();
    $('.btn_calc_dyn').append(
        '<div class="btn btn-success btn_calc btn_keypad btn_calc_ref btn_calc_ref_' + id + '">' + variable +
            '<a class="btn btn-success btn-xs btn_calc_del btn_calc_del_' + id + '"><span>x</span></a>' +
            '<a class="btn btn-success btn-xs btn_calc_edit btn_calc_edit_' + id + '">' +
                '<span class="glyphicon glyphicon-pencil"></span>' +
            '</a>' +
        '</div>'
    );
    $('.btn_calc_dyn_ref').append(
        '<button class="btn btn-success btn_calc btn_keypad btn_calc_ref_' + id + '">' + variable + '</button>'
    );
    $('.btn_calc_ref_' + id).popover({
        html: true,
        content: '<img src="http://latex.codecogs.com/svg.latex?' + c_latex + '" border="0"/>',
        placement: 'top',
        trigger: 'hover',
        container: 'body'
    });
    refresh_all_char_colors();
}

/**
 * Initialize the difficulty sliders, with either the default value or the given value from the server.
 * @param {String} type - Which kind of difficulty to initialize/reset (normal/multiple-choice/fill-in-the-blanks).
 */
function reset_difficulty(type){
	if(type == 'normal'){
		var difficulty = $('#get_difficulty').text();
		if (difficulty == '') {
			difficulty = 5;
		}
		$('#difficulty_slider').slider({
			value: parseInt(difficulty),
			min: 1,
			max: 25,
			step: 1,
			slide: function (event, ui) {
				$('#difficulty_amount').text(ui.value);
			}
		});
		$('#difficulty_amount').text(difficulty);
	}
	else if(type == 'multiple'){
		var m_difficulty = $('#get_difficulty_m').text();
		if (m_difficulty == '') {
			m_difficulty = 5;
		}
		$('#m_difficulty_slider').slider({
			value: parseInt(m_difficulty),
			min: 1,
			max: 25,
			step: 1,
			slide: function (event, ui) {
				$('#m_difficulty_amount').text(ui.value);
			}
		});
		$('#m_difficulty_amount').text(m_difficulty);
	}
	else if(type == 'blanks'){
		var f_difficulty = $('#get_difficulty_f').text();
		if (f_difficulty == '') {
			f_difficulty = 5;
		}
		$('#f_difficulty_slider').slider({
			value: parseInt(f_difficulty),
			min: 1,
			max: 25,
			step: 1,
			slide: function (event, ui) {
				$('#f_difficulty_amount').text(ui.value);
			}
		});
		$('#f_difficulty_amount').text(f_difficulty);
	}
}

/**
 * Checks which input-field the user is currently at.
 * @param {object} obj - The current object the user is operating with, which will return the input-field it's
 * corresponding to.
 * @returns {string} - The id of the current input-field.
 */
function get_input_field(obj){
	var group = $(obj).closest('.keypad').attr('id').replace(/keypad_/g, "");
	if(group == 'q'){
		return Q_INPUT;
	}
	else if(group == 's'){
		return S_INPUT;
	}
	else if(group == 'c'){
		return C_INPUT;
	}
	else if(group == 'a'){
		return A_INPUT;
	}
	else if(group == 'w'){
		return W_INPUT;
	}
	else if(group == 'm'){
		return M_INPUT;
	}
	else if(group == 'f'){
		return F_INPUT;
	}
	else if(group == 'n'){
		return N_INPUT;
	}
}

/**
 * Takes in a LaTeX string and converts variables (a,b,c,d.. etc) to computable ids (R0R,R1R,R2R,.. etc),
 * and calculated references (A,B,C, etc) with its content. The LaTeX string will also get cleaned/optimized.
 * @param {string} latex - The LaTeX string to iterate and convert.
 * @returns {string} la - The cleaned/optimized LaTeX string with converted variables.
 */
function convert_variables(latex){
	var la = latex;
	la = la.replace(/\\cdots/g, '\\cdot ');
	la = la.replace(/\\cdot/g,'\\cdot ');
	la = la.replace(/\\&/g, '&');
	la = la.replace(/\\ln/g, '\\ln ');
	la = la.replace(/\\sin/g, '\\sin ');
	la = la.replace(/\\cos/g, '\\cos ');
	la = la.replace(/\\circ/g, '{\\circ }');
	var counter = 0;
	var dict_letters = {'a' : 'R0R', 'b' : 'R1R', 'c' : 'R2R', 'g' : 'R6R', 'h' : 'R7R', 'j' : 'R9R', 'k' : 'R10R',
						'l' : 'R11R', 'm' : 'R12R', 'n' : 'R13R', 'o' : 'R14R', 'p' : 'R15R', 'q' : 'R16R', 'r' : 'R17R', 's' : 'R18R', 't' : 'R19R',
						'u' : 'R20R', 'v' : 'R21R', 'w' : 'R22R', 'A' : dict_calc[0] , 'B' : dict_calc[1],'C' : dict_calc[2],'D' : dict_calc[3],
						'E' : dict_calc[4],'F' : dict_calc[5],'G' : dict_calc[6],'H' : dict_calc[7],'I' : dict_calc[8], 'J' : dict_calc[9],
						'K' : dict_calc[10],'L' : dict_calc[11],'M' : dict_calc[12],'N' : dict_calc[13],'O' : dict_calc[14], 'P' : dict_calc[15],
						'Q' : dict_calc[16],'R' : dict_calc[17],'S' : dict_calc[18],'T' : dict_calc[19],'U' : dict_calc[20], 'V' : dict_calc[21]};
	var la2 = '';
	// Iteration for adding required {} to single exponents and subscripts.
	for(var j = 0; j < la.length; j++){
		if(la[j] == '^' || la[j] == '_'){
			if(la[j+1] != '{' && la[j+1] != '@'){
				la = la.substring(0, j+1) + '{' + la[j+1] + '}' + la.substring(j+2, la.length);
			} // Workaround for fill in. this fixes x^2 -> x^{@}xxxx@ to x^{@xxxx@}.
			else if(la[j+1] == '@' && la[j+2] == 'x' && la[j+8] == '@') {  //find the opening @xxxx@, insert { before.
				la = la.substring(0, j+1) + '{' + la.substring(j+1, j+14) + '}'+ la.substring(j+14, la.length);
			}
		}
	}
	// Iteration for converting variables to computable values, and fixing conflicts with latex-commands.
	for(var i = 0; i < la.length; i++) {
		try {
			if (la[i] == '\\') {
				if ((la[i + 1] == 't' && la[i + 2] == 'e' && la[i + 3] == 'x' && la[i + 4] == 't') ||
					(la[i + 1] == 'b' && la[i + 2] == 'e' && la[i + 3] == 'g' && la[i + 4] == 'i' && la[i + 5] == 'n') ||
					(la[i + 1] == 'e' && la[i + 2] == 'n' && la[i + 3] == 'd')) { //FIXME: some variables is not converted inside the matrix.
					while (true) {
						if (la[i] == '}' && counter == 0) {
							break
						}
						if (la[i] == '{') {
							counter++;
						}
						else if (la[i + 1] == '}') {
							counter--;
						}
						la2 += la[i];
						i++;
					}
				}
				else if (la[i + 1] == '\\') {
					la2 += '\\\\';
					i++;
					continue
				}
				else if (la[i + 1] == 'l' && la[i + 2] == 'e' && la[i + 3] == 'f' && la[i + 4] == 't') {
					la2 += '\\left';
					i += 5;
					if (la[i + 5] == 'a' && la[i + 6] == 'r' && la[i + 7] == 'r' && la[i + 8] == 'o'){
						la2 += 'arrow';
						i += 5;
					}

				}
				else if (la[i + 1] == 'r' && la[i + 2] == 'i' && la[i + 3] == 'g' && la[i + 4] == 'h' && la[i + 5] == 't') {
					la2 += '\\right';
					i += 6;
					if (la[i + 6] == 'a' && la[i + 7] == 'r' && la[i + 8] == 'r' && la[i + 9] == 'o'){
						la2 += 'arrow';
						i += 5;
					}
				}
				else if (la[i + 1] == 'c' && la[i + 2] == 'd' && la[i + 3] == 'o' && la[i + 4] == 't') {
					la2 += '\\cdot ';
					i += 5;
				}
				else if (la[i + 1] == 'n') {
					la2 += '\\n';
					i++;
					continue
				}
				else {
					// Iterating through the string after backslash '\' for inserting LaTeX-text that is not meant to
					// be parsed as computable values. Checking for 'undefined' at the end of line if the LaTeX-command
					// is the last thing in the string to prevent an endless loop.
					// 		- alternative: add a whitespace at the end of string.
					while (la[i] != '{' && la[i] != ' ' && la[i] != '_' && la[i] != '^' && la[i] != undefined) {
						la2 += la[i];
						i++;
						if (la[i] == '\\') {
							break
						}
					}
					if (la[i] == '\\' || la[i] == undefined) {
						i--;
						continue
					}
				}
			}
            //TODO:  Use get_converted_variable() instead of dict_letters.
			// Check if following char is a valid variable. (If the variable is stored in VARIABLES dictionary.)
			var variable_valid = false;
			if(get_converted_variable(la[i]) != undefined){
				variable_valid = VARIABLES[parseInt(get_converted_variable(la[i]).replace(/R/g, ''))] != undefined;
			}
			if (la[i] in dict_letters && (variable_valid || la[i].match(/^[A-Z]*$/))) {
				// If the char is a capital-letter and doesn't have a calculated variable, set the char as is.
				var get_dict_letters = get_converted_variable(la[i]);
				if(la[i].match(/^[A-Z]*$/) && get_dict_letters == undefined){
					get_dict_letters = la[i];
				}
				if ((la[i - 1] in dict_letters || la[i - 1] == ')' || !isNaN(la[i - 1])) && la[i - 2] != '\^' && la[i - 2] != '\\') {
					if (la[i - 1] != ' ' && la[i - 2] != 't' && la[i - 3] != 'o' && la[i - 4] != 'd' && la[i - 5] != 'c') {
						la2 += '\\cdot ' + get_dict_letters;
					}
					else {
						la2 += get_dict_letters;
					}
				}
				else {
					if (la[i - 1] == '\@' && la[i - 2] == 'x' && la[i - 3] == 'x' && la[i - 4] == 'x' && la[i - 5] == 'x' && la[i - 6] == '\@') {
						if ((la[i - 7] in dict_letters || la[i - 7] == ')' || !isNaN(la[i - 7])) && la[i - 8] != '\^' && la[i - 8] != '\\') {
							la2 += '\\cdot ' + get_dict_letters;
						}
						else {
							la2 += get_dict_letters;
						}
					}
					else if (la[i - 1] == '\\' && la[i - 2] == '\\') { 	//Quick-Fix to solve the LaTeX parsing error with Matrices.
						la2 += '\\' + get_dict_letters;		 		//Adding additional '\' in the LaTeX string.
					}
					else {
						if (la[i - 1] != '\\') {
							la2 += get_dict_letters;
						}
					}
				}
				if (la[i + 1] == '(') {
					la2 += '\\cdot ';
				}
			}
			else {
				la2 += la[i];
			}
		} catch(e){
			window.console.log(e);
			window.console.log('LaTeX-string: ' + la);
			window.console.log('Error at char-index '+i+': ' + la[i]);
		}
	}
	la = la2;
	return la;
}

/**
 * Close specific panel including underlying panels + reset all input-values.
 * @param {string} panel - Identifier for which panel to close.
 */
function close_panel(panel){
	if(panel == 's'){
		$('#o_panel').fadeOut();
		$('.btn-group-a').prop('disabled', false);
		if(ANSWER > 1){
			for(var ans = 2; ans <= ANSWER; ans++){
				$('#answer_' + ans).remove();
			}
		}
		ANSWER = 1;
		A_INPUT = '#a_input_mathquill_' + ANSWER;
		MathQuill.MathField($(A_INPUT)[0]).revert();
		$('#a_panel').fadeOut();
		$('.btn-group-s').prop('disabled', false);
		if(STEP > 1){
			for(var step = 2; step <= STEP; step++){
				$('#step_' + step).remove();
			}
		}
		STEP = 1;
		S_INPUT = '#s_input_mathquill_' + STEP;
		MathQuill.MathField($(S_INPUT)[0]).revert();
		$('#s_panel').fadeOut();
		$('.btn-group-q').prop('disabled', false);
		scroll_to($('#q_panel'));
		$(Q_INPUT).find('textarea').focus();
	}
	else if(panel == 'c'){
		MathQuill.MathField($(C_INPUT)[0]).revert();
        $('.calc_variable').val("");
	}
	else if(panel == 'a'){
		$('#o_panel').fadeOut();
		$('.btn-group-a').prop('disabled', false);
		if(ANSWER > 1){
			for(var ans = 2; ans <= ANSWER; ans++){
				$('#answer_' + ans).remove();
			}
		}
		ANSWER = 1;
		A_INPUT = '#a_input_mathquill_' + ANSWER;
		MathQuill.MathField($(A_INPUT)[0]).revert();
		$('#a_panel').fadeOut();
		$('#ans_title_1').hide();
		$('.btn-group-s').prop('disabled', false);
		if(STEP == 1){
			scroll_to($('#s_panel'));
		}
		else{
			scroll_to($('#step_' + STEP));
		}
		$(S_INPUT).find('textarea').focus();
	}
	else if(panel == 'o'){
		$('#o_panel').fadeOut();
		$('.btn-group-a').prop('disabled', false);
		if(ANSWER == 1){
			scroll_to($('#a_panel'));
		}
		else{
			scroll_to($('#answer_' + ANSWER));
		}
		$(A_INPUT).find('textarea').focus();
	}
}

/**
 * Redraws all mathquill elements in the document. To achieve a redraw, the mathquill element is required to have either
 * of class-name 'static-math' or 'math-field', depending if the element is an editable math-field or a static one.
 */
function redraw_mathquill_elements(){
	$('.static-math').each(function() {
		MathQuill.StaticMath(this).reflow();
	});
	$('.math-field').each(function() {
		MathQuill.MathField(this).reflow();
	});
}

/**
 * Write LaTeX to the selected math-field, which renders as readable math.
 * @param {selector|object} input - which input-field to write to.
 * @param {string} latex - the LaTeX to write.
 */
function write_to_mathfield(input, latex){
	MathQuill.MathField($(input)[0]).write(latex).focus();
}

/**
 * Write LaTeX-commands to the selected math-field.
 * @param {selector|object} input - which input-field to write to.
 * @param {string} latex - the LaTeX-command to write.
 */
function cmd_to_mathfield(input, latex){
	MathQuill.MathField($(input)[0]).cmd(latex).focus();
}

/**
 * Get the LaTeX-string from the specific math-field.
 * @param {selector|object} mathfield - which field to retrieve the LaTeX.
 * @returns {string} the LaTeX-string.
 */
function get_latex_from_mathfield(mathfield){
	return MathQuill.MathField($(mathfield)[0]).latex();
}

/**
 * Simulates keystrokes to the selected math-field.
 * @param {selector|object} input - which input-field to write to.
 * @param {string} keystroke - which keys to simulate ("Left", "Backspace", etc)
 * @param {int} times - how many times to simulate the keystroke (default: 1).
 */
function simulate_keystroke(input, keystroke, times){
	if(times){
		for(var i = 0; i < times; i++){
			MathQuill.MathField($(input)[0]).keystroke(keystroke);
		}
	}
	else{
		MathQuill.MathField($(input)[0]).keystroke(keystroke);
	}
}

/**
 * Visually draws the custom-matrix in the popover, by highlighting the cell and the connected ones.
 * @param {object} obj - The selector of the cell that the mouse enters.
 */
function preview_custom_matrix(obj){
	obj.addClass('highlighted').prevAll().addClass('highlighted');
	obj.nextAll().removeAttr('class');
	var col_pos = obj.index() + 1;
	obj.parent().prevAll().find('td').addClass('highlighted').filter(':nth-child('+ (col_pos) +')').nextAll().removeAttr('class');
	obj.parent().nextAll().find('td').removeAttr('class');
}

/**
 * Retrieves the size of the custom matrix.
 * @param {object} obj - The current cell that the mouse is hovering.
 * @returns {string} The size (x,y).
 */
function get_custom_matrix_size(obj){
	var col = obj.index() + 1;
	var row = obj.parent().prevAll().length + 1;
	return col + 'x' + row;
}

/**
 * Get a generated LaTeX-string of a custom-matrix with a given size.
 * @param {number|String} col - The column-size.
 * @param {number|String} row - The row-size.
 * @returns {string} The generated LaTeX-string of the custom-matrix.
 */
function get_custom_matrix_latex(col, row){
	var start = "\\begin{pmatrix}";
	var end = "\\end{pmatrix}";
	var col_str = "";
	for(var i = 1; i <= col; i++){
		if((i == 1)){
			col_str += "{}";
		}
		else{
			col_str += "&{}"
		}
	}
	var latex = col_str;
	for(var j = 1; j <= row; j++){
		if(j > 1){
			latex += "\\\\" + col_str;
		}
	}
	return start + latex + end;
}

/**
 * Get the converted string of the single variable or calculated-variable.
 * @param {String} variable - The single letter to convert.
 * @returns {String|*} The converted variable.
 */
function get_converted_variable(variable){
    var dict_letters = {
        'a' : 'R0R', 'b' : 'R1R', 'c' : 'R2R', 'd': 'R3R', 'e' : 'R4R', 'f' : 'R5R', 'g' : 'R6R', 'h' : 'R7R',
        'i' : 'R8R', 'j' : 'R9R', 'k' : 'R10R', 'l' : 'R11R', 'm' : 'R12R', 'n' : 'R13R', 'o' : 'R14R', 'p' : 'R15R',
        'q' : 'R16R', 'r' : 'R17R', 's' : 'R18R', 't' : 'R19R', 'u' : 'R20R', 'v' : 'R21R', 'w' : 'R22R',
        'x' : 'R23R', 'y' : 'R24R', 'z' : 'R25R',
        'A' : dict_calc[0], 'B' : dict_calc[1], 'C' : dict_calc[2], 'D' : dict_calc[3], 'E' : dict_calc[4],
        'F' : dict_calc[5], 'G' : dict_calc[6], 'H' : dict_calc[7], 'I' : dict_calc[8], 'J' : dict_calc[9],
        'K' : dict_calc[10], 'L' : dict_calc[11], 'M' : dict_calc[12], 'N' : dict_calc[13], 'O' : dict_calc[14],
        'P' : dict_calc[15], 'Q' : dict_calc[16],'R' : dict_calc[17],'S' : dict_calc[18],'T' : dict_calc[19],
        'U' : dict_calc[20], 'V' : dict_calc[21], 'W' : dict_calc[22], 'X' : dict_calc[23], 'Y' : dict_calc[24],
        'Z' : dict_calc[25]};

    return dict_letters[variable];
}

/**
 * Updates the unique variable counter. To track whether or not to disable random domain settings.
 * If there's no variables, disabled unneeded fields (or vice-versa).
 */
function update_variable_count(){
	VARIABLE_COUNT = $('#q_btn_var_dyn').children().length-1;
	if(VARIABLE_COUNT > 0){
		$('#opt_domain_from').prop('disabled', false);
		$('#opt_domain_to').prop('disabled', false);
		$('#opt_domain_dec').prop('disabled', false);
		$('#o_btn_adv_domain').prop('hidden', false);
	}
	else{
		$('#opt_domain_from').prop('disabled', true);
		$('#opt_domain_to').prop('disabled', true);
		$('#opt_domain_dec').prop('disabled', true);
		$('#o_btn_adv_domain').prop('hidden', true);
	}
}

/**
 * Scroll to specific element given by id.
 * @param id - id of element to scroll to.
 */
function scroll_to(id){
	$('html,body').animate({scrollTop: id.offset().top - 65}); // -65 because of the navbar.
}

/**
 * Add an error message under the given element.
 * @param {string} selector - id or class-name of the element to apply error message to.
 * @param {string} message - the error message.
 */
function error_message(selector, message){
	var element = $(selector);
    if(selector[0] != "." && selector[0] != "#"){
        element = $('#' + selector);
    }
	$(document).ready(function(){
		element.after('<p class="error_content">* '+message+'</p>');
		$('.error_content').show(100).delay(5000).hide(100).queue(function(){
			$(this).remove();
		});
	});
}

/**
 * Validates required fields before submitting. Adds error messages for elements that is not valid.
 * @returns {boolean} returns true if the validation pass.
 */
function submit_validation(){
	var valid = true;
	if($('#template_title').val() == ''){
		valid = false;
		$('#template_title').addClass('select_error');
		error_message('template_title', 'Dette feltet kan ikke være tomt.')
	}
	if(get_latex_from_mathfield(Q_INPUT) == ''){
		valid = false;
		$(Q_INPUT).addClass('select_error');
		error_message('q_input_field', 'Dette feltet kan ikke være tomt.');
	}
	for(var step = 1; step <= STEP; step++){
		if(get_latex_from_mathfield('#s_input_mathquill_' + step) == ''){
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
		if(get_latex_from_mathfield('#a_input_mathquill_' + ans) == ''){
			valid = false;
			$('#a_input_mathquill_' + ans).addClass('select_error');
			error_message('answer_' + ans, 'Dette feltet kan ikke være tomt.');
		}
	}
	if(VARIABLE_COUNT > 0){ //TODO: improve validation of random-domain.
		for(var adv = 22; adv >= 0; adv--){
			if($('#o_adv_from_' + adv).length){
                if($('#o_adv_sequence_'+ adv).is(':checked')) {}
                else {
                    if ($('#o_adv_from_' + adv).val() == '') {
                        valid = false;
                        error_message('o_adv_from_' + adv, 'Fyll ut!');
                        $('#o_adv_domain').fadeIn();
                        $('#o_adv_caret').addClass('dropup');
                    }
                    else if ($('#o_adv_to_' + adv).val() == '') {
                        valid = false;
                        error_message('o_adv_to_' + adv, 'Fyll ut!');
                        $('#o_adv_domain').fadeIn();
                        $('#o_adv_caret').addClass('dropup');
                    }
                    else if ($('#o_adv_dec_' + adv).val() == '') {
                        valid = false;
                        error_message('o_adv_dec_' + adv, 'Fyll ut!');
                        $('#o_adv_domain').fadeIn();
                        $('#o_adv_caret').addClass('dropup');
                    }
                }
			}
		}
	}
	if ($('#opt_graph').is(':checked')) {
		if ($(".dcg-error").length > 0) {
			valid = false;
			error_message('opt_graph', 'Feil i graf! Se over og prøv på nytt!');
		}
	}
	return valid;
}

/**
 * Returns an array of the latex in every math-input in solution.
 * @returns {string|Array} latex - The array of LaTeX strings.
 */
function get_solution_latex(){
	var latex = [];
	for(var s = 1; s <= STEP; s++){
		latex.push(get_latex_from_mathfield('#s_input_mathquill_' + s));
	}
	return latex;
}

/**
 * Retrieve the LaTeX string for multiple choices.
 * @returns {string} returns all multiple choices as one string.
 */
function get_multiple_choices(latex_bool){
	var multiple_choices = [];
	if(!latex_bool){
		for(var m = 1; m <= MULTI_CHOICE; m++){
			if($('#m_checkbox_' + m).is(':checked')){
				multiple_choices.push('@?' + convert_variables(get_latex_from_mathfield('#m_input_mathquill_' + m)) + '?@');
			}
			else{
				multiple_choices.push(convert_variables(get_latex_from_mathfield('#m_input_mathquill_' + m)));
			}
		}
	}
	else{
		for(var ml = 1; ml <= MULTI_CHOICE; ml++){
			if($('#m_checkbox_' + ml).is(':checked')){
				multiple_choices.push('✓' + get_latex_from_mathfield('#m_input_mathquill_' + ml));
			}
			else{
				multiple_choices.push(get_latex_from_mathfield('#m_input_mathquill_' + ml));
			}
		}
	}
	return multiple_choices.join('§');
}

/**
 * Reset the input-field for conditions.
 */
function refresh_conditions(){
	var con_input = $('#con_dyn_input');
	$('#con_input_field').remove();
	con_input.append('<div id="con_input_field" class="input_field"><span id="n_input_mathquill" class="math-field form-control input_mathquill"></span></div>');
	redraw_mathquill_elements();
	if(MODIFY == true && mod_condition < 2){
		mod_condition++;
		var condition = $('#conditions').text();
		MathQuill.MathField($(N_INPUT)[0]).write(condition);
		refresh_char_colors('#n_input_mathquill');
	}
	MathQuill.MathField($(N_INPUT)[0]).focus();
}

/**
 * Refreshing the contents of fill-in-the-blanks. Retrieves all data from each step in the solution.
 */
function refresh_fill_in_content(){
	var f_dyn_fill = $('#f_dyn_fill_input');
	var fill_wrapper = $('.f_fill_content');
	fill_wrapper.remove();
	if(MODIFY && mod_blanks < 2 && $('#fill_in').text() != ""){
		mod_blanks++;
		var f_latex = $('#fill_in').text().split('§');
		for(var f = 1; f <= f_latex.length; f++){
			if(f > 1){
				f_dyn_fill.append('<hr class="f_fill_content">');
			}
			f_dyn_fill.append('<div id="f_fill_content_' + f + '" class="math-field form-control f_fill_content input_mathquill" style="border: 0; box-shadow: none">' + f_latex[f-1] + '</div>');
			MathQuill.MathField($('#f_fill_content_' + f)[0]);
		}
	}
	else{
		for (var fi = 1; fi <= STEP; fi++) {
			if (fi > 1) {
				f_dyn_fill.append('<hr class="f_fill_content">');
			}
			var fill_latex = MathQuill.MathField($('#s_input_mathquill_' + fi)[0]).latex();
			f_dyn_fill.append('<div id="f_fill_content_' + fi + '" class="math-field form-control f_fill_content input_mathquill" style="border: 0; box-shadow: none">' + fill_latex + '</div>');
			MathQuill.MathField($('#f_fill_content_' + fi)[0]);
		}
	}
	fill_wrapper.unbind('keypress');
	fill_wrapper.unbind('keydown');
	refresh_char_colors('.f_fill_content');
	$('#f_diff_latex').html("");
}

/**
 * Refresh and display the solution before the multiple-choices.
 */
function refresh_multiple_choice_template(){
	var latex = get_solution_latex();
	var wrapper = $('#m_dyn_solution');
	wrapper.children().remove();
	for(var i = 1; i <= STEP; i++){
		if(i > 1){
			wrapper.append('<hr>');
		}
		wrapper.append('<div class="input_field"><span id="m_sol_template_'+i+'" class="static-math input_mathquill"></span></div>');
		//$('#m_sol_template_' + i).mathquill().mathquill('latex', latex[i-1]);
		MathQuill.StaticMath($('#m_sol_template_' + i)[0]).latex(latex[i-1]);
	}
	wrapper.append('<br>');
}

/**
 * Refreshing multiple-choice contents. If in modify, get previous content.
 */
function refresh_multiple_choice(){
	if(MULTI_CHOICE == 0 && MODIFY == false) {
		MULTI_CHOICE++;
		$('#m_dyn_multi_input').append(
			'<div class="input_field">' +
				'<span id="m_input_mathquill_1" class="math-field form-control input_mathquill" style="max-width: 50%"></span>' +
			'</div>' +
			'<label for="m_checkbox_1">Forenkle:<input id="m_checkbox_1" type="checkbox"></label>');
		MathQuill.MathField($('#m_input_mathquill_1')[0]).revert();
		MathQuill.MathField($('#m_input_mathquill_1'));
	}
	else if(MULTI_CHOICE == 0 && MODIFY == true && mod_multiple < 2){
		mod_multiple++;
		var m_choice = $('#choices').text().split('§');
		$('#m_dyn_multi_input').append(
			'<div class="input_field">' +
				'<span id="m_input_mathquill_1" class="math-field form-control input_mathquill"></span>' +
			'</div>' +
			'<label for="m_checkbox_1">Forenkle:<input id="m_checkbox_1" type="checkbox"></label>');
		MathQuill.MathField($('#m_input_mathquill_1')[0]).revert();
		MathQuill.MathField($('#m_input_mathquill_1'));
		MULTI_CHOICE = m_choice.length;
		if(MULTI_CHOICE > 1){
			for(var m = 2; m <= MULTI_CHOICE; m++){
				$('#m_btn_del_' + (m-1)).hide();
				$('#m_dyn_multi_input').append(
					'<div id="m_field_'+m+'" class="input_field multi_field">' +
						'<span id="m_input_mathquill_'+m+'" class="math-field form-control input_mathquill"></span>' +
						'<a id="m_btn_del_'+m+'" class="glyphicon glyphicon-remove pull-right del_multi"></a>' +
					'</div>' +
					'<label for="m_checkbox_'+m+'">Forenkle:<input id="m_checkbox_'+m+'" type="checkbox"></label>'
				);
				redraw_mathquill_elements();
			}
		}
		for(var n = 1; n <= MULTI_CHOICE; n++){
			if(m_choice[(n-1)][0] == '✓'){
				$('#m_checkbox_' + n).prop('checked', true);
				m_choice[n-1] = m_choice[n-1].substring(1, m_choice[n-1].length);
			}
			MathQuill.MathField($('#m_input_mathquill_' + n)[0]).write(m_choice[(n-1)]);
		}
	}
}

/**
 * Adding/removing colors to used and unused variables, unknown characters and calculated references in all
 * mathquill input-fields.
 */
function refresh_all_char_colors(){
	refresh_char_colors(Q_INPUT);
	for(var step = 1; step <= STEP; step++){
		refresh_char_colors('#s_input_mathquill_' + step);
	}
	for(var ans = 1; ans <= ANSWER; ans++){
		refresh_char_colors('#a_input_mathquill_' + ans);
	}
	refresh_char_colors(C_INPUT);
	if($(N_INPUT).attr('id') != undefined){
		refresh_char_colors(N_INPUT);
	}
	for(var multi = 1; multi <= MULTI_CHOICE; multi++){
		refresh_char_colors('#m_input_mathquill_' + multi);
	}
	if($('#f_fill_content_1').attr('id') != undefined){
		for(var fill = 1; fill <= STEP; fill++){
			refresh_char_colors('#f_fill_content_' + fill);
		}
	}
}

/**
 * Adding/removing colors to used and unused variables, unknown characters and calculated references in given
 * mathquill input-field. Also adds variable buttons if a new variable is typed in the question.
 * @param {string|object} selector - Which input field to refresh.
 */
function refresh_char_colors(selector){
	var input_id = $(selector).attr('id');
	if(input_id != undefined) {
		input_id = input_id[0];
	}
	$(selector).find('var').each(function(){
		var f_var = $(this);
        if(f_var.hasClass('content_x') || $(this).html() == 'r'){} // "r" is reserved for the graph-editor.
        else if(f_var.hasClass('mq-operator-name')){ // Remove color if the the char is part of a LaTeX-command.
            f_var.removeClass('content_x');
            f_var.removeClass('content_var');
            f_var.removeClass('content_calc');
        }
		else{
			if(f_var.html() == 'x' || f_var.html() == 'y' || f_var.html() == 'z'){
				f_var.addClass('content_x');
			}
			else if(f_var.html().match(/^[a-z]*$/)){
				var var_exist = false;
				$('.btn_var_abc').each(function(){
					if($(this).html()[0] == f_var.html()){
						f_var.addClass('content_var');
						var_exist = true;
					}
				});
				if(!var_exist){
					f_var.removeClass('content_var');
				}
			}
			else if(f_var.html().match(/^[A-Z]*$/)){
				var calc_exist = false;
				$('.btn_calc').each(function(){
					if($(this).html() == f_var.html()){
						f_var.addClass('content_calc');
						calc_exist = true;
					}
				});
				if(!calc_exist){
					f_var.removeClass('content_calc');
				}
			}
		}
		update_variable_count();
	});
}

/**
 * Adds curly brackets to captial letters that have ^ in front of them. This is done to fix a bug.
 * @param {string|object} s - The string which gets the brackets added to it.
 * */
function add_curlybrackets(s){
	var capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
				       'Q', 'R', 'S', 'T', 'U', 'V', 'D', 'X', 'Y', 'Z'];
	var new_s = s;
	var count = 0;

	// Subtracts minus one from length, because math should never end with a ^.
	for(i = 0; i < s.length-1; i++) {
		if (s[i] == '^' && capital_letters.indexOf(s[i + 1]) != -1) {
			new_s =  new_s.substring(0, i+1) + '{' + new_s[i+1] + '}' + new_s.substring(i+2, new_s.length);
			count += 2;
		}
	}
	return new_s;
}

/**
 * Compare two latex strings, converting it to asciimath, and wrap parts of string that differs with a tag.
 * @returns {string|jQuery} - The asciimath string with blank tags.
 */
function get_diff_latex(){
	var dmp = new diff_match_patch();
	dmp.Diff_Timeout = 1;
	dmp.Diff_EditCost = 4;
	var latex_before = [];
	var latex_after = [];
	for (var la_orig = 1; la_orig <= STEP; la_orig++) {
		latex_before.push(get_latex_from_mathfield('#s_input_mathquill_' + la_orig));
		latex_before[la_orig-1] = add_curlybrackets(latex_before[la_orig-1]);
		latex_after.push(get_latex_from_mathfield('#f_fill_content_' + la_orig));
	}
	var d = dmp.diff_main(latex_before.join('§'), latex_after.join('§')); // Two strings to compare.
	var ds = dmp.diff_prettyHtml(d);
	$('#f_diff_latex').html("").append(ds);
	return $('#f_diff_latex').text();
}

/**
 * Before unload, ask user to confirm redirecting.
 */
$(window).bind('beforeunload', function(){
	if(TITLE_INSERTED && !SUBMITTING){
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
 * Refresh the dictionary of used variables. Adds or removes variables if needed/unneeded.
 */
function refresh_variables(){
	var id_check = {}; // Stores which variable-ids to check
	// Adding used variables to dictionary.
	$('.btn_var_abc_q').each(function(){
		var variable_id = parseInt($(this).attr('id').replace(/q_btn_abc_/, ''));
		var variable = $(this).text();
		id_check[variable_id] = variable;
		if(variable_id in VARIABLES){}
		else{
			if(Object.keys(VARIABLES).length <= MAX_VARIABLES) {
				VARIABLES[variable_id] = variable_id + '§' + variable.replace(/x/g, '');
			}
		}
	});
	// Removing unused variables from dictionary.
	for(var variable_id in VARIABLES){
		if(variable_id in id_check){}
		else{
			delete VARIABLES[variable_id];
		}
	}
}

/**
 * Retrieving data from selected task to be modified. Inserting data to all required fields, and prepares for editing.
 */
function insert_editable_data(){
	// Initialize valid variables
	var var_str = $('#used_variables').text();
	var_str = var_str.split(' ');
	for(var v = 0; v < var_str.length; v++){
		var tmp_var = var_str[v].split('§');
		VARIABLES[tmp_var[0]] = tmp_var.join('§');
        init_new_variable(tmp_var[1]);
	}
	//window.console.log(VARIABLES);

	// Inserting text-substitution
	var dictionary = $('#dictionary').text();
	dictionary = dictionary.split('§');
	if(dictionary.length == 1){
		if(dictionary[0] == ""){
			dictionary = [];
		}
	}
	if(dictionary.length != 0){
		for(var d_make = 2; d_make <= (dictionary.length / 2); d_make++){
			$('#e_btn_del_' + (d_make - 1)).hide();
			$('#e_form').append('<div id="e_sub_'+d_make+'" style="display:none"><hr><div class="form-group"><label class="col-md-4 control-label">Bytt ut ord/setning:</label><div class="col-md-7"><input id="e_from_'+d_make+'" type="text" class="form-control" placeholder="Epler"></div><div class="col-md-1"><a id="e_btn_del_'+d_make+'" class="glyphicon glyphicon-remove del_sub" style="float:right"></a></div></div><div class="form-group"><label class="col-md-4 control-label">Med ord/setning:</label><div class="col-md-7"><textarea id="e_to_'+d_make+'" type="text" class="form-control" rows="2" placeholder="Bananer, P&#xE6;rer, Appelsiner, Druer"></textarea></div></div></div>');
			$('#e_sub_' + d_make).fadeIn();
		}
		SUB = dictionary.length / 2;
		var d_from = 1;
		var d_to = 0;
		for(var d = 1; d <= (dictionary.length / 2); d++){
			$('#e_from_' + d).val(dictionary[d-d_from]);
			$('#e_to_' + d).val(dictionary[d+d_to]);
			d_from--;
			d_to++;
		}
	}

	// Inserting calculated references.
	var calc_str = $('#calculation_references').text();
	var calc_pop = $('#unchanged_ref').text();
	calc_str = calc_str.split('§');
	calc_pop = calc_pop.split('§');
	if(calc_str.length == 1){
		if(calc_str[0] == ""){
			calc_str = [];
		}
		if(calc_pop[0] == ""){
			calc_pop = [];
		}
	}
	if(calc_str.length != 0 && calc_pop.length != 0){
		for(var c = 0; c < calc_str.length; c++){
			dict_calc[calc_str[c]] = calc_str[c+1];
			dict_calc_unchanged[calc_pop[c]] = calc_pop[c+1];
			c++;
		}
	}
	if(calc_pop.length > 0){
		// Logic for adding the calculated-reference buttons with popovers.
		for(var c in dict_calc_unchanged){
			var c_char = "A";
			var c_index = parseInt(c);
			var c_latex = dict_calc_unchanged[c];
			c_char = String.fromCharCode(c_char.charCodeAt(0) + c_index);
			$('.btn_calc_dyn').append(
				'<div class="btn btn-success btn_calc btn_keypad btn_calc_ref btn_calc_ref_'+c_index+'">'+c_char+'' +
					'<a class="btn btn-success btn-xs btn_calc_del btn_calc_del_'+c_index+'"><span>x</span></a>' +
                    '<a class="btn btn-success btn-xs btn_calc_edit btn_calc_edit_' + c_index + '">' +
                        '<span class="glyphicon glyphicon-pencil"></span>' +
                    '</a>' +
				'</div>'
			);
			$('.btn_calc_dyn_ref').append(
				'<button class="btn btn-success btn_calc btn_keypad btn_calc_ref_'+c_index+'">'+c_char+'</button>'
			);
			$('.btn_calc_ref_' + c_index).popover({
				html: true,
				content: '<img src="http://latex.codecogs.com/svg.latex?'+c_latex+'" border="0"/>',
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
		}
	}

	// Refreshing colors and adding required variable-buttons to the question.
	//refresh_char_colors('#q_input_mathquill');
	update_variable_count();

	// Insert solution
	var edit_solution = $('#solution').text();
	edit_solution = edit_solution.split('§');
	write_to_mathfield('#s_input_mathquill_1', edit_solution[0]);
	if(edit_solution.length > 1){
		for(var index_s = 2; index_s <= edit_solution.length; index_s++){
			$('#s_btn_del_' + STEP).hide();
			STEP = index_s;
			$('#s_form').append('<div id="step_' + STEP + '" class="step" style="display: none"><hr>' +
				'<h4>Steg ' + STEP + '<a id="s_btn_del_'+STEP+'" class="glyphicon glyphicon-remove del_step" style="float:right"></a></h4>' +
				'<div class="input_field s_input_field"><span id="s_input_mathquill_'+STEP+'" class="math-field form-control input_mathquill">'+ edit_solution[index_s - 1] +'</span>' +
				'<button id="s_btn_clear_'+STEP+'" class="btn btn-default btn_clear" style="margin-left: 3px; border: none">' +
				'<span class="glyphicon glyphicon-trash" style="resize: vertical"></span></button></div>');
			MathQuill.MathField($('#s_input_mathquill_' + STEP)[0]);
			$('#step_' + STEP).show();
		}
	}

	// Insert answer
	var edit_answer = $('#answer').text();
	edit_answer = edit_answer.split('§');
	write_to_mathfield('#a_input_mathquill_1', edit_answer[0]);
	if(edit_answer.length > 1){
		for(var index_a = 2; index_a <= edit_answer.length; index_a++){
			$('#a_btn_del_' + ANSWER).hide();
			ANSWER = index_a;
			$('#ans_title_1').show();
			$('#a_form').append('<div id="answer_'+ANSWER+'" class="answer" style="display: none"><hr>' +
				'<h4>Svar '+ANSWER+'<a id="a_btn_del_'+ANSWER+'" class="glyphicon glyphicon-remove del_answer" style="float:right"></a></h4>' +
				'<div class="input_field a_input_field"><span id="a_input_mathquill_'+ANSWER+'" class="math-field form-control input_mathquill">'+ edit_answer[index_a - 1] +'</span></div>');
			MathQuill.MathField($('#a_input_mathquill_' + ANSWER)[0]);
			$('#answer_' + ANSWER).show();
		}
	}

	refresh_char_colors('.input_mathquill');

    // Insert random-domain
    var random_domain = $('#random_domain').text();
    if((random_domain != "") && (random_domain != "None")){
        random_domain = JSON.parse(random_domain);
        var init_domain = 0;
        for(var key in random_domain){
            var id = key.replace(/R/g, "");
            if(random_domain[key][1]){
                for (var s = 0; s < random_domain[key][0].length; s++) {
                    $('#o_adv_sequence_container_'+ id).prepend('<span class="o_seq"><span class="math-field static-math-sm">' + random_domain[key][0][s] + '</span><a class="btn btn_tag_del">x</a></span>').fadeIn();
                    $('#o_adv_' + id).children().nextAll().slice(0, 3).each(function () {
                        $(this).fadeOut();
                    });
					$('#o_adv_sequence_'+id).attr('checked', true);
                }
            } else {
                var domain_list = random_domain[key][0];
                $('#o_adv_from_'+id).val(domain_list[0]);
                $('#o_adv_to_'+id).val(domain_list[1]);
                $('#o_adv_dec_'+id).val(domain_list[2]);
                if(init_domain == 0){
                    init_domain++;
                    $('#opt_domain_from').val(domain_list[0]);
                    $('#opt_domain_to').val(domain_list[1]);
                    $('#opt_domain_dec').val(domain_list[2]);
                }
            }
        }
    }

	// Set checked on graph
	var graph_expressions = $('#get_graph').text();
	if((graph_expressions != "[]") && (graph_expressions != "None") && (graph_expressions != "")){
		$('#opt_graph').prop('checked', true);
	}

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

	// Get and insert disallowed symbols/expressions
	var disallowed = $('#get_disallowed').text();
	if(disallowed != ""){
		disallowed = JSON.parse(disallowed);
		if (disallowed[0] != "") {
			for (var d = 0; d < disallowed.length; d++) {
				$('#tags_illegal').prepend('<span class="tag_i"><span class="math-field static-math-sm">' + disallowed[d] + '</span><a class="btn btn_tag_del">x</a></span>');
			}
		}
	}

	// Get and insert required symbols/expressions
	var required = $('#get_required').text();
	if(required != ""){
		required = JSON.parse(required);
		if (required[0] != "") {
			for (var r = 0; r < required.length; r++) {
				$('#tags_required').prepend('<span class="tag_r"><span class="math-field static-math-sm">' + required[r] + '</span><a class="btn btn_tag_del">x</a></span>');
			}
		}
	}

	// Get and insert tags
	var tags = JSON.parse($('#get_tags').text());
	if(tags[0] != ""){
		for(var t = 0; t < tags.length; t++){
			$('#tags').prepend('<span class="tag">'+tags[t]+'<a class="btn btn_tag_del">x</a></span>');
		}
	}
	VAR_INIT = false;
	redraw_mathquill_elements();
}

/**
 * Posts a form to the server
 * submits a form to the given path with a form of the given parameters.
 * @param {string} path - the path form gets posted to.
 * @param {dictionary} params - a dictionary that is the form that gets posted.
 * @param {string} method - sets the method for the submission. Uses post by default.
 */
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

/**
 *Gets a cookie and returns its value
 * @param {string} name - the name of the cookie to get.
 * @returns {string} - Returns the value of the cookie specified.
 */
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

/**
 * Converts user-conditions to actual conditions sympy can compute.
 * @param {string} expression - The LaTeX string of the conditions to be parsed.
 * @returns {string} the parsed expression.
 */
function parse_conditions(expression) {
	expression = expression.replace('/\\ne/g', '!=');
	for(var i = 0; i < expression.length; i++) {
		// Makes = into ==
		if(expression[i] == '=') {
			if (expression[i - 1] != '=' && expression[i - 1] != '=' && expression[i - 1] != '!') {
				expression = expression.substring(0, i) + '=' + expression.substring(i, expression.length);
			}
		}
	}
	return expression
}