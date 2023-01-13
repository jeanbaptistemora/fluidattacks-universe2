import { OnInit} from '@angular/core';
import { ActivatedRoute} from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

export const SESSION_OBJECT_ID: string = 'OficinaSession';

export class AsistenciaComponent implements OnInit {
  public token: string;

  constructor(
    private route: ActivatedRoute,
    private cookieService: CookieService,
  ){}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.token = params.token;
      this.cookieService.set(SESSION_OBJECT_ID, this.token);
    });
  }

}
