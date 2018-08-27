"use strict";



function ValidatePsw(evt){
	if ($("#password").val() != $("#confirm").val()){
		alert("Passwords don't match");
		evt.preventDefault();
	}
}


// function alertMe(){
// 	alert("Here");
// }



$('#signup').on('submit',ValidatePsw);




// function ValidatePsw(evt){
// 	alert("stop");
// 	evt.preventDefault();
// 	let psw = document.querySelector("#password").value;
// 	let psw1 = document.querySelector("#confirm").value;

// 	if (psw != psw1){
// 		console.log("Passwords don't match");
// 	}
// }
// let form = document.querySelector("#signup");

// form.addEventListener('submit', ValidatePsw)