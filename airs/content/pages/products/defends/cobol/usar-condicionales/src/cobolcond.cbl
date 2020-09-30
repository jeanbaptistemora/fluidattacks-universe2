       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLCOND.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 PLANET.
           05 PLANET-NUMBER PIC 9(2) VALUE 3.
           05 PLANET-NAME   PIC X(8) VALUE "Tierra".

       PROCEDURE DIVISION.
       MAIN.
           DISPLAY PLANET-NUMBER, " - ", PLANET-NAME.

           PERFORM 3 TIMES
               COMPUTE PLANET-NUMBER = PLANET-NUMBER + 2
               EVALUATE PLANET-NUMBER
                   WHEN 1 MOVE "Mercurio" TO PLANET-NAME
                   WHEN 2 MOVE "Venus   " TO PLANET-NAME
                   WHEN 3 MOVE "Tierra  " TO PLANET-NAME
                   WHEN 4 MOVE "Marte   " TO PLANET-NAME
                   WHEN 5 MOVE "Jupiter " TO PLANET-NAME
                   WHEN 6 MOVE "Saturno " TO PLANET-NAME
                   WHEN 7 MOVE "Urano   " TO PLANET-NAME
                   WHEN 8 MOVE "Neptuno " TO PLANET-NAME
                   WHEN OTHER MOVE "Invalido" TO PLANET-NAME
               END-EVALUATE

               DISPLAY PLANET-NUMBER, " - ", PLANET-NAME
           END-PERFORM.
           DISPLAY "Ingrese un numero de planeta".
           ACCEPT PLANET-NUMBER.
           IF PLANET-NUMBER IS >= 1 AND PLANET-NUMBER IS <= 8
               IF PLANET-NUMBER IS < 5
                   DISPLAY "Planeta interior"
               ELSE
                   DISPLAY "Planeta exterior"
               END-IF
           ELSE
               DISPLAY "Tipo de planeta desconocido"
           END-IF

           STOP RUN.
