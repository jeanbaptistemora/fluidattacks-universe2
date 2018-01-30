       IDENTIFICATION DIVISION.
      ******************
      * Identification *
      ******************
       PROGRAM-ID. COBOLRAND.
      ********
      * Data *
      ********
       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 W01-RANDOM PIC S9V9(10).
       01 W02-CURRENT-DATE-DATA.
           05 W02-CURRENT-DATE.
               10 W02-CURRENT-YEAR   PIC 9(04).
               10 W02-CURRENT-MONTH  PIC 9(02).
               10 W02-CURRENT-DAY    PIC 9(02).
           05 W02-CURRENT-TIME.
               10 W02-CURRENT-HOURS  PIC 9(02).
               10 W02-CURRENT-MINUTE PIC 9(02).
               10 W02-CURRENT-SECOND PIC 9(02).
               10 W02-CURRENT-MILLIS PIC 9(02).
           05 W02-DIFF-FROM-GMT PIC X(05).
       01 W03-IDAY PIC 9(12).
       01 W04-SVAL PIC 9(12).
      ********
      * Main *
      ********
       PROCEDURE DIVISION.
       MAIN.
           MOVE FUNCTION CURRENT-DATE TO W02-CURRENT-DATE-DATA.
           COMPUTE W03-IDAY = 365 * (W02-CURRENT-YEAR - 1970).
           EVALUATE W02-CURRENT-MONTH
               WHEN 1  COMPUTE W03-IDAY = W03-IDAY + 0
               WHEN 2  COMPUTE W03-IDAY = W03-IDAY + 31
               WHEN 3  COMPUTE W03-IDAY = W03-IDAY + 59
               WHEN 4  COMPUTE W03-IDAY = W03-IDAY + 90
               WHEN 5  COMPUTE W03-IDAY = W03-IDAY + 120
               WHEN 6  COMPUTE W03-IDAY = W03-IDAY + 151
               WHEN 7  COMPUTE W03-IDAY = W03-IDAY + 181
               WHEN 8  COMPUTE W03-IDAY = W03-IDAY + 212
               WHEN 9  COMPUTE W03-IDAY = W03-IDAY + 243
               WHEN 10 COMPUTE W03-IDAY = W03-IDAY + 273
               WHEN 11 COMPUTE W03-IDAY = W03-IDAY + 304
               WHEN 12 COMPUTE W03-IDAY = W03-IDAY + 365
               WHEN OTHER COMPUTE W03-IDAY = W03-IDAY + 0
           END-EVALUATE.
           COMPUTE W03-IDAY = W03-IDAY + (W02-CURRENT-DAY - 1).
           COMPUTE W04-SVAL = W02-CURRENT-SECOND +
                             (60 * W02-CURRENT-MINUTE) +
                             (3600 * (W02-CURRENT-HOURS + (24 * W03-IDAY))).
           COMPUTE W01-RANDOM = FUNCTION RANDOM(W04-SVAL).
           
           DISPLAY "Numero aleatorio: " W01-RANDOM.
        
           STOP RUN.