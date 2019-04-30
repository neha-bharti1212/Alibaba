import {
  Component,
  OnInit
} from '@angular/core';
import {
  FormControl,
  Validators
} from '@angular/forms';
import {
  MatSnackBar
} from '@angular/material';
import {
  Router
} from '@angular/router';
import {
  HttpClient,
  HttpHeaders
} from '@angular/common/http';
import {
  map
} from 'rxjs/operators';
import {
  LoginService
} from '../../service/login.service';
import {
  getDefaultService
} from 'selenium-webdriver/edge';
import { SearchService } from 'src/service/search.service';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json'
  })
};



@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  email = new FormControl('', [Validators.required, Validators.email]);
  password = new FormControl('', [Validators.required]);
  data: any = [];
  loginData: any;
  convert : any;
  converted : any;
  bool = 1;
  hide = true;

  constructor(public snackBar: MatSnackBar,
    private router: Router,
    private http: HttpClient,
    private login: LoginService
  ) {}

  ngOnInit() {

  }

  getErrorMessage() {
    return this.email.hasError('required') ? 'You must enter an email_id' :
      this.email.hasError('email') ? 'Not a valid email' : '';
  }


  authenticate(event) {
    if (this.email.value === '' || this.password.value === '') {
      console.log('Field is empty');
    } else {
      // tslint:disable-next-line:max-line-length

      if (this.email.value.indexOf('@meltwater.com')) {
        this.data.push(this.email.value, this.password.value);
        this.loginData = this.data;
        console.log("Data to be sent for Verification");
        this.postUser(this.loginData);
        
      } else {
        this.router.navigate(['login']);
        // tslint:disable-next-line: no-use-before-declare
        this.snackBar.openFromComponent(ErrorComponent, {
          duration: 1000,
        });
      }
    }
  }

  // getUser() {
  //   this.http.get('/api/login').pipe(map(data => {
  //     this.loginData = data;
  //     console.log("getting");
  //     console.log(data);

  //   })).subscribe();
  // }

  postUser(data) {
    console.log('Post User')
    console.log(data)
    this.http.post('/api/logindata', data).pipe(map(data => {
      this.loginData = data;
      console.log("posting");
      console.log(data);
      this.convert =JSON.stringify(data);
      this.converted = JSON.parse(this.convert);
      if (this.converted.client_key == "")
        this.bool = this.bool * 1;
      else
        this.bool = this.bool * 0;
      if ( this.bool == 0)
        this.router.navigate(['search']);
    })).subscribe();
  }
}





@Component({
  selector: 'app-authentication-snack',
  template: `<span class="errorField">
          Invalid credentials! Try Again!
    </span>
`,
/*This is styling the error message  */
  styles: [`
    .errorField {
      color: white;
      float : left; 
      font-family: ComicSansMs;
      font-size: 16px;
      line-height: 20px;
      margin: 0 10px 10px;
    }
  `],
})
export class ErrorComponent {}
