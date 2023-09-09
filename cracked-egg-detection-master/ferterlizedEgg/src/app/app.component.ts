import { Component, OnDestroy, OnInit } from '@angular/core';
import { UserService } from 'src/services/user.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'ferterlizedEgg';
  contentLoaded: boolean = true;
  constructor(private readonly userService: UserService){
    setTimeout(() => {
      this.contentLoaded = false;
  }, 5000)
  }

  ngOnInit(): void {
    
  }

  ngOnDestroy(): void {
    this.userService.dispose();
  }
}
