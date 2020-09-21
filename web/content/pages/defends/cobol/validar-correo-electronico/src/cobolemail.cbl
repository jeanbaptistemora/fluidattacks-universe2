       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLEMAIL.

       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 W01-EMAIL      PIC X(256) VALUE "".
       01 W02-VALIDEMAIL PIC X(256) VALUE "".
       01 W03-COUNT      PIC 9(002) VALUE 0.
       01 W04-EMAIL
           02 W04-USERNAME PIC X(64).
           02 W04-DOMAIN   PIC X(255).

       PROCEDURE DIVISION.
       MAIN.
           ACCEPT W01-EMAIL.
           INSPECT W01-EMAIL
           TALLYING W03-COUNT
           FOR ALL "@".
           IF W03-COUNT > 0 THEN
               MOVE 0 TO W03-COUNT
               UNSTRING W01-EMAIL
               DELIMITED BY "@"
               INTO W04-USERNAME W04-DOMAIN
               INSPECT W04-USERNAME
               TALLYING W03-COUNT
               FOR CHARACTERS
               BEFORE INITIAL SPACE
               IF W03-COUNT > 0 THEN
                   MOVE 0 TO W03-COUNT
                   INSPECT W04-DOMAIN
                   TALLYING W03-COUNT
                   FOR CHARACTERS
                   BEFORE INITIAL SPACE
                   IF W03-COUNT > 0 THEN
                       UNSTRING W04-USERNAME
                       DELIMITED BY "+"
                       INTO W02-VALIDEMAIL
                       STRING W02-VALIDEMAIL "@" W04-DOMAIN
                       DELIMITED BY SPACE
                       INTO W02-VALIDEMAIL
                       DISPLAY W02-VALIDEMAIL
                   ELSE
                       PERFORM EMAIL-ERROR
                   END-IF
               ELSE
                   PERFORM EMAIL-ERROR
               END-IF
           ELSE
               PERFORM EMAIL-ERROR
           END-IF.

           STOP RUN.
