var firstnameError = document.getElementById('fname-error')
var lastnameError = document.getElementById('lname-error')
var passwordError = document.getElementById('psw-error')
var phoneError = document.getElementById('phone-error')
var emailError = document.getElementById('email-error')

var formError = document.getElementById('signin_submit_error')
var codeformError=document.getElementById('login_code_error')

function firstnamevalidation(){

    var name = document.getElementById('firstname').value
    if(!name.match(/^[A-Za-z\s]{3,}$/)){
        firstnameError.innerHTML = '<p class="text-danger">first name must be characters only</p>'
    return false;

    }
    firstnameError.innerHTML = '<p class="text-success">valid</p>'
    return true;
}
function lastnamevalidation(){

    var name = document.getElementById('lastname').value
    if(!name.match(/^[A-Za-z\s]{3,}$/)){
        lastnameError.innerHTML = '<p class="text-danger">first name must be characters only</p>'
    return false;

    }
    lastnameError.innerHTML = '<p class="text-success">valid</p>'
    return true;
}

function emailvalidation(){
        
    var email = document.getElementById('email').value
    if(!email.match(/^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{2,3}$/)){
        emailError.innerHTML = '<p class="text-danger">Invalid Email</p>';
        return false;
    }
    emailError.innerHTML ='<p class="text-success">valid</p>'
    return true;

} 

function numbervalidation(){
                
    var phone = document.getElementById('phone').value
    if(!phone.match(/^\d{10}$/)){
        phoneError.innerHTML = '<p class="text-danger">Phone number must be 10 digits only</p>';
        return false;
    }
    phoneError.innerHTML = '<p class="text-success">valid</p>'
    return true;

}

 

function passwordvalidation(){

    var psw1 = document.getElementById('password1').value
    var psw2 = document.getElementById('password2').value
    if(psw1=="" || psw2==""){
        passwordError.innerHTML = 'Field should not be empty';
        return false;
    }
    else if(psw1.length<4){
        passwordError.innerHTML = 'password must be contain 4 or more charactors';
        return false;
    }
    else if(psw1!=psw2){
        passwordError.innerHTML = 'Both passwords are not match';
        return false;
    }
    passwordError.innerHTML ='<p class="text-success">passwords are valid</p>'
    return true;
}

function codevalidation(){

    var otp = document.getElementById('otpcode').value
    if(otp==''){
        codeError.innerHTML = 'Field should not be empty';
        return false;
    }
    codeError.innerHTML = ''
    return true;
}




function formvalidation(){
    if(! firstnamevalidation() || ! lastnamevalidation() || ! emailvalidation()|| ! numbervalidation()|| ! passwordvalidation() ){
        formError.innerHTML = 'Fill all the fields';
        return false;
    }
    formError.innerHTML = ''
    return true;

}

function codeformvalidation(){
    if(! codevalidation() ){
        codeformError.innerHTML = 'code field is empty';
        return false;
    }
    codeformError.innerHTML = ''
    return true;

}