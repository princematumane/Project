import { Component, Input, OnInit } from '@angular/core';
import { IEggsInfo } from '../home/home.component';

@Component({
  selector: 'app-eggs-info',
  templateUrl: './eggs-info.component.html',
  styleUrls: ['./eggs-info.component.scss']
})
export class EggsInfoComponent implements OnInit {
  @Input() eggsInfo: IEggsInfo | undefined;

  constructor() { }

  ngOnInit(): void {
  }

}
