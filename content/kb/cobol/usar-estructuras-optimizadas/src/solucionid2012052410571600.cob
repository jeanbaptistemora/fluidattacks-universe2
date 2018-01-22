       IDENTIFICATION DIVISION.
      ******************
      * Identification *
      ******************
       PROGRAM-ID. COBOLCOPYB.

      ********
      * Data *
      ********
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       COPY QPHONE OF FLUID-QRPGSRC.

      ********
      * Main *
      ********
       PROCEDURE DIVISION.
       MAIN.
           MOVE "Apellido  Nombre    3001234982"
           TO PHONE-RECORD.

           DISPLAY "Nombre: " PHONE-FIRST-NAME.
           DISPLAY "Apellido: " PHONE-LAST-NAME.
           DISPLAY "Numero tel: " PHONE-NUMBER.

           STOP RUN.