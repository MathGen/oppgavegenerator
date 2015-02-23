$(document).ready(function () {
    var answer_box = '<input type="textbox" name="answer_box" />';
    var text = 'some text';
    var answer = $('#answer').html();
    var template_type = $('#template_type').html();
    if (String(template_type) == 'multiple') {
        choices = $('#choices').html();
        choices = choices.split('§');
        for (i = 0; i < choices.length; i++) {
            text = choices[i] + '<br />';
            $('#target').append('<input type="radio" name="answer_button" id="radio' + i + '" value="' + choices[i] + '"/>' + text);
        }
    }
    else if (template_type == 'normal') {
        var number_of_answers = $('#number_of_answers').html();
        for (i = 0; i < number_of_answers; i++) {
            $('#target').append('<input type="textbox" name="answer_box" id="ans_box'+ i +'" />');
        }
    }
    else if (template_type == 'insert') {
        var number_of_answers = $('#number_of_answers').html();
        for (i = 0; i < number_of_answers; i++) {
            $('#target').append(answer_box); //todo: This needs to be inserted into text where needed.
        }
    }

    $('#submit').click(function(e){


    });

});
//todo: event listener to the submit button and then post dat shit, yo.
//todo: add answer textbox, yo.
//todo: Split answers with § to find number of answers find out where the best place to do that is.

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