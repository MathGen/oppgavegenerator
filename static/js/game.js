var current_level = "";
$(document).ready(function () {
    load_chapters();
    // Load levels for the specific chapter
    $(document).on('click', '.btn_chapter', function(e){
        e.preventDefault();
        var chapter_title = $(this).find('.chapter_title').text();
        $('#chapter_title').text(" - " + chapter_title);
        var chapter_id = $(this).attr('id').match(/\d+/);
        load_levels(chapter_id);
    });
    // Load a task from the specific level
    $(document).on('click', '.btn_level', function(e){
        e.preventDefault();
        var level_title = $(this).find('.level_title').text();
        $('#level_title').text(" - " + level_title);
        var level_id = $(this).attr('id').match(/\d+/);
        current_level = level_id;
        load_template(level_id);
    });
    // Go back to main-page (chapter-picker)
    $('.btn_game_back').click(function(e){
        e.preventDefault();
        load_chapters();
    });
});

/**
 * Loads all chapters within the current set.
 */
function load_chapters(){
    var set_id = $('#set_id').text();
    $('#game_nav').hide();
    $('#chapter_title').text("");
    $('#level_title').text("");
    $('#game_content').fadeOut('fast', function(){
        $(this).load('../' + set_id + '/chapters/', function () { //AJAX load
            //append_medal_star(); //TODO: call from a better place.
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
    $('#game_content').fadeOut('fast', function () {
        $(this).load('../' + chapter_id + '/levels/', function () { //AJAX load
            var progress_number = $('#progress_number').text();
            unlock_levels(progress_number);
            get_stars_per_level(progress_number);
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
    $('#game_content').fadeOut('fast', function () {
        $(this).load('../' + level_id + '/template/', function () { //AJAX load
            $(this).fadeIn('fast', function(){
                $('#game_nav').fadeIn(function(){
                    redraw_mathquill_elements();
                });
            });
        });
    });
}

/**
 * Submits the user-answer form and retrieves the solution from the server.
 * @param {dictionary|Object} submit_dict - The dictionary which holds the user-answer form.
 */
function post_answer(submit_dict){
    $('#game_content').fadeOut('fast', function () {
        $.post('../' + current_level + '/answer/', submit_dict, function(result){ //AJAX post
            $('#game_content').html(result).fadeIn('fast', function(){
                $('#game_nav').fadeIn(function(){
                    redraw_mathquill_elements();
                });
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
 * Draws and appends the star inside the ribbon.
 */
function append_medal_star(){
    $('.chapter_ribbon').each(function(){
        $(this).append('<div class="star-5-points"></div>');
    });
}

/**
 * Unlocks all levels the user has reached. Removes the lock.
 * @param {number} progress_number - The progress-number which indicates how many levels is unlocked.
 */
function unlock_levels(progress_number){
    $('.btn_level').each(function(index){
        $(this).removeClass('btn_locked').attr('disabled', false);
        return index < progress_number; // To end the iteration when finished with all unlocked levels.
    });
}

/**
 * Draws the amount of stars the user has reached on each levels.
 * @param {number} progress_number - The progress-number which indicates how many levels is unlocked.
 */
function get_stars_per_level(progress_number){
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