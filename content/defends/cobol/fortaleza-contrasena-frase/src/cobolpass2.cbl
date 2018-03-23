       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLPASS2.
       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 W01-PASSWORD PIC X(64) VALUE "".
       01 W02-COUNT    PIC 9(02) VALUE 1.
       01 W03-LENGTH   PIC 9(02) VALUE 0.
       01 W04-CHAR     PIC X     VALUE "".
       01 W05-PNUMBER  PIC 9(02) VALUE 0.
       01 W06-FLAG     PIC 9     VALUE 0.
           88 W06-FLAG-FALSE VALUE 0.
           88 W06-FLAG-TRUE  VALUE 1.

       PROCEDURE DIVISION.
       MAIN.
           ACCEPT W01-PASSWORD.
           COMPUTE W03-LENGTH = FUNCTION LENGTH(W01-PASSWORD).
           PERFORM UNTIL W02-COUNT > W03-LENGTH
               MOVE W01-PASSWORD(W02-COUNT:1) TO W04-CHAR
               IF W04-CHAR = SPACE
                   IF W06-FLAG-TRUE
                       MOVE 0 TO W06-FLAG
                   END-IF
               ELSE
                   IF W06-FLAG-FALSE
                       COMPUTE W05-PNUMBER = W05-PNUMBER + 1
                       MOVE 1 TO W06-FLAG
                   END-IF
               END-IF
               COMPUTE W02-COUNT = W02-COUNT + 1
           END-PERFORM.
           IF W05-PNUMBER < 3
               DISPLAY "Requisito incumplido"
           ELSE
               DISPLAY "Requisito cumplido"
           END-IF.

           STOP RUN.
