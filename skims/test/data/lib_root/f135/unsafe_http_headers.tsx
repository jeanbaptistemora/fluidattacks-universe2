import { HttpHeaders } from '@angular/common/http';
import Observable from '../types.tsx';

type LoginModel ={};
export class AppComponent {

  login(login: LoginModel): Observable<any>{

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-XSS-Protection': 'anything', // Unsafe F135
      'X-Frame-Options': 'anything', // Unsafe F152
    });

  }
}
