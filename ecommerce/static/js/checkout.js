$(document).ready(function () {

    $('#paywithrazorpay').click(function (e){

        e.preventDefault();
        var check=document.querySelector('input[name="check"]:checked')
        if (!check){
        
            var country = $("[name = 'country']").val();
            var firstname = $("[name = 'fname']").val();
            var lastname = $("[name = 'lname']").val();
            var email = $("[name = 'email']").val();
            var phone = $("[name = 'phone']").val();
            var address1 = $("[name = 'address1']").val();
            var address2 = $("[name = 'address2']").val();
            var city = $("[name = 'city']").val();
            var state = $("[name = 'state']").val();
            var zip = $("[name = 'zipcode']").val();
            var order_for_others ="False";
            var token = $("[name='csrfmiddlewaretoken']").val();
            console.log("else case")
        }                                     
        if (check){
            var country = $("[name ='tempcountry']").val();
            var firstname = $("[name = 'tempfname']").val();
            var lastname = $("[name = 'templname']").val();
            var email = $("[name = 'tempemail']").val();
            var phone = $("[name = 'tempphone']").val();
            var address1 = $("[name = 'tempaddress1']").val();
            var address2 = $("[name = 'tempaddress2']").val();
            var city = $("[name = 'tempc']").val();
            var state = $("[name = 'temps']").val();
            var zip = $("[name = 'tempz']").val();
            var order_for_others = check;
            var token = $("[name='csrfmiddlewaretoken']").val();
            
            console.log("if case")

        }
        
        
        
       
        if(firstname == "" || lastname == "" || email == "" || phone == "" || address1 == "" || 
            state == "" || city == "" || country == "" || zip == "") 
            {
                swal("Alert!", "All fields are mandatory!", "error");

                return false;

            }
        else
        {  
            $.ajax({
                
                method: "GET",
                url: "/orders/check_out/proced-to-pay/",
                success: function (response) {
                    
                   
                    var options = {
                        "key": "rzp_test_FVH1KVcHhptVkl", // Enter the Key ID generated from the Dashboard
                        "amount": parseInt(response.total_price * 100), // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Uniq Fassion",
                        "description": "Test Transaction",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            alert(responseb.razorpay_payment_id);
                              
                             
                            data = {

                                "first_name":firstname,
                                "last_name":lastname ,
                                "phone": phone ,
                                "email": email ,
                                "address1": address1,
                                "address2": address2,
                                "zip": zip,
                                "state": state, 
                                "city": city ,
                                "country": country, 
                                "order_for_others":order_for_others,
                                "paymentmode": "razorpay",
                                "payment_id" : responseb.razorpay_payment_id,
                                csrfmiddlewaretoken : token,
                            }
                            

                            $.ajax({
                              
                                method: "POST",
                                url: "/orders/check_out/online/",
                                data: data,
                                
                                success: function (responsec){
                                    swal("Congratulations!",responsec.status, "success").then ((value) => {
                                        window.location.href = '/order/my_orders/'
                                      });

                                }
                            })
                            
                        },
                        "prefill": {
                            "name": firstname + " " +lastname,
                            "email": email,
                            "contact": phone
                        },
                        
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    console.log("anything")
                    var rzp1 = new Razorpay(options);
                    rzp1.open();

                }
            }) ;

           
        }    


        

    });
});