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

function load_chapters(){
    var set_id = $('#set_id').text();
    $('#game_nav').hide();
    $('#chapter_title').text("");
    $('#level_title').text("");
    $('#game_content').fadeOut('fast', function(){
        $(this).load('../' + set_id + '/chapters/', function () {
            lock_game_contents();
            append_medal_star();
            $(this).fadeIn('fast', function(){
                update_progress_bar();
            });
        });
    });
}

function load_levels(chapter_id){
    $('#game_content').fadeOut('fast', function () {
        $(this).load('../' + chapter_id + '/levels/', function () {
            unlock_levels($('#progress_number').text());
            lock_game_contents();
            $(this).fadeIn('fast', function(){
                $('#game_nav').fadeIn();
            });
        });
    });
}

function load_template(level_id){
    $('#game_content').fadeOut('fast', function () {
        $(this).load('../' + level_id + '/template/', function () {
            $(this).fadeIn('fast', function(){
                $('#game_nav').fadeIn(function(){
                    redraw_mathquill_elements();
                });
            });
        });
    });
}

function post_answer(submit_dict){
    $('#game_content').fadeOut('fast', function () {
        $.post('../' + current_level + '/answer/', submit_dict, function(result){
            $('#game_content').html(result).fadeIn('fast', function(){
                $('#game_nav').fadeIn(function(){
                    redraw_mathquill_elements();
                });
            });
        });
    });
}

function lock_game_contents(){
    // Set the disable attribute to all locked chapters/levels
    $('.btn_locked').each(function () {
        $(this).attr('disabled', true).children().remove(); //TODO: hide/remove locked content (cheat-proof?)
    });
}

function update_progress_bar(){
    $('.progress-bar').each(function(){
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
        }
    });
}

function append_medal_star(){
    $('.chapter_ribbon').each(function(){
        $(this).append('<div class="star-5-points"></div>');
    });
}

function unlock_levels(progress_number){

}