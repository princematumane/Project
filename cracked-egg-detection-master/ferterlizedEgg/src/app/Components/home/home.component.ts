import { Component, OnDestroy, OnInit } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { ApiService } from 'src/services/api.service';


export interface IEggsInfo {
  eggsFertilized: string,
  crackedEggsImage: string,
  eggsFertilizedImage: string,
  eggAbnormals: number,
  fertilizedEggsCount: number,
  eggsMajorCrack: number,
  eggsMinorCrack: number,
  total: number
  dataCaptured?: Date
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {

  tempData = {
    eggsFertilized: '',
    crackedEggsImage: '',
    eggsFertilizedImage: '',
    eggAbnormals: 0,
    fertilizedEggsCount: 0,
    eggsMajorCrack: 0,
    eggsMinorCrack: 0,
    total: 0
  };

  isDataLoading = true;

  private eggsInfoDataSubject: BehaviorSubject<IEggsInfo> = new BehaviorSubject(this.tempData);
  eggsInfoData$: Observable<IEggsInfo> = this.eggsInfoDataSubject.asObservable();

  private allEggsInfoDataSubject: BehaviorSubject<any> = new BehaviorSubject([]);
  allEggsInfoData$: Observable<IEggsInfo[]> = this.allEggsInfoDataSubject.asObservable();

  constructor(private readonly apiService: ApiService) { }
  ngOnDestroy(): void {
    this.eggsInfoDataSubject.complete();
    this.allEggsInfoDataSubject.complete();
  }

  ngOnInit(): void {
    this.isDataLoading = true
    this.apiService.getAllScan().subscribe(data => {
      this.isDataLoading = false;
      this.allEggsInfoDataSubject.next(data.sort((a, b) => {
          if (a.dataCaptured && b.dataCaptured) {
              return a.dataCaptured.getTime() - b.dataCaptured.getTime();
          } else if (a.dataCaptured && !b.dataCaptured) {
              return -1; // a comes after b if b.dataCaptured is undefined
          } else if (!a.dataCaptured && b.dataCaptured) {
              return 1; // a comes before b if a.dataCaptured is undefined
          }
          return 0; // leave unchanged if both are undefined
      }));
    });
  }

  fetchEggsData(){
    this.apiService.getScan().subscribe(data => {
      this.eggsInfoDataSubject.next(data);
    });
  }

}
