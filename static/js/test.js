$(document).ready(function() {
	// Question variables
	var max_fields      		= 20; //maximum input boxes allowed
	var wrapper         		= $(".input_fields_test"); //Input field wrapper - question
	var wrapper_solution		= $(".input_field_solution"); // Input field wrapper - solution
	var wrapper_sol_btn			= $(".input_field_sol_btn"); // Field for btn - solution
	var add_button_text   		= $(".add_field_button_text"); //Add button ID
	var add_button_var			= $(".add_field_button_var");
	var add_button_equal		= $(".add_field_button_equal");
	var add_button_addition 	= $(".add_field_button_addition");
	var add_button_subtraction	= $(".add_field_button_subtraction");
	var add_button_x			= $(".add_field_button_x");
	var add_button_integral		= $(".add_field_button_integral");
	var q_btn_parleft			= $("#btn_q_parenthesis_l");
	var q_btn_parright			= $("#btn_q_parenthesis_r");
	var clean_button			= $(".button_clean_mal");
	var remove_last_content		= $(".button_remove_last_content");
	var fetch_input_q			= $(".input_text_fetch_q");
	var toggle_solution			= $(".continue_to_solution");
	var variable				= "a";
	var variable_s				= "a";
	var variable_sol			= "a";
	var R						= 0;
	var input_text_count		= 0;
	var content_count			= 0;
	var x 						= 1; //initial text box count
	
	// Solution variables
	var max_fields_so			= 20; //maximum input in solution panels
	var sol_btn_x				= $("#btn_sol_x");
	var sol_btn_eq				= $("#btn_sol_eq");
	var sol_btn_parleft			= $("#btn_sol_parenthesis_l");
	var sol_btn_parright		= $("#btn_sol_parenthesis_r");
	var sol_btn_addition		= $("#btn_sol_addition");
	var sol_btn_subtraction		= $("#btn_sol_subtraction");
	var sol_btn_division		= $("#btn_sol_division");
	var sol_btn_delete			= $("#btn_sol_delete");
	var y						= 0; // amount of elemens in solution box
	var sol_step				= 1;
	
	// Answer variables
	var max_fields_ans			= 10; //maximum input in answer panel
	var wrapper_ans_btn			= $(".input_field_ans_btn");
	var wrapper_answer			= $(".input_field_answer");
	var toggle_answer			= $(".continue_to_answer");
	var ans_btn_x				= $("#btn_ans_x");
	var ans_btn_parleft			= $("#btn_ans_parenthesis_l");
	var ans_btn_parright		= $("#btn_ans_parenthesis_r");
	var ans_btn_addition		= $("#btn_ans_addition");
	var ans_btn_subtraction		= $("#btn_ans_subtraction");
	var ans_btn_division		= $("#btn_ans_division");
	var ans_btn_delete			= $("#btn_ans_delete");
	var variable_ans			= "a";
	var z						= 0; //amount of elements in answer box
	
	// Option variables
	var toggle_option			= $("#btn_ans_continue");
	var array_submit_temp		= [];
	var array_submit			= {};
	
	// Calculation variables
	var max_fields_calc			= 10;
	var wrapper_solve_btn		= $(".input_field_solve_btn");
	var wrapper_calc			= $(".input_field_solve");
	var calc_btn_x				= $("#btn_solve_x");
	var calc_btn_parleft		= $("#btn_solve_parenthesis_l");
	var calc_btn_parright		= $("#btn_solve_parenthesis_r");
	var calc_btn_addition		= $("#btn_solve_addition");
	var calc_btn_subtraction	= $("#btn_solve_subtraction");
	var calc_btn_division		= $("#btn_solve_division");
	var calc_btn_delete			= $("#btn_solve_delete");
	var calc_btn_save			= $("#btn_solve_save");
	var variable_calc			= "a";
	var variable_solve			= "A";
	var variable_solve_ref		= "@";
	var w						= 0;
	var solve_count				= 0;
	var array_solve_ref			= []; // Store the reference for solve-buttons
	var array_solve_line		= [];
	
	/*
	======= QUESTION PANEL ========
	*/
	
	// Insert text
	$(fetch_input_q).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			var input_text = $("#mal-input-text").val();
			if(input_text != ""){
				x++; //text box increment
				$(wrapper).append('<span class="input_content_text input_content'+content_count+' input_content_q"> '+input_text+' </span>');
				content_count = content_count + 1;
			}
			$("#mal-input-text").val("");
		}
	});
	
	// Cancel text-input
	$($(".add_field_button_text_cancel")).click(function(e){
		e.preventDefault();
		$("#mal-input-text").val("");
	});
	
	// Insert a variable
	$(add_button_var).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			$(wrapper).append('<span id="R'+R+'" class="input_content_var input_content'+content_count+' input_content_q">'+variable+'</span>');
			variable = String.fromCharCode(variable.charCodeAt(0) + 1);
			R = R + 1;
			content_count = content_count + 1;
		}
	});
	
	// Insert unknown X
	$(add_button_x).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_x input_content'+content_count+' input_content_q">x </span>');
			content_count = content_count + 1;
		}
	});
	
	// Insert equal sign (only once)
	$(add_button_equal).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_eq input_content'+content_count+' input_content_q"> = </span>');
			$(add_button_equal).prop('disabled', true);
			content_count = content_count + 1;
		}
	});
	
	// Insert left parenthesis
	$(q_btn_parleft).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_op input_content_q">(</span>');
			content_count = content_count + 1;
		}
	});
	
	// Insert right parenthesis
	$(q_btn_parright).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_op input_content_q">)</span>');
			content_count = content_count + 1;
		}
	});
	
	// Insert addition operator
	$(add_button_addition).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_op input_content'+content_count+' input_content_q"> + </span>');
			content_count = content_count + 1;
		}
	});
	
	// Insert subtraction operator
	$(add_button_subtraction).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_op input_content'+content_count+' input_content_q"> - </span>');
			content_count = content_count + 1;
		}
	});
	
	// Insert integral sign
	$(add_button_integral).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_op input_content'+content_count+' input_content_q"> &#x222B; </span>');
			content_count = content_count + 1;
		}
	});
	
	// Reset the input field
	$(clean_button).click(function(e){
		e.preventDefault();
		$("#mal_input_field").html("");
		variable = "a";
		R = 0;
		content_count = 0;
		x = 1;
		input_text_count = 0;
		$(add_button_equal).prop('disabled', false);
	});
	
	// Delete the last input component
	$(remove_last_content).click(function(e){
		e.preventDefault();
		// if last content is a variable
		if($("#mal_input_field span:last").is(".input_content_var")){
			$("#mal_input_field span:last-child").remove();
			if(variable != "a"){
				variable = String.fromCharCode(variable.charCodeAt(0) - 1);
				R--;
			}
		}
		// if last content is an unknown x
		else if($("#mal_input_field span:last").is(".input_content_x")){
			$("#mal_input_field span:last-child").remove();
		}
		// if last content is a text-box
		else if($("#mal_input_field span:last").is(".input_content_text")){
			$("#mal_input_field span:last-child").remove();
		}
		// if last content is an equal sign
		else if($("#mal_input_field span:last").is(".input_content_eq")){
			$("#mal_input_field span:last-child").remove();
			$(add_button_equal).prop('disabled', false);
		}
		// if last content is an operator
		else if($("#mal_input_field span:last").is(".input_content_op")){
			$("#mal_input_field span:last-child").remove();
		}
		if(content_count > 0){
			x--;
			content_count--;
		}
	});
	
	// Proceed to solution panel
	$(toggle_solution).click(function(e){
		e.preventDefault();
		RS = 0;
		var number_of_vars = $('.input_content_var').length;
		if(number_of_vars != 0){
			for(i=0; i<number_of_vars; i++){
				$(wrapper_sol_btn).append('<button id="btn_sol_R'+RS+'" class="btn btn-danger btn_sol_var btn-group-s">'+variable_s+'</button>');
				$(wrapper_ans_btn).append('<button id="btn_ans_R'+RS+'" class="btn btn-danger btn_ans_var btn-group-a">'+variable_s+'</button>');
				$(wrapper_solve_btn).append('<button id="btn_calc_R'+RS+'" class="btn btn-danger btn_solve_var">'+variable_s+'</button>');
				variable_s = String.fromCharCode(variable_s.charCodeAt(0) + 1);
				RS++;
			}
		}
		$(wrapper_solution).append('<div id="container_sol'+sol_step+'" class="page-header"><form class="form-group"><h4>Steg #'+sol_step+'</h4><div class="input_fields_wrap"><input id="sol_val_input_'+sol_step+'" type="text" class="form-control" name="solutiontext[]" placeholder="Forklaring..."><div class="input_field_sol_'+sol_step+'"></div></div></form></div>');
		$(".btn-group-q").prop('disabled', true);
		$("#sol_panel").fadeToggle();
	});
	
	/*
	======= SOLUTION PANEL ========
	*/
	
	// Close solution panel
	$("#solution_panel_btn_cancel").click(function(e){
		e.preventDefault();
		// Close sub-panels
		$("#opt_range_from").val("");
		$("#opt_range_to").val("");
		$("#opt_decimal").val("");
		$("#opt_allow").prop("checked", false);
		$(".btn-group-a").prop('disabled', false);
		$("#opt_panel").fadeOut();
		$(wrapper_answer).html("");
		$(".btn-group-s").prop('disabled', false);
		$("#ans_panel").fadeOut();
		z = 0;
		// Close solution panel
		$("#dyn_sol_btn").html("");
		$("#dyn_ans_btn").html("");
		$("#dyn_solve_btn").html("");
		$("#dyn_sol_btn_solve .calc_btns").not('button:first').remove(); // remove A,B,C,...
		$(wrapper_solution).html("");
		$('#dyn_ans_btn_solve').html("");
		sol_step = 1;
		variable_s = "a";
		variable_solve = "A";
		solve_count	= 0;
		RS = 0;
		$(".btn-group-q").prop('disabled', false);
		$("#sol_panel").fadeOut();
		y = 0;
		array_solve_ref = [];
		array_solve_line = [];
	});
	
	// Add new step
	$("#btn_sol_new_step").click(function(e){
		e.preventDefault();
		$("#mal_input_field_solution a:last").hide();
		$(".input_field_sol_"+sol_step).append('<span class="input_content_s sol_new_line"></span>');
		sol_step++;
		$(wrapper_solution).append('<div id="container_sol'+sol_step+'"class="page-header"><form class="form-group"><a class="glyphicon glyphicon-remove btn_sol_del_step" style="float:right"></a><h4>Steg #'+sol_step+'</h4><div class="input_fields_wrap"><input id="sol_val_input_'+sol_step+'" type="text" class="form-control" name="solutiontext[]" placeholder="Forklaring..."><div class="input_field_sol_'+sol_step+'"></div></div></form></div>');
		y = 0;
	});
	
	// Delete last step
	$(document).on('click', '#mal_input_field_solution .btn_sol_del_step', function(e){ 
		e.preventDefault();
		$("#container_sol"+sol_step).remove();
		$("#mal_input_field_solution a:last").show();
		sol_step--;
		y = $('.sol_input_'+sol_step).length
	});
	
	// Clear all fields, reset
	$("#btn_sol_clear_all").click(function(e){
		e.preventDefault();
		sol_step = 1;
		$(wrapper_solution).html("");
		$(wrapper_solution).append('<div class="page-header"><form class="form-group"><h4>Steg #'+sol_step+'</h4><div class="input_fields_wrap"><input type="text" class="form-control" name="solutiontext[]" placeholder="Forklaring..."><div class="input_field_sol_'+sol_step+'"></div></div></form></div>');
		y = 0;
	});
	
	// Insert unknown X
	$(sol_btn_x).click(function(e){
		e.preventDefault();
		if(y < max_fields_so){
			y++;
			$(".input_field_sol_"+sol_step).append('<span class="input_content_x sol_input_'+sol_step+' input_content_s">x </span>');
		}
	});
	
	// Insert variable a,b,c,..
	$(document).on('click', '#dyn_sol_btn .btn_sol_var', function(e){
		e.preventDefault();
		if(y < max_fields_so) {
			y++;
			var id = parseInt($(this).attr("id").match(/[\d]+$/)); // Retrieve the variable-number at end of id.
			variable_sol = String.fromCharCode(variable_sol.charCodeAt(0) + id);
			$(".input_field_sol_"+sol_step).append('<span id="R'+id+'" class="input_content_var sol_input_'+sol_step+' input_content_s">'+variable_sol+'</span>');
			variable_sol = "a";
		}
	});
	
	// Insert solved A,B,C,..
	$(document).on('click', '#dyn_sol_btn_solve .btn_sol_solve_ref', function(e){
		e.preventDefault();
		if(y < max_fields_so){
			y++;
			var id = parseInt($(this).attr("id").match(/[\d]+$/));
			variable_solve_ref = String.fromCharCode(variable_solve_ref.charCodeAt(0) + id);
			s_id = id - 1;
			$(".input_field_sol_"+sol_step).append('<span id="solve_content_'+s_id+'" class="input_content_calc input_content_s">'+variable_solve_ref+'</span>');
			variable_solve_ref = "@";
		}
	});
	
	// Insert equal sign
	$(sol_btn_eq).click(function(e){
		e.preventDefault();
		if(y < max_fields_so){
			y++;
			$(".input_field_sol_"+sol_step).append('<span class="input_content_eq sol_input_'+sol_step+' input_content_s"> = </span>');
		}
	});
	
	// Insert left parenthesis
	$(sol_btn_parleft).click(function(e){
		e.preventDefault();
		if(y < max_fields_so){
			y++;
			$(".input_field_sol_"+sol_step).append('<span class="input_content_op sol_input_'+sol_step+' input_content_s">(</span>');
		}
	});
	
	// Insert right parenthesis
	$(sol_btn_parright).click(function(e){
		e.preventDefault();
		if(y < max_fields_so){
			y++;
			$(".input_field_sol_"+sol_step).append('<span class="input_content_op sol_input_'+sol_step+' input_content_s">)</span>');
		}
	});
	
	// Insert addition operator
	$(sol_btn_addition).click(function(e){
		e.preventDefault();
		if(y < max_fields_so){
			y++;
			$(".input_field_sol_"+sol_step).append('<span class="input_content_op sol_input_'+sol_step+' input_content_s"> + </span>');
		}
	});
	
	// Insert subtraction operator
	$(sol_btn_subtraction).click(function(e){
		e.preventDefault();
		if(y < max_fields_so){
			y++;
			$(".input_field_sol_"+sol_step).append('<span class="input_content_op sol_input_'+sol_step+' input_content_s"> - </span>');
		}
	});
	
	// Insert division operator
	$(sol_btn_division).click(function(e){
		e.preventDefault();
		if(y < max_fields_so){
			y++;
			$(".input_field_sol_"+sol_step).append('<span class="input_content_op sol_input_'+sol_step+' input_content_s"> / </span>');
		}
	});
	
	// Delete last input component for current step
	$(sol_btn_delete).click(function(e){
		e.preventDefault();
		// if last conent is a variable
		if($("#container_sol"+sol_step+" span:last").is(".input_content_var")){
			$("#container_sol"+sol_step+" span:last").remove();
			if(variable_sol != "a"){
				variable_sol = String.fromCharCode(variable_sol.charCodeAt(0) - 1);
			}
		}
		// if last content is an unknown x
		else if($("#container_sol"+sol_step+" span:last").is(".input_content_x")){
			$("#container_sol"+sol_step+" span:last").remove();
		}
		// if last content is an equal sign
		else if($("#container_sol"+sol_step+" span:last").is(".input_content_eq")){
			$("#container_sol"+sol_step+" span:last").remove();
		}
		// if last content is an operator
		else if($("#container_sol"+sol_step+" span:last").is(".input_content_op")){
			$("#container_sol"+sol_step+" span:last").remove();
		}
		// if last content is an solved reference
		else if($("#container_sol"+sol_step+" span:last").is(".input_content_calc")){
			$("#container_sol"+sol_step+" span:last").remove();
		}
		if(y > 0){
			y--;
		}
	});
	
	// Proceed to answer panel
	$(toggle_answer).click(function(e){
		e.preventDefault();
		$(".btn-group-s").prop('disabled', true);
		$("#ans_panel").fadeToggle();
	});
	
	/*
	======= ANSWER PANEL ========
	*/
	
	// Close answer panel
	$("#ans_panel_btn_cancel").click(function(e){
		e.preventDefault();
		// Close sub-panels
		$("#opt_range_from").val("");
		$("#opt_range_to").val("");
		$("#opt_decimal").val("");
		$("#opt_allow").prop("checked", false);
		$(".btn-group-a").prop('disabled', false);
		$("#opt_panel").fadeOut();
		// Close answer panel
		$(wrapper_answer).html("");
		$(".btn-group-s").prop('disabled', false);
		$("#ans_panel").fadeOut();
		z = 0;
	});
	
	// Insert variable a,b,c,..
	$(document).on('click', '#dyn_ans_btn .btn_ans_var', function(e){
		e.preventDefault();
		if(z < max_fields_ans){
			z++;
			var id = parseInt($(this).attr("id").match(/[\d]+$/)); // Retrieve the variable-number at end of id.
			variable_ans = String.fromCharCode(variable_ans.charCodeAt(0) + id);
			$(wrapper_answer).append('<span id="R'+id+'" class="input_content_var input_content_a">'+variable_ans+'</span>');
			variable_ans = "a";
		}
	});
	
	// Insert solved A,B,C,..
	$(document).on('click', '#dyn_ans_btn_solve .btn_ans_solve_ref', function(e){
		e.preventDefault();
		if(z < max_fields_ans){
			z++;
			var id = parseInt($(this).attr("id").match(/[\d]+$/));
			variable_solve_ref = String.fromCharCode(variable_solve_ref.charCodeAt(0) + id);
			s_id = id - 1;
			$('.input_field_answer').append('<span id="solve_content_'+s_id+'" class="input_content_calc input_content_a">'+variable_solve_ref+'</span>');
			variable_solve_ref = "@";
		}
	});
	
	// Insert unknown x
	$(ans_btn_x).click(function(e){
		e.preventDefault();
		if(z < max_fields_ans){
			z++;
			$(wrapper_answer).append('<span class="input_content_x input_content_a">x </span>');
		}
	});
	
	// Insert left parenthesis
	$(ans_btn_parleft).click(function(e){
		e.preventDefault();
		if(z < max_fields_ans){
			z++;
			$(wrapper_answer).append('<span class="input_content_op input_content_a">(</span>');
		}
	});
	
	// Insert right parenthesis
	$(ans_btn_parright).click(function(e){
		e.preventDefault();
		if(z < max_fields_ans){
			z++;
			$(wrapper_answer).append('<span class="input_content_op input_content_a">)</span>');
		}
	});
	
	// Insert addition operator
	$(ans_btn_addition).click(function(e){
		e.preventDefault();
		if(z < max_fields_ans){
			z++;
			$(wrapper_answer).append('<span class="input_content_op input_content_a"> + </span>');
		}
	});
	
	// Insert subtraction operator
	$(ans_btn_subtraction).click(function(e){
		e.preventDefault();
		if(z < max_fields_ans){
			z++;
			$(wrapper_answer).append('<span class="input_content_op input_content_a"> - </span>');
		}
	});
	
	// Insert division operator
	$(ans_btn_division).click(function(e){
		e.preventDefault();
		if(z < max_fields_ans){
			z++;
			$(wrapper_answer).append('<span class="input_content_op input_content_a"> / </span>');
		}
	});
	
	// Clear input field, reset
	$("#btn_ans_clear_all").click(function(e){
		e.preventDefault();
		$(wrapper_answer).html("");
		z = 0;
	});
	
	// Delete last input component
	$(ans_btn_delete).click(function(e){
		e.preventDefault();
		// if last conent is a variable
		if($("#mal_input_field_answer span:last").is(".input_content_var")){
			$("#mal_input_field_answer span:last").remove();
			if(variable_sol != "a"){
				variable_sol = String.fromCharCode(variable_sol.charCodeAt(0) - 1);
			}
		}
		// if last content is an unknown x
		else if($("#mal_input_field_answer span:last").is(".input_content_x")){
			$("#mal_input_field_answer span:last").remove();
		}
		// if last content is an operator
		else if($("#mal_input_field_answer span:last").is(".input_content_op")){
			$("#mal_input_field_answer span:last").remove();
		}
		// if last content is an solved reference
		else if($("#mal_input_field_answer span:last").is(".input_content_calc")){
			$("#mal_input_field_answer span:last").remove();
		}
		if(z > 0){
			z--;
		}
	});
	
	// Proceed to option panel
	$(toggle_option).click(function(e){
		e.preventDefault();
		$(".btn-group-a").prop('disabled', true);
		$("#opt_panel").fadeToggle();
	});
	
	/*
	======= OPTION PANEL ========
	*/
	
	// Close option panel
	$("#opt_panel_btn_cancel").click(function(e){
		e.preventDefault();
		$("#opt_range_from").val("");
		$("#opt_range_to").val("");
		$("#opt_decimal").val("");
		$("#opt_allow").prop("checked", false);
		$(".btn-group-a").prop('disabled', false);
		$("#opt_panel").fadeOut();
	});
	
	// Retrieve all values and save to database
	var array_submit_q = [];
	var array_submit_s = [];
	var array_submit_a = [];
	var array_submit_o = [];
	var tmp_sol_step = 1;
	var get_string_s = true;
	$('#btn_opt_save').click(function(e){
		e.preventDefault();
		array_submit = [];
		// Retrieve values in question field
		$(".input_content_q").each(function(index){
			var var_q = "";
			if($(this).hasClass('input_content_var')){
				var_q = $(this).attr('id');
			}
			else if($(this).hasClass('input_content_x')){
				if($(this).prev().hasClass('input_content_var')){
					var_q = "*x";
				}
				else if($(this).prev().hasClass('input_content_calc')){
					var_q = "*x";
				}
				else{
					var_q = "x";
				}
			}
			else{
				var_q = $(this).text();
			}
			array_submit_q.push(var_q);
		});
		// Retrieve values in solution field
		$(".input_content_s").each(function(index){
			var var_s = "";
			if(get_string_s == true){
				array_submit_s.push($("#sol_val_input_"+tmp_sol_step).val());
				get_string_s = false;
				tmp_sol_step++;
			}
			if($(this).hasClass('input_content_var')){
				var_s = $(this).attr('id');
			}
			else if($(this).hasClass('input_content_x')){
				if($(this).prev().hasClass('input_content_var')){
					var_s = "*x";
				}
				else if($(this).prev().hasClass('input_content_calc')){
					var_s = "*x";
				}
				else{
					var_s = "x";
				}
			}
			else if($(this).hasClass('input_content_calc')){
				var id = parseInt($(this).attr("id").match(/[\d]+$/));
				var_s = "{"+array_solve_line[id]+"}";
			}
			else if($(this).hasClass('sol_new_line')){
				var_s = "\n";
				get_string_s = true;
			}
			else{
				var_s = $(this).text();
			}
			array_submit_s.push(var_s);
		});
		// Retrieve values in answer field
		$(".input_content_a").each(function(index){
			var var_a = "";
			if($(this).hasClass('.input_content_var')){
				var_a = $(this).attr('id');
			}
			else if($(this).hasClass('input_content_x')){
				if($(this).prev().hasClass('input_content_var')){
					var_a = "*x";
				}
				else if($(this).prev().hasClass('input_content_calc')){
					var_a = "*x";
				}
				else{
					var_a = "x";
				}
			}
			else if($(this).hasClass('input_content_calc')){
				var id = parseInt($(this).attr("id").match(/[\d]+$/));
				var_a = "{"+array_solve_line[id]+"}";
			}
			else{
				var_a = $(this).text();
			}
			array_submit_a.push(var_a);
		});
		// Retrieve values in option panel
		var r_f = $('#opt_range_from').val();
		var r_t = $('#opt_range_to').val();
		array_submit_o.push(r_f + " " + r_t);
		array_submit_o.push($('#opt_decimal').val());
		var opt_allow = "";
		if($('#opt_allow').is(':checked')){
			opt_allow = "true";
		}
		else {
			opt_allow = "false";
		}
		array_submit_o.push(opt_allow);
		var var_q_final = array_submit_q.join("");
		var var_s_final = array_submit_s.join("");
		var var_a_final = array_submit_a.join("");
		// Store in dictionary
		array_submit["question"] 	= var_q_final;
		array_submit["solution"] 	= var_s_final;
		array_submit["answer"] 		= var_a_final;
		array_submit["range"]		= array_submit_o[0];
		array_submit["decimals"]	= array_submit_o[1];
		array_submit["allow_zero"]	= array_submit_o[2];
		array_submit["topic"] 		= "7";
		// Reset temp lists
		tmp_sol_step = 1;
		get_string_s = true;
		array_submit_q = [];
		array_submit_s = [];
		array_submit_a = [];
		array_submit_o = [];

		// Output testing
		var s_output = [];
		for(var s_u in array_submit){
			s_output.push(s_u+":\n"+array_submit[s_u]);
		}
		var u_output = s_output.join("\n");
		alert(u_output);

		alert(array_submit.join("\n"));
		post(/test/, array_submit)
	});
	
	/*
	======= CALCULATION PANEL ========
	*/
	
	// Insert variable a,b,c,..
	$(document).on('click', '#dyn_solve_btn .btn_solve_var', function(e){
		e.preventDefault();
		if(w < max_fields_calc){
			w++;
			var id = parseInt($(this).attr("id").match(/[\d]+$/)); // Retrieve the variable-number at end of id.
			variable_calc = String.fromCharCode(variable_calc.charCodeAt(0) + id);
			$(wrapper_calc).append('<span id="R'+id+'" class="input_content_var solve_content">'+variable_calc+'</span>');
			variable_calc = "a";
		}
	});
	
	// Insert unknown x
	$(calc_btn_x).click(function(e){
		e.preventDefault();
		if(w < max_fields_calc){
			w++;
			$(wrapper_calc).append('<span class="input_content_x solve_content">x </span>');
		}
	});
	
	// Insert left parenthesis
	$(calc_btn_parleft).click(function(e){
		e.preventDefault();
		if(w < max_fields_calc){
			w++;
			$(wrapper_calc).append('<span class="input_content_op solve_content">(</span>');
		}
	});
	
	// Insert right parenthesis
	$(calc_btn_parright).click(function(e){
		e.preventDefault();
		if(w < max_fields_calc){
			w++;
			$(wrapper_calc).append('<span class="input_content_op solve_content">)</span>');
		}
	});
	
	// Insert addition operator
	$(calc_btn_addition).click(function(e){
		e.preventDefault();
		if(w < max_fields_calc){
			w++;
			$(wrapper_calc).append('<span class="input_content_op solve_content"> + </span>');
		}
	});
	
	// Insert subtraction operator
	$(calc_btn_subtraction).click(function(e){
		e.preventDefault();
		if(w < max_fields_calc){
			w++;
			$(wrapper_calc).append('<span class="input_content_op solve_content"> - </span>');
		}
	});
	
	// Insert division operator
	$(calc_btn_division).click(function(e){
		e.preventDefault();
		if(w < max_fields_calc){
			w++;
			$(wrapper_calc).append('<span class="input_content_op solve_content"> / </span>');
		}
	});
	
	// Delete last input component
	$(calc_btn_delete).click(function(e){
		e.preventDefault();
		// if last content is a variable
		if($("#mal_input_field_solve span:last").is(".input_content_var")){
			$("#mal_input_field_solve span:last").remove();
			if(variable_calc != "a"){
				variable_calc = String.fromCharCode(variable_calc.charCodeAt(0) - 1);
			}
		}
		// if last content is an unknown x
		else if($("#mal_input_field_solve span:last").is(".input_content_x")){
			$("#mal_input_field_solve span:last").remove();
		}
		// if last content is an operator
		else if($("#mal_input_field_solve span:last").is(".input_content_op")){
			$("#mal_input_field_solve span:last").remove();
		}
		if(w > 0){
			w--;
		}
	});
	
	// Retrieve and insert calculation to solution
	$(calc_btn_save).click(function(e){
		e.preventDefault();
		var total_solve_contents = $('.solve_content').length;
		if(total_solve_contents != 0){
			var input_array_solve = [];
			var input_array_solve_tmp = [];
			var input_temp_val = "";
			$(".solve_content").each(function(index){
				if($(this).hasClass('input_content_var')){
					input_temp_val = $(this).attr('id');
				}
				else if($(this).hasClass('input_content_x')){
					input_temp_val = "*x";
				}
				else{
					input_temp_val = $(this).text();
				}
				var calc_var = $(this).get(0).outerHTML //text();
				input_array_solve.push(calc_var);
				input_array_solve_tmp.push(input_temp_val);
			});
			var solve_popover = input_array_solve.join("");
			var input_tmp_join = input_array_solve_tmp.join("");
			array_solve_line.push(input_tmp_join); // storing the value
			array_solve_ref.push(solve_popover); // storing the reference
			$(".input_field_sol_"+sol_step).append('<span id="solve_content_'+solve_count+'" class="input_content_calc input_content_s">'+variable_solve+'</span>');
			var solve_ref = solve_count + 1;
			$('#btn_sol_solve_'+solve_count).after('<button id="btn_sol_solve_'+solve_ref+'" class="btn btn-success btn-group-s calc_btns btn_sol_solve_ref">'+variable_solve+'</button>');
			$("#btn_sol_solve_"+solve_ref).popover({
				html : true,
				content: array_solve_ref[solve_count],
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
			$('#dyn_ans_btn_solve').append('<button id="btn_ans_solve_'+solve_ref+'" class="btn btn-success btn_ans_solve_ref btn-group-a">'+variable_solve+'</button>');
			$('#btn_ans_solve_'+solve_ref).popover({
				html: true,
				content: array_solve_ref[solve_count],
				placement: 'top',
				trigger: 'hover',
				container: 'body'
			});
			solve_count++;
			variable_solve = String.fromCharCode(variable_solve.charCodeAt(0) + 1);
		}
		$('#mal_input_field_solve').html("");
	});
	
	// Cancel calculation
	$('#btn_solve_cancel').click(function(e){
		e.preventDefault();
		$('#mal_input_field_solve').html("");
	});
	
	/*
	======= TEST FUNCTIONS ========
	*/
	
	$(add_button_text).click(function(e){
		e.preventDefault();
		$("#mal-input-text").focus();
	});
	
	$(".modal").on('shown', function(){
		$(this).find("[autofocus]:first").focus();
	});
	
	$(wrapper).on("click",".remove_field", function(e){ //user click on remove text
		e.preventDefault(); $(this).parent('font').remove(); x--;
	})
});

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
