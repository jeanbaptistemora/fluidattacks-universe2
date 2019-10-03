       IDENTIFICATION DIVISION.

       PROGRAM-ID. COBOLCPASS.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT COMMON-PASS ASSIGN TO "COMMONPASS"
           ORGANIZATION IS SEQUENTIAL.

       DATA DIVISION.

       FILE SECTION.
       FD COMMON-PASS.
       01 PASSWORD-RECORD.
           88 WS-PASS-EOF VALUE HIGH-VALUES.
           02 WS-PASSWORD PIC X(26).
       WORKING-STORAGE SECTION.
       01 WS-USERPASS     PIC X(26).
       01 WS-COUNT        PIC 9(02) VALUE 0.
       01 WS-LENGTH       PIC 9(02).
       01 WS-FLAG         PIC 9     VALUE 0.
           88 WS-FLAG-FALSE VALUE 0.
           88 WS-FLAG-TRUE  VALUE 1.

       PROCEDURE DIVISION.
       MAIN.
           DISPLAY "Ingrese clave a verificar: ".
           ACCEPT WS-USERPASS.
           MOVE FUNCTION UPPER-CASE(WS-USERPASS) TO WS-USERPASS.
           OPEN INPUT COMMON-PASS.
           READ COMMON-PASS
               AT END SET WS-PASS-EOF TO TRUE
           END-READ.
           PERFORM UNTIL WS-PASS-EOF
               MOVE FUNCTION UPPER-CASE(WS-PASSWORD) TO WS-PASSWORD
               MOVE 0 TO WS-COUNT
               MOVE 0 TO WS-LENGTH
               INSPECT FUNCTION REVERSE(WS-PASSWORD)
               TALLYING WS-LENGTH FOR LEADING SPACES

               COMPUTE WS-LENGTH = FUNCTION LENGTH(WS-PASSWORD)
                                   - WS-LENGTH
               INSPECT WS-USERPASS
               TALLYING WS-COUNT
               FOR ALL WS-PASSWORD(1:WS-LENGTH)
               IF WS-COUNT > 0 THEN
                   MOVE 1 TO WS-FLAG
                   PERFORM FINAL-PROCESS
               END-IF
               READ COMMON-PASS
                   AT END SET WS-PASS-EOF TO TRUE
               END-READ
           END-PERFORM
       FINAL-PROCESS.
           CLOSE COMMON-PASS
           IF WS-FLAG-FALSE THEN
               DISPLAY "Requisito cumplido"
           ELSE
               DISPLAY "Requisito no cumplido"
           END-IF.

           STOP RUN.
