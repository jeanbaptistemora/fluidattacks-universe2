       IDENTIFICATION DIVISION.
      ******************
      * Identification *
      ******************
       PROGRAM-ID. COBOLCLSF.
      ***************
      * Environment *
      ***************
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT TEST-FILE ASSIGN TO 'TESTFILE'
           ORGANIZATION IS SEQUENTIAL.
      ********
      * Data *
      ********
       DATA DIVISION.

       FILE SECTION.
       FD TEST-FILE.
       01 TEST-FILE-RECORD PIC X(32).
      ********
      * Main *
      ********
       PROCEDURE DIVISION.
       MAIN.
           OPEN EXTEND TEST-FILE.
           MOVE "Hola mundo" TO TEST-FILE-RECORD.
           WRITE TEST-FILE-RECORD.
           CLOSE TEST-FILE.
           STOP RUN.