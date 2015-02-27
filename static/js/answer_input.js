$(document).ready(function () {
    var text = 'some text';
    var answer = $('#answer').html();
    var template_type = $('#template_type').html();
    var number_of_answers = 1;


    if(answer.indexOf('§') > -1){
        number_of_answers = answer.split('§');
        number_of_answers = number_of_answers.length;
    }
    if (String(template_type) == 'multiple') {
        choices = $('#choices').html();
        choices = choices.split('§');
        for (i = 0; i < choices.length; i++) {
            text = '`' + choices[i] + '`' + '<br />';
            $('#target').append('<input class="form-control" type="radio" name="answer_button" id="radio' + i + '" value="' + choices[i] + '"/>' + text);
        }
    }
    else if (template_type == 'normal') {
        for (i = 0; i < number_of_answers; i++) {
            $('#target').append('<input class="form-control" type="textbox" name="answer_box" id="ans_box'+ i +'" />');
        }
    }
    else if (template_type == 'insert') {

            $('#target').append(answer_box); //todo: This needs to be inserted into text where needed.

    }


    $('#submit_answer').click(function (e) {
        e.preventDefault();
        var user_answer = "";
        if (template_type == 'multiple') {
            user_answer = getRadioValue('answer_button');
        }
        else {
            for (i = 0; i < number_of_answers; i++) {
                if (i > 0) {
                    user_answer += '§';
                }
                user_answer += document.getElementById('ans_box' + i).value;
            }
        }

        //make a dict with the user answer and the answer:
        var submit_dict = {
            "user_answer" : String(user_answer),
            "answer" : String(answer),
            "csrfmiddlewaretoken" : getCookie('csrftoken')
        };

        post(/answers/, submit_dict);

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