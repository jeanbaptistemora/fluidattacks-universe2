       IDENTIFICATION DIVISION.
      ******************
      * Identification *
      ******************
       PROGRAM-ID. COBOLDBG.
      ***************
      * Environment *
      ***************
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-ISERIES WITH DEBUGGING MODE.
      ********
      * Data *
      ********
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 RESULTADO  PIC 9(04) VALUE 1.
       01 CONTADOR   PIC 9(02).
      ********
      * Main *
      ********
       PROCEDURE DIVISION.
       MAIN.
           PERFORM VARYING CONTADOR FROM 1 BY 1 UNTIL CONTADOR > 10
      D        DISPLAY "Actual: " RESULTADO
               COMPUTE RESULTADO = RESULTADO * 2
           END-PERFORM.
           DISPLAY "Resultado: " RESULTADO.

           STOP RUN.
