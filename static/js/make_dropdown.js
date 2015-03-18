$(document).ready(function(){
   //create a drop down list from db values
	var category_selection = $('#category_selection');
	var formated_db_topics = "";
	var db_topics = $('#db_topics').html();
	db_topics = db_topics.split('§');
	for(var i = 0; i < db_topics.length; i+=2){
		formated_db_topics = db_topics[i+1].charAt(0).toUpperCase() + db_topics[i+1].slice(1);
		category_selection.append('<option id="'+db_topics[i] + '">'+ formated_db_topics +'</option>');
	}
});