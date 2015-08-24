var current_level = 0;
var level_progress = 0;
$(document).ready(function () {
    load_chapters();
    //Add current user to the set
    $(document).on('click', '.btn_add_user_to_set', function(e){
        e.preventDefault();
        add_user_to_set();
    });

    // Load levels for the specific chapter
    $(document).on('click', '.btn_chapter', function(e){
        e.preventDefault();
        var chapter_title = $(this).find('.content_title').text();
        $('#chapter_title').text(" - " + chapter_title);
        var chapter_id = $(this).attr('id').match(/\d+/);
        load_levels(chapter_id);
    });
    // Load a task from the specific level
    $(document).on('click', '.btn_level', function(e){
        console.log("btn_level clicked");
        e.preventDefault();
        var level_title = $(this).find('.level_title').text();
        $('#level_title').text(" - " + level_title);
        var level_id = $(this).attr('id').match(/\d+/);
        var level_index = $(this).index()-1; // TODO: fix the level_index so it's not affected by other elements than .btn_level.
        console.log("level_progress: " + level_progress + " level_index: " + level_index);
        if(level_index <= level_progress + 1){
            current_level = level_id;
            load_level_template(level_id);
        }
    });

    // Load a task from the specific level in a requirement type set
    $(document).on('click', '.btn_level_req', function(e){
        e.preventDefault();
        var level_title = $(this).find('.level_title').text();
        $('#level_title').text(" - " + level_title);
        var level_id = $(this).attr('id').match(/\d+/);
        current_level = level_id;
        load_level_template(level_id);
    });

    // Go back to main-page (chapter-picker)
    $('.btn_game_back').click(function(e){
        e.preventDefault();
        load_chapters();
    });
    $(document).on('click', '#v_new_question', function(){
        load_level_template(current_level);
    });
});

function add_user_to_set(){
    var set_id = $('#set_id').text();
    $.post('/add-user-to-set/', {'csrfmiddlewaretoken': getCookie('csrftoken'), 'set_id': set_id}, function(result){
        console.log(result);
        location.reload();
    });
}

function display_loading_icon(boolean){
    if(boolean){
        $('#game_loading').show();
    } else{
        $('#game_loading').hide();
    }
}

/**
 * Loads all chapters within the current set.
 */
function load_chapters(){
    console.log("loading chapters");
    var set_id = $('#set_id').text();
    $('#game_nav').hide();
    $('#chapter_title').text("");
    $('#level_title').text("");
    $('#game_content').fadeOut('fast', function(){
        display_loading_icon(true);
        $(this).load('/game/' + set_id + '/chapters/', function () { //AJAX load
            display_loading_icon(false);
            var progress_number = $('#progress_number');
            level_progress = progress_number.text();
            progress_number.remove();
            unlock_contents('.btn_chapter', level_progress);
            update_medals();
            append_medal_star();
            disable_game_contents();
            $(this).fadeIn('fast', function(){
                update_progress_bar();
            });
        });
    });
}

/**
 * Loads all levels within the specific chapter. Unlocks levels the user has reached.
 * @param {number} chapter_id - The id of the selected chapter.
 */
function load_levels(chapter_id){
    console.log("loading levels");
    $('#game_content').fadeOut('fast', function () {
        display_loading_icon(true);
        $(this).load('/game/' + chapter_id + '/levels/', function () { //AJAX load
            display_loading_icon(false);
            var progress_number = $('#progress_number');
            level_progress = progress_number.text();
            progress_number.remove();
            unlock_contents('.btn_level', level_progress);
            //unlock_contents('.btn_level_req', level_progress);
            get_stars_per_level(level_progress);
            disable_game_contents();
            $(this).fadeIn('fast', function(){
                $('#game_nav').fadeIn();
            });
        });
    });
}

/**
 * Loads a template given by the selected level.
 * @param {number} level_id - The id of the selected level.
 */
function load_template(level_id){
    console.log("loading a template");
    var submit_dict = {};
    current_chapter = $('#get_chapter_id').text();
    submit_dict['chapter_id'] = current_chapter;
    submit_dict['level_id'] = level_id;
    submit_dict['csrfmiddlewaretoken'] = getCookie('csrftoken');
    $('#game_content').fadeOut('fast', function () {
        display_loading_icon(true);
        $.post('../template/', submit_dict, function (result) { //AJAX load
            display_loading_icon(false);
            $('#game_content').html(result).fadeIn('fast', function(){
                setup_answer_input();
                update_progress_bar_level();
                draw_level_stars();
                var graph_expressions = $('#get_graph').text();
                if((graph_expressions != "[]") && (graph_expressions != "None") && (graph_expressions != "")) {
                    dcg_init_game_graph();
                }
                $('#game_nav').fadeIn(function(){
                    redraw_mathquill_elements();
                });
            });
        });
    });
}

