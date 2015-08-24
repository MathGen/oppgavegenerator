// This file is the result of a last minute fix for the game.js file sending multiple post requests to the answer view

$(document).ready(function () {
    update_progress_bar_level();
    draw_level_stars();
    var graph_expressions = $('#get_graph').text();
    if ((graph_expressions != "[]") && (graph_expressions != "None") && (graph_expressions != "")) {
        dcg_init_game_graph();
    }
    $('#game_nav').fadeIn(function () {
        redraw_mathquill_elements();
    });

    $(document).on('click', '#v_new_question', function(){
        load_level_template(current_level);
    });
    redraw_mathquill_elements()
});

/**
 * Updates the progress-bar which indicates the progress towards unlocking a new star for the current level.
 */
function update_progress_bar_level() {
    console.log("updating progress bar for level");
    var stars = parseInt($('#num_stars').text());
    var rating = $('#get_ulp').text(); // ulp = user level progress
    switch (stars) {
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
    var value = ((rating - rating_from) / (rating_to - rating_from)) * 100;
    if (stars === 5) {
        value = 100;
    }
    $('.star_progress').find('.progress-bar').width(value + '%').attr('aria-valuenow', value);
}

/**
 * Draws the amount of stars the user has unlocked in this current level.
 */
function draw_level_stars() {
    console.log("drawing level stars");
    var stars = $('#num_stars').text();
    $('.progress_star').each(function (index) {
        if (index < stars) {
            $(this).toggleClass('glyphicon-star-empty glyphicon-star');
        }
    });
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
                    //print_solution();
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

function display_loading_icon(boolean){
    if(boolean){
        $('#game_loading').show();
    } else{
        $('#game_loading').hide();
    }
}

/**
 * Loads a template given by the selected level without ajax to avoid
 * multiple answers being sent.
 * @param {number} level_id - The id of the selected level.
 */
function load_level_template(level_id){
    console.log("loading a template");
    var submit_dict = {};
    submit_dict['set_id'] = current_set;
    submit_dict['chapter_id'] = current_chapter;
    submit_dict['level_id'] = level_id;
    submit_dict['csrfmiddlewaretoken'] = getCookie('csrftoken');
    post('/game/template/', submit_dict)
}