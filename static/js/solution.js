
$(document).ready(function () {
    // See step-by-step solution
    var v_solution = $('#v_solution');
    var v_panel = $('#v_panel');
    v_solution.click(function (e) {
        e.preventDefault();
        v_panel.fadeIn();
    });

    // Close step-by-step solution
    var v_ok = $('#v_ok');
    v_ok.click(function (e) {
        e.preventDefault();
        v_panel.fadeOut();
    });

    var solution = $('#get_solution').text();
    solution = solution.split('\\n');
    for(var s = 0; s < solution.length; s++){
        $('#mathquill_field').append('<div class="input_field"><div id="mathquill_solution_'+s+'" class="input_mathquill"></div></div><br/>');
        $('#mathquill_solution_' + s).mathquill().mathquill('latex', solution[s]);
    }
});