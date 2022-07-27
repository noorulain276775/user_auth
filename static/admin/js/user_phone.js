var phone = document.getElementById('id_phone');
phone.oninvalid = function(event) {
    event.target.setCustomValidity('Your phone should be in 923xxxxxxxxx');
};
phone.oninput = function(event){
	event.target.setCustomValidity('');
}