import { HttpHeaders } from '@angular/common/http';
import Observable from '../types.ts';

type LoginModel ={};
export class AppComponent {

  login(login: LoginModel): Observable<any>{

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-Frame-Options': 'anything',
    });

  }
}
