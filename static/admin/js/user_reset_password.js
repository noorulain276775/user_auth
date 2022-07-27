var password = document.getElementById('id_new_password');
password.oninvalid = function(event) {
    event.target.setCustomValidity('Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters. ');
};
password.oninput = function(event){
	event.target.setCustomValidity('');
}