var phone = document.getElementById('id_phone');
phone.oninvalid = function(event) {
    event.target.setCustomValidity('Your phone should be in 923xxxxxxxxx');
};
phone.oninput = function(event){
	event.target.setCustomValidity('');
}


var password = document.getElementById('id_password');
password.oninvalid = function(event) {
    event.target.setCustomValidity('Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters. ');
};
password.oninput = function(event){
	event.target.setCustomValidity('');
}