var phone = document.getElementById('id_otp');
phone.oninvalid = function(event) {
    event.target.setCustomValidity('OTP is 6 characters long');
};
phone.oninput = function(event){
	event.target.setCustomValidity('');
}