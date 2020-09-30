       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLCLSC.

       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 WS-USERNAME PIC X(64) VALUE "".

       COPY SQLCA OF QSYSINC-QCBLLESRC.

       PROCEDURE DIVISION.
       MAIN.
           EXEC SQL
               DECLARE C1 CURSOR FOR
               SELECT usuario
               FROM SQLTEST
           END-EXEC.
           EXEC SQL
               OPEN C1
           END-EXEC.

           EXEC SQL
               FETCH C1 INTO :WS-USERNAME
           END-EXEC.
           DISPLAY "Nombre de usuario: " WS-USERNAME
           EXEC SQL
               CLOSE C1
           END-EXEC.
           STOP RUN.
