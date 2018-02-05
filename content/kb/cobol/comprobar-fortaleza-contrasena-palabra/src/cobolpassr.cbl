       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLPASSR.

       ENVIRONMENT DIVISION.

       SPECIAL-NAMES.
           CLASS WS-SPECIAL IS
                   ' ' THRU '/'
                   ':' THRU '@'
                   '[' THRU '`'.

       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 W01-PASSWORD PIC X(64) VALUE "".
       01 W02-COUNT    PIC 9(02) VALUE 1.
       01 W03-LENGTH   PIC 9(02) VALUE 0.
       01 W04-CHAR     PIC X     VALUE "".
       01 W05-UCOUNT   PIC 9(02) VALUE 0.
       01 W06-LCOUNT   PIC 9(02) VALUE 0.
       01 W07-NCOUNT   PIC 9(02) VALUE 0.
       01 W08-SCOUNT   PIC 9(02) VALUE 0.
       01 W09-FLAG     PIC 9     VALUE 1.
           88 W09-FLAG-FALSE VALUE 0.
           88 W09-FLAG-TRUE  VALUE 1.

       PROCEDURE DIVISION.
       MAIN.
           ACCEPT W01-PASSWORD.
           INSPECT FUNCTION REVERSE(W01-PASSWORD)
                   TALLYING W03-LENGTH FOR LEADING SPACES.
           COMPUTE W03-LENGTH = FUNCTION LENGTH(W01-PASSWORD)
                                - W03-LENGTH.
           IF W03-LENGTH < 8 THEN
               MOVE 0 TO W09-FLAG
           END-IF.
           IF W09-FLAG-TRUE
               PERFORM UNTIL W02-COUNT > W03-LENGTH
                   MOVE W01-PASSWORD(W02-COUNT:1) TO W04-CHAR
                   IF W04-CHAR IS ALPHABETIC-UPPER
                       COMPUTE W05-UCOUNT = W05-UCOUNT + 1
                   ELSE
                       IF W04-CHAR IS ALPHABETIC-LOWER
                           COMPUTE W06-LCOUNT = W06-LCOUNT + 1
                       ELSE
                           IF W04-CHAR IS NUMERIC
                               COMPUTE W07-NCOUNT = W07-NCOUNT + 1
                           ELSE
                               IF W04-CHAR IS WS-SPECIAL
                                   COMPUTE W08-SCOUNT = W08-SCOUNT + 1
                               END-IF
                           END-IF
                       END-IF
                   END-IF
                   COMPUTE W02-COUNT = W02-COUNT + 1
               END-PERFORM
           END-IF.
           IF W05-UCOUNT = 0 OR W06-LCOUNT = 0 OR
              W07-NCOUNT = 0 OR W08-SCOUNT = 0
               MOVE 0 TO W09-FLAG
           END-IF.
           IF W09-FLAG-TRUE
               DISPLAY "Requisito cumplido"
           ELSE
               DISPLAY "Requisito incumplido"
           END-IF.

           STOP RUN.