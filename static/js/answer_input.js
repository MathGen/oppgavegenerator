$(document).ready(function () {
    var text = 'some text';
    var template_type = $('#template_type').html();
    var template_specific = $('#template_specific').html();
    var number_of_answers = $('#number_of_answers').html();
    var primary_key = $('#primary_key').html();
    var variable_dictionary = $('#variable_dictionary').html();
    var w_target = $('#w_target');
    if (String(template_type) == 'multiple') {
        choices = template_specific;
        choices = choices.split('§');
        for (i = 0; i < choices.length; i++) {
            text = '`' + choices[i] + '`' + '<br />';
            w_target.append('<input type="radio" name="answer_button" id="radio' + i + '" value="' + choices[i] + '"/>' + text);
        }
    }
    else if (template_type == 'normal') {
        for (i = 0; i < number_of_answers; i++) {
            //$('#a_target').append('<input class="form-control" type="textbox" name="answer_box" id="ans_box'+ i +'" />');
            if(i > 0){
                w_target.append('<div class="col-md-12"><h4>og</h4></div>');
            }
            w_target.append('<div class="col-md-12 input_field"><span id="w_input_mathquill_'+i+'" class="mathquill-editable form-control input_mathquill"><span class="textarea"><textarea></textarea></span></span></div>');
            $('#w_input_mathquill_' + i).mathquill('revert').mathquill('editable');
        }
    }
    else if (template_type == 'blanks') {
        for(j=0;j<number_of_answers;j++){
            var replaced = $("body").html().replace('@boxx@','`<div class="col-md-12 input_field"><span id="w_input_mathquill_'+j+'" class="mathquill-editable form-control input_mathquill"><span class="textarea"><textarea></textarea></span></span></div>`');
            $("body").html(replaced);
            $('#w_input_mathquill_' + j).mathquill('revert').mathquill('editable');
        }

        w_target.append(answer_box); //todo: This needs to be inserted into text where needed.

    }

    $('#submit_answer').click(function (e) {
        e.preventDefault();
        var user_answer = "";
        if (template_type == 'multiple') {
            user_answer = getRadioValue('answer_button');
        }
        else {
            for (j = 0; j < number_of_answers; j++) {
                if (j > 0) {
                    user_answer += '§';
                }
                //user_answer += document.getElementById('ans_box' + i).value;
                var w_input = ($('#w_input_mathquill_' + j).mathquill('latex'));
                user_answer += latex_to_sympy(w_input);
            }

        }

        //make a dict with the user answer and the answer:
        var submit_dict = {
            "user_answer" : String(user_answer),
            "csrfmiddlewaretoken" : getCookie('csrftoken'),
            "primary_key" : primary_key,
            "variable_dictionary" : variable_dictionary,
            "template_type" : template_type,
            "template_specific" : template_specific
        };

        post(/answers/, submit_dict);

    });

    $(document).on('keyup', '.input_mathquill', function(e){
        $('#submit_answer').click();
    });
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

function getRadioValue(groupName) {
    var radios = document.getElementsByName(groupName);
    var rdValue; // declares the global variable 'rdValue'
    for (var i = 0; i < radios.length; i++) {
        var someRadio = radios[i];
        if (someRadio.checked) {
            rdValue = someRadio.value;
            break;
        }
        else rdValue = 'noRadioChecked'; //todo prevent this from happening by forcing the user to select one before submitting
    }
    return rdValue;
}

function latex_to_sympy(latex){
    var la = latex;
	la = la.replace(/{/g,'(');
	la = la.replace(/}/g,')');
	la = la.replace(/\\cdot/g,'*');
	la = la.replace(/\\left/g,'');
	la = la.replace(/\\right/g,'');
    var la2 = "";
    i = 0;
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
        la2 += la[i];
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