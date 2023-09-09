import { Component, Input, OnInit } from '@angular/core';
import { BehaviorSubject, ReplaySubject } from 'rxjs';
import { IEggsInfo } from '../home/home.component';

@Component({
  selector: 'app-items-list',
  templateUrl: './items-list.component.html',
  styleUrls: ['./items-list.component.scss']
})
export class ItemsListComponent implements OnInit {
@Input() set allEggsInfoData(value: IEggsInfo[]){
  this.allEggsSubject.next(value);
}

private allEggsSubject = new ReplaySubject<IEggsInfo[]>(1);
allEggs$ = this.allEggsSubject.asObservable();

hideToggle = true;

  constructor() { }

  ngOnInit(): void {
  }

}
