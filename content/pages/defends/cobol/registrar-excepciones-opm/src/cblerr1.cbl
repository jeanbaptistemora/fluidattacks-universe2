       IDENTIFICATION DIVISION.
       PROGRAM-ID. CBLERR1.

       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 MISC.
           05 ERROR-HANDLER       PIC  X(20).
               06 OBJECT-NAME     PIC  X(10) VALUE "ERRHDL1".
               06 LIBRARY-NAME    PIC  X(10) VALUE "FLUID".
           05 SCOPE               PIC  X(01) VALUE "C".
           05 ERROR-HANDLER-LIB   PIC  X(10) VALUE "".
           05 PRIOR-ERROR-HANDLER PIC  X(20).

       01 NUMERIC-GROUP.
           05 X PIC 9(03).
           05 Y PIC S9(09) VALUE 0.

       01 WS-ERROR-HANDLER.
           02 BYTES-PROVIDED   PIC S9(009) BINARY.
           02 BYTES-AVAILABLE  PIC S9(009) BINARY.
           02 EXCEPTION-ID     PIC  X(007).
           02 RESERVED         PIC  X(001).
           02 EXCEPTION-DATA   PIC  X(240).

       PROCEDURE DIVISION.
       MAIN.
           MOVE 16 TO BYTES-PROVIDED OF WS-ERROR-HANDLER.
           CALL "QLRSETCE"
           USING ERROR-HANDLER OF MISC,
                 SCOPE OF MISC,
                 ERROR-HANDLER-LIB   OF MISC,
                 PRIOR-ERROR-HANDLER OF MISC,
                 WS-ERROR-HANDLER.
           IF BYTES-AVAILABLE OF WS-ERROR-HANDLER > 0
               DISPLAY "Error setting handler"
               STOP RUN
           END-IF.
           ADD X TO Y.

           STOP RUN.