/**
 * Loads a template given by the selected level without ajax to avoid
 * multiple answers being sent.
 * @param {number} level_id - The id of the selected level.
 */
function load_level_template(level_id){
    console.log("loading a template");
    var submit_dict = {};
    current_chapter = $('#get_chapter_id').text();
    current_set = $('#set_id').text();
    submit_dict['set_id'] = current_set;
    submit_dict['chapter_id'] = current_chapter;
    submit_dict['level_id'] = level_id;
    submit_dict['csrfmiddlewaretoken'] = getCookie('csrftoken');
    post('/game/template/', submit_dict)
}

/**
 * Submits the user-answer form and retrieves the solution from the server.
 * @param {dictionary|Object} submit_dict - The dictionary which holds the user-answer form.
 */
function post_answer(submit_dict){
    console.log("submitting answer");
    $('#game_content').fadeOut('fast', function () {
        display_loading_icon(true);
        $.post('/game/' + current_level + '/answer/', submit_dict, function(result){ //AJAX post
            console.log(result);
            display_loading_icon(false);
            $('#game_content').html(result).fadeIn('fast', function(){
                    print_solution();
                $('#game_nav').fadeIn(function(){
                    redraw_mathquill_elements();
                });
                if(($('#new_star').text() == 1) || $('#new_medal').text() > 0){
                    $('#achievement_modal').modal('show');
                }
                update_progress_bar_level();
                draw_level_stars();
            });
        });
    });
}

/**
 * Removes the inner-content of all locked chapters/levels.
 */
function disable_game_contents(){
    // Set the disable attribute to all locked chapters/levels
    $('.btn_locked').each(function () {
        $(this).attr('disabled', true).children().remove(); //TODO: hide/remove locked content (cheat-proof?)
    });
}

function update_medals(){
    console.log("updating medals");
    var medals = JSON.parse($('#medals').text());
    $('.ribbon').each(function(index){
        var medal_value = medals[index];
        switch (medal_value){
            case 0:
                $(this).removeClass('medal_bronze').removeClass('medal_silver').removeClass('medal_gold').removeClass('chapter_ribbon').children().remove();
                break;
            case 1:
                $(this).removeClass('medal_silver').removeClass('medal_gold').addClass('medal_bronze').addClass('chapter_ribbon');
                break;
            case 2:
                $(this).removeClass('medal_bronze').removeClass('medal_gold').addClass('medal_silver').addClass('chapter_ribbon');
                break;
            case 3:
                $(this).removeClass('medal_bronze').removeClass('medal_silver').addClass('medal_gold').addClass('chapter_ribbon');
                break;
        }
    });
}

/**
 * Updates the progress-bar for each chapter. Updates the value and the color of the progress-bar.
 */
function update_progress_bar(){
    console.log("updating progress bar");
    var chapter_completion = JSON.parse($('#chapters_completed').text());
    $('.progress-bar').each(function(index){
        $(this).find('.chapter_completion').text(chapter_completion[index]);
        var value = $(this).text().split('/');
        value = (value[0]/value[1])*100;
        $(this).width(value + '%').attr('aria-valuenow', value);
        switch (true){
            case value < 33:
                $(this).addClass('progress-bar-danger').removeClass('progress-bar-warning').removeClass('progress-bar-success');
                break;
            case value < 66:
                $(this).addClass('progress-bar-warning').removeClass('progress-bar-danger').removeClass('progress-bar-success');
                break;
            case value <= 100:
                $(this).addClass('progress-bar-success').removeClass('progress-bar-danger').removeClass('progress-bar-warning');
                break;
        }
    });
}

/**
 * Updates the progress-bar which indicates the progress towards unlocking a new star for the current level.
 */
