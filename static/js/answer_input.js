$(document).ready(function () {
    var radio_btn = '<input type="radio" name="rbtnCount" />';
    var answer_box = '<input type="textbox" name="answer_box" />';
    var text = 'some text';
    var template_type = $('#template_type').html();
    if (String(template_type) == 'multiple') {
        arr_choices = $('#choices').html();
        arr_choices = arr_choices.split('§');
        for (i = 0; i < arr_choices.length; i++) {
            text = arr_choices[i] + '<br />';
            $('#target').append('<input type="radio" name="answer_button" id="radio' + i + '" value="' + arr_choices[i] + '"/>' + text);
        }
    }
    else if (template_type == 'normal') {
        var number_of_answers = $('#template_type').html();
        for (i = 0; i < number_of_answers; i++) {
            $('#target').append(answer_box);
        }
    }
    else if (template_type == 'insert') {
        var number_of_answers = $('#template_type').html();
        for (i = 0; i < number_of_answers; i++) {
            $('#target').append(answer_box); //todo: This needs to be inserted into text where needed.
        }
    }
});
//todo: event listener to the submit button and then post dat shit, yo.
//todo: add answer textbox, yo.
