import { Component, Input, OnInit } from '@angular/core';
import { IEggsInfo } from '../home/home.component';

@Component({
  selector: 'app-card-item',
  templateUrl: './card-item.component.html',
  styleUrls: ['./card-item.component.scss']
})
export class CardItemComponent implements OnInit {
  @Input() eggsInfo: IEggsInfo | undefined;

  constructor() { }

  ngOnInit(): void {
  }

}
