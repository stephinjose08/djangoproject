
var countryError = document.getElementById('country-error')
var firstnameError = document.getElementById('firstname-error')
var lastnameError = document.getElementById('lastname-error')
var emailError = document.getElementById('email-error')
var phoneError = document.getElementById('phone-error')
var addressline1Error = document.getElementById('addressline1-error')
var addressline2Error = document.getElementById('addressline2-error')
var cityError = document.getElementById('city-error')
var stateError = document.getElementById('state-error')
var zipError = document.getElementById('zip-error')
var formError = document.getElementById('form-error')
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
        lastnameError.innerHTML = '<p class="text-danger">last name must be characters only</p>'
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
function addressvalidation1(){
        
    var address = document.getElementById('address1').value
    if(address==''){
        addressline1Error.innerHTML = '<p class="text-danger">Field should not be empty</p>';
        return false;
    }
    addressline1Error.innerHTML = '<p class="text-success">valid</p>'
    return true;
}
function addressvalidation2(){
        
    var address = document.getElementById('address2').value
    if(address==''){
        addressline2Error.innerHTML = '<p class="text-danger">Field should not be empty</p>';
        return false;
    }
    addressline2Error.innerHTML = '<p class="text-success">valid</p>'
    return true;
}
function cityvalidation(){
        
    var city = document.getElementById('city').value
    if(city==''){
        cityError.innerHTML = '<p class="text-danger">Field should not be empty</p>';
        return false;
    }
    cityError.innerHTML ='<p class="text-success">valid</p>'
    return true;
}
function statevalidation(){
        
    var city = document.getElementById('state').value
    if(city==''){
        cityError.innerHTML = '<p class="text-danger">Field should not be empty</p>';
        return false;
    }
    cityError.innerHTML ='<p class="text-success">valid</p>'
    return true;
}
function zipvalidation(){
        
    var zip = document.getElementById('zip').value
    if(!zip.match(/^\d{6}$/)){
        zipError.innerHTML = '<p class="text-danger">Enter six number pincode</p>';
        return false;
    }
    zipError.innerHTML ='<p class="text-success">valid</p>'
    return true;
}
function formvalidation(){
    if(document.querySelector('input[name="check"]:checked')){
        if(! firstnamevalidation() || ! lastnamevalidation() || ! emailvalidation() || ! numbervalidation()|| ! addressvalidation1() || !addressvalidation2() || ! cityvalidation() || ! statevalidation() || ! zipvalidation() ){
            formError.innerHTML = '<p class="text-danger">fill all fields</p>';
            return false;
        }
        formError.innerHTML = ''
        return true;  
    }
}

