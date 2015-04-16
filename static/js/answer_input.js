var template_type = "";
var number_of_answers = "";
var num_boxx = 0;

$(document).ready(function () {
    var text = 'some text';
    template_type = $('#template_type').html();
    var template_specific = $('#template_specific').html();
    number_of_answers = $('#number_of_answers').html();
    var primary_key = $('#primary_key').html();
    var variable_dictionary = $('#variable_dictionary').html();
    var w_target = $('#w_target');
    if (String(template_type) == 'multiple') {
        var output = $('#get_question').text();
        $('#mathquill_field').append('<div id="mathquill_output" class="input_mathquill"></div><hr>');
        $('#mathquill_output').mathquill().mathquill('latex', output);
        var choices = template_specific;
        choices = choices.split('§');
        for (var i = 0; i < choices.length; i++) {
            w_target.append('<div class="col-lg-12 input_field"><input name="answer_button" type="radio" id="radio'+i+'" value="'+choices[i]+'">' +
                            '<span id="mathquill_output_'+i+'" style="margin-left: 6px"></span></div>');
            $('#mathquill_output_' + i).mathquill().mathquill('latex', choices[i]);
        }
    }
    else if (template_type == 'normal') {
        var output = $('#get_question').text();
        $('#mathquill_field').append('<div id="mathquill_output" class="input_mathquill"></div>');
        $('#mathquill_output').mathquill().mathquill('latex', output);
        $('#w_answer_head').show();
        for (i = 0; i < number_of_answers; i++) {
            if(i > 0){
                w_target.append('<div class="col-md-12"><h4>og</h4></div>');
            }
            w_target.append('<div id="ans_'+i+'" class="col-md-12 input_field"><span id="w_input_mathquill_'+i+'" class="form-control input_mathquill"></span></div>');
            $('#w_input_mathquill_' + i).mathquill('editable');
        }
    }
    else if (template_type == 'blanks') {
        var output = $('#get_question').text();
        var arr_output = output.split('\n');
        for(var i = 0; i < arr_output.length; i++){
            if(i < 1){
                $('#mathquill_field').append('<div class="input_field"><span id="mathquill_output_'+i+'" class="input_mathquill"></span></div><hr/>');
            }
            else{
                $('#mathquill_field').append('<div class="input_field"><span id="mathquill_output_'+i+'" class="input_mathquill"></span></div><br/>');
            }
            $('#mathquill_output_' + i).mathquill().mathquill('latex', arr_output[i]);
            $('.mathquill-editable').addClass('form-control blank_input');
        }
    }
    else if (template_type == 'multifill'){
        var output = $('#get_question').text();
        $('#mathquill_field').append('<div id="mathquill_output" class="input_mathquill"></div><hr>');
        $('#mathquill_output').mathquill().mathquill('latex', output);
        var choices = template_specific;
        choices = choices.split('§');
        for (var i = 0; i < choices.length; i++) {
            $('#mathquill_field').append('<div class="input_field multifill_field"><input id="radio'+i+'" type="radio" name="answer_button" value="' + i + '§' + choices[i] + '"><span id="mathquill_output_'+i+'" class="input_mathquill multifill_input"></span></div><br/>');
            $('#mathquill_output_' + i).mathquill().mathquill('latex', choices[i]);
            $('.mathquill-editable').addClass('form-control blank_input');
        }
        $('.blank_input').each(function(index){
            $(this).attr('id', 'multifill_' + index);
        });
    }

    $('#submit_answer').click(function (e) {
        e.preventDefault();
        var user_answer = "";
        if (template_type == 'multiple') {
            user_answer = getRadioValue('answer_button');
        }
        else if(template_type == 'blanks'){
            $('#mathquill_field').find('.blank_input').each(function(f){
                if(f > 0) {
                    user_answer += '§';
                }
                user_answer += $(this).mathquill('latex');
            });
        }
        else if(template_type == 'multifill'){
            var radio_values = getRadioValue('answer_button');
            radio_values = radio_values.split('§');
            user_answer = radio_values[1];
            var boxx_content = $('#multifill_' + radio_values[0]).mathquill('latex');
            user_answer = user_answer.replace(/\\editable\{}/g, boxx_content);
        }
        else {
            for (j = 0; j < number_of_answers; j++) {
                if (j > 0) {
                    user_answer += '§';
                }
                user_answer += ($('#w_input_mathquill_' + j).mathquill('latex'));
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
        if(answer_validation()) {
            post(/answers/, submit_dict);
        }

    });

    $(document).on('keyup', '.input_mathquill', function(e){
        if(e.keyCode == 13){
            $('#submit_answer').click();
        }
    });
});

$(window).load(function(){
    $('.mathquill-rendered-math').mathquill('redraw');
    $('.mathquill-embedded-latex').mathquill('redraw');
});

function answer_validation(){
    var valid = true;
    if(template_type == 'normal'){
        for(var ans = 0; ans < number_of_answers; ans++){
            if($('#w_input_mathquill_' + ans).mathquill('latex') == ''){
                valid = false;
                $('#w_input_mathquill_' + ans).addClass('select_error');
                error_message('ans_' + ans, 'Dette feltet kan ikke være tomt.');
            }
        }
    }
    if(template_type == 'blanks'){
        for(var bla = 0; bla < num_boxx; bla++){
            if($('#blank_' + bla).mathquill('latex') == ''){
                valid = false;
                $('#blank_' + bla).addClass('select_error');
                error_message('blank_' + bla, 'Fyll ut!');
            }
        }
    }
    return valid;
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
