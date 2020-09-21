       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLSQL.

       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 W01-USERNAME PIC X(64) VALUE "".
       01 W02-PASSWORD PIC X(64) VALUE "".
       01 W03-SQLCMD   PIC X(128) VALUE "".

       COPY SQLCA OF QSYSINC-QCBLLESRC.

       PROCEDURE DIVISION.
       MAIN.
           DISPLAY "Username: ".
           ACCEPT W01-USERNAME.

           STRING "SELECT contrasenia" SPACE
                  "FROM SQLTEST" SPACE
                  "WHERE usuario = """ W01-USERNAME """"
                  DELIMITED BY SIZE
                  INTO W03-SQLCMD.

           EXEC SQL
               DECLARE STMT STATEMENT
           END-EXEC

           EXEC SQL
               PREPARE STMT FROM :W03-SQLCMD
           END-EXEC

           EXEC SQL
               DECLARE C1 CURSOR FOR STMT
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
