       IDENTIFICATION DIVISION.
      ******************
      * Identification *
      ******************
       PROGRAM-ID. COBOLPASS.

      ********
      * Data *
      ********
       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 W01-USERNAME PIC X(20).
       01 W02-PASSWORD PIC X(20).

      ********
      * Main *
      ********
       PROCEDURE DIVISION.
       MAIN.
           DISPLAY "Username: ".
           ACCEPT W01-USERNAME.

           DISPLAY "Password: ".
           ACCEPT W02-PASSWORD WITH NO-ECHO.

           STOP RUN.