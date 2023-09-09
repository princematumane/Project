import { Injectable } from '@angular/core';
import { DestroyedSubject } from './destroyed.service';

@Injectable()
export class UserService {
  subscriptions: PushSubscription[]=[];
  constructor(private readonly destroyedSubject: DestroyedSubject) { }

  dispose(){
    this.subscriptions.forEach(subscription =>subscription.unsubscribe())
  }
}