function update_progress_bar_level(){
    console.log("updating progress bar for level");
    var stars = parseInt($('#num_stars').text());
    var rating = $('#get_ulp').text(); // ulp = user level progress
    switch(stars){
        case 1:
            rating_from = 1250;
            rating_to = 1450;
            break;
        case 2:
            rating_from = 1400;
            rating_to = 1600;
            break;
        case 3:
            rating_from = 1500;
            rating_to = 1800;
            break;
        case 4:
            rating_from = 1700;
            rating_to = 2000;
            break;
        default:
            var rating_from = 1000;
            var rating_to = 1300;
    }
    var value = ((rating-rating_from)/(rating_to-rating_from))*100;
    if(stars === 5){
        value = 100;
    }
    $('.star_progress').find('.progress-bar').width(value+'%').attr('aria-valuenow', value);
}

/**
 * Draws and appends the star inside the ribbon.
 */
function append_medal_star(){
    console.log("appending medal star");
    $('.chapter_ribbon').each(function(){
        $(this).append('<div class="star-5-points"></div>');
    });
}

/**
 * Unlocks all chapters the user has reached. Removes the lock.
 * @param {number} progress_number - The progress-number which indicates how many chapters is unlocked.
 */
function unlock_chapters(progress_number){ //TODO: call this when retrieving the progress_number from back-end.
    $('.btn_chapter').each(function(index){
        $(this).removeClass('btn_locked').attr('disabled', false);
        return index < progress_number; // To end the iteration when finished with all unlocked chapters.
    });
}

/**
 * Unlocks all levels the user has reached. Removes the lock.
 * @param {object} selector - the container of the contents.
 * @param {number} progress_number - The progress-number which indicates how many levels is unlocked.
 */
function unlock_contents(selector, progress_number){
    $(selector).each(function(index){
        $(this).removeClass('btn_locked').attr('disabled', false);
        return index < progress_number; // To end the iteration when finished with all unlocked levels.
    });
}

/**
 * Draws the amount of stars the user has reached on each levels.
 * @param {number} progress_number - The progress-number which indicates how many levels is unlocked.
 */
function get_stars_per_level(progress_number){
    console.log("getting stars for each unlocked level");
    var stars_per_level = JSON.parse($('#spl').text());
    $('.level_progress').each(function(index){
        $(this).find('.progress_star').each(function(i){
            if(i < stars_per_level[index]){
                $(this).toggleClass('glyphicon-star-empty glyphicon-star');
            }
        });
        return index < progress_number; // To end the iteration when finished with all unlocked levels.
    });
}

/**
 * Draws the amount of stars the user has unlocked in this current level.
 */
function draw_level_stars(){
    console.log("drawing level stars");
    var stars = $('#num_stars').text();
    $('.progress_star').each(function(index){
        if(index < stars){
            $(this).toggleClass('glyphicon-star-empty glyphicon-star');
        }
    });
}

/**
 * Opens and draws all steps in solution.
 * Collapse and Un-collapse the panel by button-click.
 */
function print_solution(){
    console.log('printing solution');
    // See step-by-step solution
    var v_solution = $('#v_solution');
    var v_panel = $('#v_panel');
    v_solution.click(function (e) {
        e.preventDefault();
        v_panel.fadeIn(function(){
            redraw_mathquill_elements();
            //$('.mathquill-rendered-math').mathquill('redraw'); // Redraws the latex math when it is shown.
        });
    });

    // Close step-by-step solution
    var v_ok = $('#v_ok');
    v_ok.click(function (e) {
        e.preventDefault();
        v_panel.fadeOut();
    });

    var solution = $('#get_solution').text();
    solution = solution.split('§');
    for(var s = 0; s < solution.length; s++){
        if(document.getElementById("mathquill_solution_" + s) == null){
                console.log('printing step' + s);
            $('#mathquill_field').append('<div class="input_field"><div id="mathquill_solution_' + s + '" class="static-math input_mathquill">' + solution[s] + '</div></div><br/>');
        }
        //$('#mathquill_solution_' + s).mathquill().mathquill('latex', solution[s]);
    }
    console.log('end print solution')
}

function setup_answer_input() {
    console.log("setting up for answer input");
    var template_type = "";
    var number_of_answers = "";
    var num_boxx = 0;

    var graph_expressions = $('#get_graph').text();
    if(($('#task_view').text() == "true") && (graph_expressions != "[]") && (graph_expressions != 'None') && (graph_expressions != "")){
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

    $('#post_answer_game').click(function (e) {
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
                submit_dict['chapter_id'] = current_chapter;
                post_answer(submit_dict);
        }

    });

    $(document).on('keyup', '.input_mathquill', function(e){
        if(e.keyCode == 13){
            $('#post_answer_game').click();
        }
    });

}

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