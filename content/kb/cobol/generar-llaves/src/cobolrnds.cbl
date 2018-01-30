       PROCESS NOMONOPRC.
       IDENTIFICATION DIVISION.
      ******************
      * Identification *
      ******************
       PROGRAM-ID. COBOLRNDS.
      ***************
      * Environment *
      ***************
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
         SOURCE-COMPUTER. IBM-ISERIES.
         OBJECT-COMPUTER. IBM-ISERIES.
         SPECIAL-NAMES.
         LINKAGE TYPE PROCEDURE FOR "Qc3GenPRNs".
      ********
      * Data *
      ********
       DATA DIVISION.

       WORKING-STORAGE SECTION.
       COPY QC3CCI OF QSYSINC-QCBLLESRC.
       COPY QUSEC OF QSYSINC-QCBLLESRC.
       01 WS-RAND-BYTES PIC X(32).
      ********
      * Main *
      ********
       PROCEDURE DIVISION.
       MAIN.
           CALL "Qc3GenPRNs" USING
               BY REFERENCE WS-RAND-BYTES,
               BY CONTENT   LENGTH OF WS-RAND-BYTES,
               BY CONTENT   "0",
               BY CONTENT   "0",
               BY REFERENCE QUS-EC.
           DISPLAY "Random: " WS-RAND-BYTES.

           STOP RUN.