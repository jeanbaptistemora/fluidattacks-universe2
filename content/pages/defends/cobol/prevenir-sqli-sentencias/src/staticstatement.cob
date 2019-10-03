       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLSQL.

       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 W01-USERNAME PIC X(64) VALUE "".
       01 W02-PASSWORD PIC X(64) VALUE "".

       COPY SQLCA OF QSYSINC-QCBLLESRC.

       PROCEDURE DIVISION.
       MAIN.
           DISPLAY "Username: ".
           ACCEPT W01-USERNAME.

           EXEC SQL
               DECLARE C1 CURSOR FOR
               SELECT contrasenia
               FROM SQLTEST
               WHERE usuario = :W01-USERNAME
           END-EXEC.

           EXEC SQL
               OPEN C1
           END-EXEC.

           EXEC SQL
               FETCH C1 INTO :W02-PASSWORD
           END-EXEC.

           PERFORM UNTIL SQLCODE NOT = 0
               DISPLAY "Resultado: " W02-PASSWORD

               EXEC SQL
                   FETCH C1 INTO :W02-PASSWORD
               END-EXEC
           END-PERFORM.

           EXEC SQL
               CLOSE C1
           END-EXEC.

           STOP RUN.
