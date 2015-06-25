$(document).ready(function () {
    load_set_editor($('#set_id').text());
    $('#chapter_container').sortable({placeholder:"list_chapter"}).disableSelection();
    $('.list_chapter').draggable({containment:"#chapter_container", axis:"y"});
});

function load_set_editor(set_id){
    if(set_id){

    }
    else{

    }
}