       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLINPUT.

       ENVIRONMENT DIVISION.
       SPECIAL-NAMES.
           CLASS WS-VALID-CHARSET IS
               'A' THRU 'D'
               'x' THRU 'z'
               'S' 'T' '9' ' '.

       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 W01-INPUT PIC X(10).

       PROCEDURE DIVISION.
       MAIN.
           ACCEPT W01-INPUT.
           IF W01-INPUT IS NUMERIC
               DISPLAY "Numeric"
           ELSE
               DISPLAY "Not numeric"
           END-IF.
           IF W01-INPUT IS ALPHABETIC
               DISPLAY "Alphabetic"
           ELSE
               DISPLAY "Not alphabetic"
           END-IF.
           IF W01-INPUT IS ALPHABETIC-LOWER
               DISPLAY "Alphabetic lower"
           ELSE
               DISPLAY "Not alphabetic lower"
           END-IF.
           IF W01-INPUT IS ALPHABETIC-UPPER
               DISPLAY "Alphabetic upper"
           ELSE
               DISPLAY "Not alphabetic upper"
           END-IF.
           IF W01-INPUT IS WS-VALID-CHARSET
               DISPLAY "Charset valid"
           ELSE
               DISPLAY "Charset not valid"
           END-IF.

           STOP RUN.
