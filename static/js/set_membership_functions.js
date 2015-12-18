$(document).ready(function() {

});

var user_pw = '';
var join_button = $('.btn_add_user_to_set');

join_button.click(function() {
    console.log('hellooo');
    var pw_required = join_button.data('pw-required');
    console.log(pw_required);
    if(pw_required){
        var pw_input = $('#joinSetPassword');
        user_pw = pw_input.val();
        if(user_pw == ''){
            window.alert('Vennligst tast inn passord for å bli med i kurset.')
        } else {
            add_user_to_set();
        }
    } else {
        add_user_to_set();
    }
});

function add_user_to_set(){
    $.post('/add-user-to-set/', {'csrfmiddlewaretoken': getCookie('csrftoken'), 'set_id': set_id, 'password': user_pw}, function(result){
        console.log(result);
        location.reload();
    });
}