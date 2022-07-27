var first_name = document.getElementById('id_first_name');
first_name.oninvalid = function(event) {
    event.target.setCustomValidity('Please enter Alphabets only.');
};
first_name.oninput = function(event){
	event.target.setCustomValidity('');
}

var last_name = document.getElementById('id_last_name');
last_name.oninvalid = function(event) {
    event.target.setCustomValidity('Please enter Alphabets only.');
};
last_name.oninput = function(event){
	event.target.setCustomValidity('');
}

var phone = document.getElementById('id_phone');
phone.oninvalid = function(event) {
    event.target.setCustomValidity('Your phone should be in 923xxxxxxxxx');
};
phone.oninput = function(event){
	event.target.setCustomValidity('');
}

var password = document.getElementById('id_password');
password.oninvalid = function(event) {
    event.target.setCustomValidity('Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters');
};
password.oninput = function(event){
	event.target.setCustomValidity('');
}

var message_tag = document.getElementById("message_box");
function buttonclose(){ 
   message_tag.style.display = "none"; 
};