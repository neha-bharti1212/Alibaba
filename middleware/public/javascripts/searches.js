// // var request = require('request');

// // var headers = {
// //    'Content-Type': 'application/x-www-form-urlencoded',
// //    'Accept': 'application/json',
// //    'user-key': process.env.USER_KEY,
// //    'Authorization': process.env.AUTH_KEY
// // };

// // var dataString = 'grant_type=client_credentials&scope=search';

// // var options = {
// //    url: 'https://api.meltwater.com/oauth2/access_token',
// //    method: 'POST',
// //    headers: headers,
// //    body: dataString
// // };

// // function callback(error, response, body) {
// //    if (!error && response.statusCode == 200) {
// //        console.log(body);
// //    }
// // }

// // request(options, callback);



// var request = require('request-promise');
// var async = require('async');
// module.exports = {
//     getSearch: function () {
//         return new Promise(function (resolve, reject) {
//             var comparr = [];
//             var options = {
//                 method: 'POST',
//                 uri: 'https://api.meltwater.com/oauth2/access_token',
//                 headers: {
//                     'Content-Type': 'application/x-www-form-urlencoded',
//                     'Accept': 'application/json',
//                     'user-key': process.env.USER_KEY,
//                     'Authorization': process.env.AUTH_KEY
//                 },
//                 body: "grant_type=client_credentials&scope=search"
//             };
//             console.log("Get Token");
//             request(options)
//                 .then(function (response) {
//                     console.log("hi");
//                     // if(!error && response.statusCode == 200){
//                     //     console.log(body);
//                     // }
//                     console.log('Got Token');
//                     var resp = JSON.parse(response);
//                     var access_token = 'Bearer ' + resp.access_token;
//                     console.log(" ---------- Access Company Details Meltwater API Service ----------  ");
//                     //use this token to get list of companies
//                      var compOptions = {
//                          method: 'GET',
//                          url: 'https://api.meltwater.com/v2/companies',
//                          headers: {
//                              'Accept': 'application/json',
//                              'user-key': process.env.USER_KEY,
//                              'Authorization': access_token
//                          }
//                      };
//                      console.log("Get companies");
//                      request(compOptions)
//                          .then(function (compResponse) {
//                              console.log("Got companies");
//                              var compResp = JSON.parse(compResponse);
//                              var companies = compResp.companies;
//                              for (var i in companies) {
//                                  comparr.push(companies[i].id);
//                              }
//                              console.log(comparr);
//                              //go through each company id and check if the search exists
//                              async.forEachSeries(comparr, function (companyId, callbackSearch) {
//                                  // Send Request to Meltwater API
//                                  let searchOptions = {
//                                      method: 'GET',
//                                      uri: 'https://api.meltwater.com/export/v1/searches?company_id=' + companyId + '&include_query=false',
//                                      headers: {
//                                          'Accept': 'application/json',
//                                          'user-key': process.env.USER_KEY,
//                                         'Authorization': access_token,
//                                      },
//                                      body: "company_id=" + companyId + "&include_query=false"
//                                  };
//                                  request(searchOptions)
//                                     .then(function (searchResponse) {
//                                          var searchResp = JSON.parse(searchResponse);
//                                         var searchRespSorted = (searchResp.searches).sort();
//                                          console.log(searchResp);
//                                          resolve(searchResp)
//                                      });

//                              });
//                          });
//                  });
//          })
//     }
// }


var access_token;
var request = require('request-promise');
var async = require('async');
module.exports = {
    getSearch: function () {
        return new Promise(function (resolve, reject) {
            var comparr = [];
            var options = {
                method: 'POST',
                uri: 'https://api.meltwater.com/oauth2/access_token',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json',
                    'user-key': "f85448a8491fc21c65a582f9b74b1440",
                    'Authorization': process.env.AUTH_KEY
                },
                body: "grant_type=client_credentials&scope=search"
            };
            console.log("Get Token");
            request(options)
                .then(function (response) {
                    console.log('Got Token');
                    var resp = JSON.parse(response);
                    console.log(resp);
                    access_token = 'Bearer ' + resp.access_token;
                    // exports.bearer_key = JSON.stringify(access_token);
                    // console.log(exports.bearer_key);
                    console.log(" ---------- Access Company Details Meltwater API Service ----------  ");
                    //use this token to get list of companies
                    var compOptions = {
                        method: 'GET',
                        uri: 'https://api.meltwater.com/v2/companies',
                        headers: {
                            'Accept': 'application/json',
                            'user-key': "f85448a8491fc21c65a582f9b74b1440",
                            'Authorization': access_token
                        }
                    };
                    console.log("Get companies");
                    request(compOptions)
                        .then(function (compResponse) {
                            console.log("Got companies");
                            var compResp = JSON.parse(compResponse);
                            var companies = compResp.companies;
                            for (var i in companies) {
                                comparr.push(companies[i].id);
                            }
                            console.log(comparr);
                            //go through each company id and check if the search exists
                            async.forEachSeries(comparr, function (companyId, callbackSearch) {
                                // Send Request to Meltwater API
                                let searchOptions = {
                                    method: 'GET',
                                    uri: 'https://api.meltwater.com/export/v1/searches?company_id=' + companyId + '&include_query=false',
                                    headers: {
                                        'Accept': 'application/json',
                                        'user-key': "f85448a8491fc21c65a582f9b74b1440",
                                        'Authorization': access_token,
                                    },
                                    body: "company_id=" + companyId + "&include_query=false"
                                };
                                request(searchOptions)
                                    .then(function (searchResponse) {
                                        var searchResp = JSON.parse(searchResponse);
                                        var searchRespSorted = (searchResp.searches).sort();
                                        console.log(searchResp);
                                        resolve(searchResp)
                                    });

                            });
                        });
                });
        })
    }
}

module.exports.getbearer = function getbearer(){
    return { bearer_key : access_token};
}

