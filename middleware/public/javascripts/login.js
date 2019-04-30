var request = require('request-promise');
var async = require('async');
 module.exports = {
     postUser: function (loginData) {
        return new Promise (function(resolve, reject) {
            console.log("Sending Login Credentials For Validation!")
            console.log(loginData);
            var options = {
                method : 'POST',
                url : 'https://e235da15.ngrok.io/login',
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                },
                body : loginData,
            };
            request(options).then(function(response){
                    console.log("This is the response");
                    console.log(response);
                    console.log (typeof response)
                    //console.log("just checking");
                    data = JSON.parse(response);
                   // console.log (typeof data)
                    console.log(data.message)
                    // console.log(response.message);
                    //  data = response.body;
                    //  console.log("This is the response body");
                    //  console.log(data);
                    //  console.log(data.message);

                    if( data.message == "good" ){
                                //console.log(data.message);
                               // console.log(data.client_key);
                                process.env.AUTH_KEY = "Basic " + data.client_key;
                                console.log(process.env.AUTH_KEY);
                                resolve(response);


                    }else if (data.message == "bad")
                    {
                                console.log(data.message);
                                process.env.AUTH_KEY = "Basic " + data.client_key;
                                resolve(response);
                    }else{
                        console.log("Error!!");
                    }
                
            });
        });
    }
}