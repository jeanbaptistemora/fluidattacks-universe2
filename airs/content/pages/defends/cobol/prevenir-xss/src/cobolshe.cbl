       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLSHE.

       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 W01-INPUT     PIC X(064) VALUE "".
       01 W02-SANITIZED PIC X(384) VALUE "".
       01 W03-LENGTH    PIC 9(002) VALUE 0.
       01 W04-COUNT     PIC 9(002) VALUE 1.
       01 W05-CHAR      PIC X(001) VALUE "".
       01 W06-TEMP      PIC X(006) VALUE "".

       PROCEDURE DIVISION.
       MAIN.
           MOVE "<script>alert(document.cookie); </script>" TO W01-INPUT
           INSPECT FUNCTION REVERSE(W01-INPUT)
           TALLYING W03-LENGTH FOR LEADING SPACES.

           COMPUTE W03-LENGTH = FUNCTION LENGTH(W01-INPUT) - W03-LENGTH.
           PERFORM UNTIL W04-COUNT > W03-LENGTH
               MOVE W01-INPUT(W04-COUNT:1) TO W05-CHAR
               MOVE "" TO W06-TEMP
               EVALUATE W05-CHAR
                   WHEN """"  MOVE "&quot;" TO W06-TEMP
                   WHEN "'"   MOVE "&apos;" TO W06-TEMP
                   WHEN " "   MOVE "&nbsp;" TO W06-TEMP
                   WHEN "&"   MOVE "&amp;"  TO W06-TEMP
                   WHEN "<"   MOVE "&lt;"   TO W06-TEMP
                   WHEN ">"   MOVE "&gt;"   TO W06-TEMP
                   WHEN OTHER MOVE W05-CHAR TO W06-TEMP
               END-EVALUATE
               STRING W02-SANITIZED W06-TEMP
               DELIMITED BY SPACE
               INTO W02-SANITIZED
               COMPUTE W04-COUNT = W04-COUNT + 1
           END-PERFORM.
           DISPLAY W02-SANITIZED.

           STOP RUN.
