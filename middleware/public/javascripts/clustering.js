let bear = require('./searches.js');
var request = require('request-promise');
var async = require('async');
const {Client} = require('pg')
const client = new Client({
    user : "postgres",
    password : "12345",
    host : "localhost",
    port : 5432,
    database : "testdb"
}) 
 module.exports = {
    postSearch: function (dataGot) {
        return new Promise(function (resolve, reject) {
            console.log("Sending Cluster Data")
            var comparr = [];
            let temp_body= dataGot
            console.log(temp_body)
            var bearer_key = bear.getbearer();
            console.log(bearer_key)
            
            //console.log(dataGot.toString())
            var options = {
                method: 'POST',
                uri: 'https://e235da15.ngrok.io/clustering',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: JSON.stringify(temp_body) + JSON.stringify(bearer_key)
                //body: temp_body.toString();

                
            };
            request(options)
                .then(async function (response) {
                    try{
                        var resp = response;
                        await client.connect()
                        console.log("Connected!")
                        const results = await client.query("select export_name , created_on, clustered_data, document_count from fitbit_table")
                        console.table(results.rows)
                        console.log(results.rows)
                        console.log("generated Report link =",resp)
                        resolve(results.rows);
                    }
                    catch(ex)
                    {
                        console.log('Error occured ${ex')
                    }
                    finally{
                        await client.end()
                        console.log("Disconnected")
                    }
                    // console.log("the link is generated here");
                    // console.log(resp);
                    // require("openurl").open(resp);
                });
        })
    }
}