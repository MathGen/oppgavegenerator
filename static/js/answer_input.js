var template_type = "";
var number_of_answers = "";
var num_boxx = 0;

$(document).ready(function () {
    var graph_expressions = $('#get_graph').text();
    if($('#task_view').text() == "true" && graph_expressions != "[]" && graph_expressions != 'None'){
        dcg_init_game_graph();
    }
    var text = 'some text';
    template_type = $('#template_type').html();
    var template_specific = $('#template_specific').html();
    number_of_answers = $('#number_of_answers').html();
    var replacing_words = $('#replacing_words').html();
    var primary_key = $('#primary_key').html();
    var variable_dictionary = $('#variable_dictionary').html();
    var w_target = $('#w_target');
    if (String(template_type) == 'multiple') {
        $('.keypad_answer').hide();
        var output = $('#get_question').text();
        $('#mathquill_field').append('<div id="mathquill_output" class="static-math output_mathquill">'+output+'</div>');
        var choices = template_specific;
        choices = choices.split('§');
        for (var i = 0; i < choices.length; i++) {
            w_target.append('<div class="col-lg-12 input_field"><input name="answer_button" type="radio" id="radio'+i+'" value="'+choices[i]+'">' +
                            '<span id="mathquill_output_'+i+'" class="static-math output_mathquill" style="margin-left: 6px"></span></div>');
            MathQuill.StaticMath($('#mathquill_output_' + i)[0]).latex(choices[i]);
        }
        redraw_mathquill_elements();
    }
    else if (template_type == 'normal') {
        var output = $('#get_question').text();
        $('#mathquill_field').append('<div id="mathquill_output" class="static-math output_mathquill">'+output+'</div>');
        $('#w_answer_head').show();
        for (i = 0; i < number_of_answers; i++) {
            if(i > 0){
                w_target.append('<div class="col-md-12"><h4>og</h4></div>');
            }
            w_target.append('<div id="ans_'+i+'" class="col-md-12 input_field"><span id="w_input_mathquill_'+i+'" class="math-field form-control input_mathquill input_blanks"></span></div>');
        }
        redraw_mathquill_elements();
    }
    else if (template_type == 'blanks') {
        var output = $('#get_question').text();
        var arr_output = output.split('§');
        for(var i = 0; i < arr_output.length; i++){
            if(i < 1){
                $('#mathquill_field').append('<div class="input_field"><span id="mathquill_output_'+i+'" class="static-math output_mathquill">'+arr_output[i]+'</span></div><hr/>');
            }
            else{
                $('#mathquill_field').append('<div class="input_field"><span id="mathquill_output_'+i+'" class="static-math output_mathquill">'+arr_output[i]+'</span></div><br/>');
            }
            //$('.static-math').addClass('form-control blank_input');
        }
        redraw_mathquill_elements();
        $('.mq-editable-field').each(function(b){
            $(this).attr('id', 'w_input_mathquill_' + b).addClass('input_blanks');
        });
    }
    else if (template_type == 'multifill'){
        var output = $('#get_question').text();
        $('#mathquill_field').append('<div id="mathquill_output" class="static-math output_mathquill">'+output+'</div><hr>');
        var choices = template_specific;
        choices = choices.split('§');
        for (var i = 0; i < choices.length; i++) {
            $('#mathquill_field').append('<div class="input_field multifill_field"><input id="radio'+i+'" type="radio" name="answer_button" value="' + i + '§' + choices[i] + '"><span id="mathquill_output_'+i+'" class="static-math output_mathquill multifill_input">'+choices[i]+'</span></div><br/>');
            $('.mq-editable-field').addClass('form-control blank_input');
        }
        $('.blank_input').each(function(index){
            $(this).attr('id', 'multifill_' + index);
        });
    }

    $('#submit_answer').click(function (e) {
        e.preventDefault();
        var user_answer = "";
        if (template_type == 'multiple') {
            user_answer = get_radio_value('answer_button');
        }
        else if(template_type == 'blanks'){
            $('#mathquill_field').find('.mq-editable-field').each(function(f){
                if(f > 0) {
                    user_answer += '§';
                }
                user_answer += get_latex_from_mathfield(this);
            });
        }
        else if(template_type == 'multifill'){
            var radio_values = get_radio_value('answer_button');
            radio_values = radio_values.split('§');
            user_answer = radio_values[1];
            var boxx_content = get_latex_from_mathfield('#multifill_' + radio_values[0]);
            user_answer = user_answer.replace(/\\MathQuillMathField\{}/g, boxx_content);
        }
        else {
            for (j = 0; j < number_of_answers; j++) {
                if (j > 0) {
                    user_answer += '§';
                }
                //user_answer += ($('#w_input_mathquill_' + j).mathquill('latex'));
                user_answer += get_latex_from_mathfield('#w_input_mathquill_' + j)
            }
        }

        //make a dict with the user answer and the answer:
        var submit_dict = {
            "user_answer" : String(user_answer),
            "csrfmiddlewaretoken" : getCookie('csrftoken'),
            "primary_key" : primary_key,
            "variable_dictionary" : variable_dictionary,
            "template_type" : template_type,
            "template_specific" : template_specific,
            "replacing_words" : replacing_words
        };
        if(answer_validation()) {
            if($('#submit_answer').hasClass('game_submit')){
                submit_dict['chapter_id'] = current_chapter;
                post_answer(submit_dict);
            }
            else{
                post(/answers/, submit_dict);
            }
        }

    });

    $(document).on('keyup', '.input_mathquill', function(e){
        if(e.keyCode == 13){
            $('#submit_answer').click();
        }
    });
});


/**
 * Validates the user-answer before submitting.
 * Checks whether or not the user-input is empty and displays an error-message and preventing from submitting.
 * @returns {boolean} - If validation passed or not.
 */
function answer_validation(){
    var valid = true;
    if(template_type == 'normal'){
        for(var ans = 0; ans < number_of_answers; ans++){
            if(get_latex_from_mathfield('#w_input_mathquill_' + ans) == ''){
                valid = false;
                $('#w_input_mathquill_' + ans).addClass('select_error');
                error_message('ans_' + ans, 'Dette feltet kan ikke være tomt.');
            }
        }
    }
    if(template_type == 'blanks'){
        for(var bla = 0; bla < num_boxx; bla++){
            if(get_latex_from_mathfield('#blank_' + bla) == ''){
                valid = false;
                $('#blank_' + bla).addClass('select_error');
                error_message('blank_' + bla, 'Fyll ut!');
            }
        }
    }
    return valid;
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
 * Checks which radio-button is checked and return its value.
 * @param groupName - Group name of all radio-buttons.
 * @returns {string} - the value of the checked radio-button.
 */
function get_radio_value(groupName) {
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
