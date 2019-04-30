var express = require('express');
var router = express.Router();
var request = require('request');
var login = require('../public/javascripts/login');
var router = require('express').Router();
const bodyParser = require('body-parser');
var search = require('../public/javascripts/searches');
var cluster = require('../public/javascripts/clustering');
var log;
/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', {
    title: 'Welcome to Alibaba Backend'
  });
});



/*POST the login credentials*/
router.post('/api/logindata', function (req, res) {
  console.log("This is Login...");
  data = req.body;
  log = JSON.stringify({type: "user", username : data[0], password : data[1]});
  console.log("data passed");
  console.log(log)
  login.postUser(log)
    .then(function (resp1) {
      resp2 = JSON.parse(resp1);
      console.log(resp2)
      res.end(resp1)
    });
});



/* Get searches from Export*/
router.get('/api/searches', function (req, res) {
  search.getSearch()
    .then(function (data) {
      console.log("Data sent to angular is this");
      res.json(data.searches);
    });
});


/* Post the selected data*/
router.post('/api/clustering', function (req, res) {
  console.log("Inside Clustering ... ");
  search_arr = [];
  data = req.body;
  // var test = [{
  //   "export_name": "zse",
  //   "created_on": "2019-03-01T05:49:52.505Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-03-01 11:19:48.838972/Report.html",
  //   "document_count": "0"
  // }, {
  //   "export_name": "ExportWorks",
  //   "created_on": "2019-03-01T05:57:15.007Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-03-01 11:27:11.494382/Report.html",
  //   "document_count": "0"
  // }, {
  //   "export_name": "Exports_works",
  //   "created_on": "2019-03-01T08:26:54.690Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-03-01 13:56:50.054895/Report.html",
  //   "document_count": "0"
  // }, {
  //   "export_name": "bhy",
  //   "created_on": "2019-03-01T09:19:56.621Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-03-01 14:49:52.421776/Report.html",
  //   "document_count": "0"
  // }, {
  //   "export_name": "biy",
  //   "created_on": "2019-03-01T11:07:58.185Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-03-01 16:37:54.790325/Report.html",
  //   "document_count": "0"
  // }, {
  //   "export_name": "bhuyt",
  //   "created_on": "2019-04-25T09:29:32.810Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-04-25 14:59:29.918094/Report.html",
  //   "document_count": "167"
  // }, {
  //   "export_name": "ngj",
  //   "created_on": "2019-04-25T09:33:25.612Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-04-25 15:03:22.647189/Report.html",
  //   "document_count": "167"
  // }, {
  //   "export_name": "nji",
  //   "created_on": "2019-04-26T07:06:30.038Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-04-26 12:36:25.760383/Report.html",
  //   "document_count": "25"
  // }, {
  //   "export_name": "lopa",
  //   "created_on": "2019-04-26T10:07:15.927Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-04-26 15:37:12.512486/Report.html",
  //   "document_count": "117"
  // }, {
  //   "export_name": "den",
  //   "created_on": "2019-04-26T10:23:50.430Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-04-26 15:53:47.322337/Report.html",
  //   "document_count": "117"
  // }, {
  //   "export_name": "teu",
  //   "created_on": "2019-04-26T10:40:38.178Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-04-26 16:10:34.833989/Report.html",
  //   "document_count": "25"
  // }, {
  //   "export_name": "het",
  //   "created_on": "2019-04-29T18:01:13.222Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-04-29 23:31:10.423429/Report.html",
  //   "document_count": "25"
  // }, {
  //   "export_name": "test",
  //   "created_on": "2019-04-29T18:07:29.487Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-04-29 23:37:26.763783/Report.html",
  //   "document_count": "25"
  // }, {
  //   "export_name": "test1",
  //   "created_on": "2019-04-29T18:10:43.031Z",
  //   "clustered_data": "https://s3.us-east-2.amazonaws.com/bibinimagebuckets/Data/fitbit/2019-04-29 23:40:40.323562/Report.html",
  //   "document_count": "25"
  // }];
  // res.json(test);
  cluster.postSearch(data)
    .then(function (resp2) {
      console.log("Inside Search Clustering ... ")
      res.json(resp2)
      console.log(resp2)
    });
});



/*Receive the response for Authentication Attempt*/
module.exports = router;