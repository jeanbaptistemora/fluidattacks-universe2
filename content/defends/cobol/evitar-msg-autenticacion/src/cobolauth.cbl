       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLAUTH.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 W01-USERNAME PIC X(16) VALUE "".
       01 W02-PASSWORD PIC X(16) VALUE "".
       01 W03-USERAPP  PIC X(16) VALUE "administrator".
       01 W04-PASSAPP  PIC X(16) VALUE "Admin_123456!".

       PROCEDURE DIVISION.
           DISPLAY "Username: ".
           ACCEPT W01-USERNAME.

           DISPLAY "Password: ".
           ACCEPT W02-PASSWORD.
           IF W01-USERNAME = W03-USERAPP THEN
               IF W02-PASSWORD = W04-PASSAPP THEN
                   DISPLAY "Combinacion valida"
               ELSE
                   DISPLAY "Combinacion no valida"
               END-IF
           ELSE
               DISPLAY "Combinacion no valida"
           END-IF.

           STOP RUN.
