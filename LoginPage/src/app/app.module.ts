import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent , ErrorComponent} from './login/login.component';
import { SearchComponent } from './search/search.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatInputModule } from '@angular/material';
import {MatStepperModule} from '@angular/material/stepper';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatBadgeModule } from '@angular/material/badge';
import { MatDividerModule } from '@angular/material/divider';
import { MatGridListModule } from '@angular/material/grid-list';
import {MatSelectModule} from '@angular/material/select';
import {MatTableModule} from '@angular/material/table';
//import {HttpModule} from '@angular/common/http';
import {MatExpansionModule} from '@angular/material/expansion';

import {MatListModule} from '@angular/material/list';

import { HttpClientModule } from '@angular/common/http';
import { LoginService } from 'src/service/login.service';
import { SearchService } from 'src/service/search.service';
import { CostComponent } from './cost/cost.component';
import { CountComponent } from './count/count.component';
import { ReportComponent } from './report/report.component';

@NgModule({
  
  declarations: [
    AppComponent,
    LoginComponent,
    SearchComponent,
    ErrorComponent,
    CostComponent,
    CountComponent,
    ReportComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    MatTableModule,
    ReactiveFormsModule,
    MatSelectModule,
    HttpClientModule,
    MatInputModule,
    MatStepperModule,
    MatFormFieldModule,
    MatButtonModule,
    MatCardModule,
    MatDatepickerModule,
    MatBadgeModule,
    MatDividerModule,
    MatSnackBarModule,
    BrowserAnimationsModule,
    MatGridListModule,
    MatIconModule,
    MatExpansionModule,
    MatListModule
  ],
  exports: [
    BrowserAnimationsModule,
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule,
    
  ],
  entryComponents: [
    ErrorComponent
],
  providers: [HttpClientModule, LoginService, SearchService],
  bootstrap: [AppComponent]
})
export class AppModule { }
