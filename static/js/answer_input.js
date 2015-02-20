$(document).ready(function() {
    var radio_btn = '<input type="radio" name="rbtnCount" />';
    var answer_box = '<input type="radio" name="answer_box" />';
    var template_type = 0;


    if(template_type == 'multiple') {
        var choices = 0; //get choices.split(§)
        for (i = 0; i < choices.size(); i++) {
            $('#target').append(radio_btn);
        }
    }
    else if(template_type == 'normal'){
        var number_of_answers = 0;
        for (i = 0; i < number_of_answers; i++) {

        }
    }
    else if(template_type == 'insert'){
        var number_of_answers = 0;
        for (i = 0; i < number_of_answers; i++) {

        }
    }


});