import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, FormBuilder } from '@angular/forms';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import {ViewChild} from '@angular/core';
import { Validators } from '@angular/forms';
import { RequestOptions } from '@angular/http';
import { MAT_MOMENT_DATE_FORMATS, MomentDateAdapter } from '@angular/material-moment-adapter';
import { DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import * as _moment from 'moment';
const moment = _moment;

export interface Section {
  name: string;
  updated: Date;
}
export interface Tile { 
  color : string;
  cols : number ; 
  rows : number;
  text : string;
}

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type' : 'application/json',
    'Authorization' : 'my-auth-token'
  })
};

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
  providers: [{ 
    provide : DateAdapter,
    useClass: MomentDateAdapter,
    deps : [MAT_DATE_LOCALE]
  },
{
  provide: MAT_DATE_FORMATS,
  useValue: MAT_MOMENT_DATE_FORMATS
},
],
})


export class SearchComponent implements OnInit {
  isLinear = true;
  firstFormGroup : FormGroup;
  secondFormGroup: FormGroup;
  thirdFormGroup: FormGroup;
  forthFormGroup: FormGroup;
  startdate : Date;
  enddate : Date;
  searchList: any;
  exports: any;
  start_date = new Date(2009,1,1);
  minDate1 = new Date(2009,1,1);
  maxDate1 = new Date (2019,2,22);
  minDate2 = new Date(2009,1,2);
  maxDate2 = moment();
  name = new FormControl('');
  bool : number = 1;
  count: number = 0;
  date;
  json;
  report_result : any ;
  searchText : any = [];
  searchName : any;
  SearchArr : any;
  cardContent = false;
  tiles: Tile[] = [
    // {
    //   text: 'Cost',
    //   cols: 1,
    //   rows: 1,
    //   color: 'lightblue'
    // },
    // {
    //   text: 'Count',
    //   cols: 1,
    //   rows: 1,
    //   color: 'lightgreen'
    // },
    {
      text: 'Report',
      cols: 1,
      rows: 1,
      color: 'lightpink'
    }
  ];

  constructor(
    private http : HttpClient,
    private _formBuilder : FormBuilder
  ) { }
  ngOnInit() {
    this.getSearch();
    this.date = new FormControl(moment().format());
    this.firstFormGroup = this._formBuilder.group({
      firstCtrl: ['', Validators.required]
    });
    this.secondFormGroup = this._formBuilder.group({
      secondCtrl: ['', Validators.required]
    });
    this.thirdFormGroup = this._formBuilder.group({
      thirdCtrl: ['', Validators.required]
    });
    this.forthFormGroup = this._formBuilder.group({
      forthCtrl: ['', Validators.required]
    });
  }

  search(ev) {
    if (this.firstFormGroup.valid) {
      this.bool = this.bool * 1;
      this.SearchArr = this.firstFormGroup.value;
      this.SearchArr.firstCtrl.forEach(search => {
        console.log(search.search_id)
      });
    } else {
      this.bool = this.bool * 0;
    }

    if (this.secondFormGroup.valid) {
      this.bool = this.bool * 1;
      this.startdate = this.secondFormGroup.value;
    } else {
      this.bool = this.bool * 0;
    }
    if (this.thirdFormGroup.valid) {
      this.bool = this.bool * 1;
      this.enddate = this.thirdFormGroup.value;
    } else {
      this.bool = this.bool * 0;
    }
    if (this.forthFormGroup.valid) {
      this.bool = this.bool * 1;
      this.searchName = this.forthFormGroup.value;
    } else {
      this.bool = this.bool * 0;
    }
    if (this.bool == 1) {
      this.searchText.push(this.SearchArr, this.startdate, this.enddate, this.searchName);
      this.json = JSON.stringify(this.searchText);
      this.searchText = JSON.parse(this.json);
      console.log(this.searchText);
      console.log(this.json);
      this.cardContent = true;
      this.postSearch(this.json);
    } else {
      console.log("If this throws error. I'm sleeping!");
    }
  }

  getSearch() {
    this.http.get('/api/searches').pipe(map(data => {
      this.searchList = data;
    })).subscribe();
  }

  postSearch(data) {
    this.http.post('/api/clustering', data, httpOptions).pipe(map(response => {
      this.exports = response;
      console.log(response);
      //this.getCluster();
    })).subscribe();
  }
  // getCluster(){
  //   this.http.get('/api/clustering').pipe(map(data=>{
  //     this.report_result = data;
  //     console.log(data);
  //   })).subscribe();
  // }

}
