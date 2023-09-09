import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UserService } from 'src/services/user.service';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import { DestroyedSubject } from 'src/services/destroyed.service';
import { HttpClientModule } from '@angular/common/http';
import { httpInterceptorProviders } from 'src/services/interceptors';
import { HomeComponent } from './Components/home/home.component';
import {MatButtonModule} from '@angular/material/button';
import { ApiService } from 'src/services/api.service';
import { EggsInfoComponent } from './Components/eggs-info/eggs-info.component';
import {MatExpansionModule} from '@angular/material/expansion';
import { ItemsListComponent } from './Components/items-list/items-list.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations'; 
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    EggsInfoComponent,
    ItemsListComponent
  ],
  imports: [
    BrowserModule,
    NoopAnimationsModule,
    AppRoutingModule,
    MatProgressBarModule,
    HttpClientModule,
    MatButtonModule,
    MatExpansionModule,
    MatProgressSpinnerModule
  ],
  providers: [UserService, ApiService, DestroyedSubject, httpInterceptorProviders],
  bootstrap: [AppComponent]
})
export class AppModule { }
