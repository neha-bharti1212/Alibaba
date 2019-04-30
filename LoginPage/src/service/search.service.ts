import { Injectable } from '@angular/core';
import{ map } from 'rxjs/operators';
import{ HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'

})
export class SearchService {

  constructor(private http: HttpClient) { }

}