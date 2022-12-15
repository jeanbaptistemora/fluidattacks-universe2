  import { Component, OnInit } from '@angular/core';
  import { ActivatedRoute, Router } from '@angular/router';
  import { JwtHelperService } from '@auth0/angular-jwt';
  import { ICliente } from '@nautilus/nautilus-commerce';
  import { CookieService } from 'ngx-cookie-service';
  import { AuthService } from '../service/auth.service';

  export const SESSION_OBJECT_ID: string = 'OficinaSession';

  @Component({
    selector: 'app-asistencia',
    templateUrl: './asistencia.component.html'
  })

  export class AsistenciaComponent implements OnInit {
    public token: string;

    constructor(
      private route: ActivatedRoute,
      private authService: AuthService,
      private cookieService: CookieService,
      private router: Router) {

    }

    ngOnInit(): void {
      this.route.params.subscribe(params => {
        this.token = params.token;
        try {
          const jwtHelper = new JwtHelperService();
          const decondeToken: any = jwtHelper.decodeToken(this.token);
          // se valida si el token no ha expirado
          if (jwtHelper.isTokenExpired(this.token)) {
            throw new Error("token expirado");
          }
          // valida si el cliente viene en el token
          if (decondeToken.cliente) {
            const cliente: ICliente = JSON.parse(decondeToken.cliente);
            this.cookieService.set(SESSION_OBJECT_ID, this.token);
            this.authService.setCurrentUser(cliente);
            this.router.navigate(['main'], { replaceUrl: true });
          } else {
            this.router.navigate(['login'], { replaceUrl: true });
          }
        } catch (error) {
          this.router.navigate(['login'], { replaceUrl: true });
        }

      });


    }

  }
