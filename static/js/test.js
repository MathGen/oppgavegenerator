$(document).ready(function() {
	var max_fields      = 10; //maximum input boxes allowed
	var wrapper         = $(".input_fields_wrap"); //Fields wrapper
	var add_button      = $(".add_field_button"); //Add button ID
   
	var x = 1; //initlal text box count
	$(add_button).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			$(wrapper).append('<div class="test_field"><input type="text" name="mytext[]"/><a href="#" class="remove_field">Remove</a></div>'); //add input box
		}
	});
    
	$(wrapper).on("click",".remove_field", function(e){ //user click on remove text
		e.preventDefault(); $(this).parent('div').remove(); x--;
	})
});

$(document).ready(function() {
	var max_fields      		= 20; //maximum input boxes allowed
	var wrapper         		= $(".input_fields_test"); //Fields wrapper
	var button_wrapper			= $(".add_button_equal");
	var add_button_text   		= $(".add_field_button_text"); //Add button ID
	var add_button_var			= $(".add_field_button_var");
	var add_button_equal		= $(".add_field_button_equal");
	var add_button_addition 	= $(".add_field_button_addition");
	var add_button_subtraction	= $(".add_field_button_subtraction");
	var add_button_x			= $(".add_field_button_x");
	var clean_button			= $(".button_clean_mal");
	var remove_last_content		= $(".button_remove_last_content");
	var variable				= "a";
	var R						= 0;
	var input_text_count		= 0;
	var content_count			= 0;
	var x 						= 1; //initial text box count
	
	$(add_button_text).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			$(wrapper).append('<span class="input_content_text input_content'+content_count+'"><input id="input_text" type="text" style="background-color:#5BC0DE;" name="mytext[]"/></span>'); //add input box
			content_count = content_count + 1;
		}
	});
	
	$(add_button_var).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			$(wrapper).append('<span id="R'+R+'" class="input_content_var input_content'+content_count+'">'+variable+'</span>');
			variable = String.fromCharCode(variable.charCodeAt(0) + 1);
			R = R + 1;
			content_count = content_count + 1;
		}
	});
	
	// Add unknown X
	$(add_button_x).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_x input_content'+content_count+'">x </span>');
			content_count = content_count + 1;
		}
	});
	
	$(add_button_equal).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_op input_content'+content_count+'"> = </span>');
			$(add_button_equal).prop('disabled', true);
			content_count = content_count + 1;
		}
	});
	
	$(add_button_addition).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_op input_content'+content_count+'"> + </span>');
			content_count = content_count + 1;
		}
	});
	
	$(add_button_subtraction).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<span class="input_content_op input_content'+content_count+'"> - </span>');
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
	});
	
	// Delete the last input component
	$(remove_last_content).click(function(e){
		e.preventDefault();
		if($(".input_content"+content_count).find(".input_content_var")){
			$("#mal_input_field span:last-child").remove();
			if(variable != "a"){
				variable = String.fromCharCode(variable.charCodeAt(0) - 1);
			}
			R--;
		}
		else if($(".input_content"+content_count).find(".input_content_x")){
			$("#mal_input_field span:last-child").remove();
		}
		else if($(".input_content"+content_count).find(".input_content_text")){
			$("input_content_text.input_content"+content_count).remove();
		}
		if(content_count > 0){
			x--;
			content_count--;
		}
	});
    
	$(wrapper).on("click",".remove_field", function(e){ //user click on remove text
		e.preventDefault(); $(this).parent('font').remove(); x--;
	})
});