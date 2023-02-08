import { HttpHeaders } from "@angular/common/http";

export class AppComponent {
  login(login) {
    const headers = new HttpHeaders({
      "Content-Type": "application/json",
      "X-Frame-Options": "anything",
    });
  }
}
