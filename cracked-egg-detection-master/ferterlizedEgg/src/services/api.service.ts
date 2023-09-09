import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { IEggsInfo } from 'src/app/Components/home/home.component';

@Injectable()
export class ApiService {

  apiUrl: string = 'http://localhost:8000'
  constructor(private httpClient: HttpClient) {}

  getScan(): Observable<any> {
    const url = `${this.apiUrl}/`;
    return this.httpClient.get<IEggsInfo>(url);
  }
  
  getAllScan(): Observable<any[]> {
    const url = `${this.apiUrl}/all`;
    return this.httpClient.get<IEggsInfo[]>(url);
  }
}
