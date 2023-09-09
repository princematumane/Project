
import { HTTP_INTERCEPTORS } from "@angular/common/http";
import { LoggingInterceptor } from "./logging-interceptor";

/** Http interceptor providers in outside-in order */
export const httpInterceptorProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: LoggingInterceptor, multi: true },
];
