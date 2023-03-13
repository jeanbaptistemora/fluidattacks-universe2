import { OnInit} from '@angular/core';
import { ActivatedRoute} from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

export const SESSION_OBJECT_ID = 'OficinaSession';

export class AsistenciaComponent {
  constructor(route, cookieService){
    return
  }

  ngOnInit(){
    this.route.params.subscribe(params => {
      this.token = params.token;
      this.CookieService.set(SESSION_OBJECT_ID, this.token);
    });
  }

}
