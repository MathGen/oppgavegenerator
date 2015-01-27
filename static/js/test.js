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
	var add_button_text   		= $(".add_field_button_text"); //Add button ID
	var add_button_var			= $(".add_field_button_var");  //Add button ID
	var add_button_equal		= $(".add_field_button_equal");
	var add_button_addition 	= $(".add_field_button_addition");
	var add_button_subtraction	= $(".add_field_button_subtraction");
	var add_button_x			= $(".add_field_button_x");
	var variable				= "a";
	var R						= 0;
   
	var x = 1; //initlal text box count
	$(add_button_text).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			$(wrapper).append('<input id="input_text" type="text" style="background-color:#5BC0DE;" name="mytext[]"/><a href="#" class="remove_field"> </a>'); //add input box
		}
	});
	
	$(add_button_var).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			$(wrapper).append('<font size="14" id="R'+R+'" color="#D9534F">'+variable+'</font>');
		}
		variable = String.fromCharCode(variable.charCodeAt(0) + 1);
		R = R + 1;
	});
	
	$(add_button_x).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<font size="14" color="#F0AD4E">x </font>');
		}
	});
	
	$(add_button_equal).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<font size="13"> = </font>');
		}
	});
	
	$(add_button_addition).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<font size="14"> + </font>');
		}
	});
	
	$(add_button_subtraction).click(function(e){
		e.preventDefault();
		if(x < max_fields){
			x++;
			$(wrapper).append('<font size="14"> - </font>');
		}
	});
    
	$(wrapper).on("click",".remove_field", function(e){ //user click on remove text
		e.preventDefault(); $(this).parent('div').remove(); x--;
	})
});