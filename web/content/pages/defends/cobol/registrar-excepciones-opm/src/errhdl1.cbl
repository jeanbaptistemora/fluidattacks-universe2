       IDENTIFICATION DIVISION.
       PROGRAM-ID. ERRHDL1.

       DATA DIVISION.

       WORKING-STORAGE SECTION.
       01 MISC.
           05 LOG-EXCEPTION-ID PIC  X(12).
           05 MESSAGE-KEY      PIC  X(04).
           05 POINT-OF-FAILURE PIC S9(09) BINARY VALUE 1.
           05 PRINT-JOBLOG     PIC  X(01) VALUE "Y".
           05 NBR-OF-ENTRIES   PIC S9(09) BINARY.
           05 NBR-OF-OBJECTS   PIC S9(09) BINARY VALUE 1.

       01 MESSAGE-INFO.
           05 MSG-OFFSET       PIC S9(09) BINARY.
           05 MSG-LENGTH       PIC S9(09) BINARY.

       01 OBJECT-LIST.
           05 OBJECT-NAME      PIC  X(30).
           05 LIBRARY-NAME     PIC  X(30).
           05 OBJECT-TYPE      PIC  X(10) VALUE "*PGM      ".

       01 WS-ERROR-HANDLER.
           02 BYTES-PROVIDED   PIC S9(009) BINARY.
           02 BYTES-AVAILABLE  PIC S9(009) BINARY.
           02 EXCEPTION-ID     PIC  X(007).
           02 RESERVED         PIC  X(001).
           02 EXCEPTION-DATA   PIC  X(240).
       LINKAGE SECTION.
       01 CBL-EXCEPTION-ID     PIC  X(07).
       01 VALID-RESPONSES      PIC  X(06).
       01 PGM-IN-ERROR.
           05 PGM-NAME         PIC  X(10).
           05 LIB-NAME         PIC  X(10).
       01 SYS-EXCEPTION-ID     PIC  X(07).
       01 MESSAGE-TEXT         PIC  X(01).
       01 MESSAGE-LENGTH       PIC S9(09) BINARY.
       01 SYS-OPTION           PIC  X(01).

       PROCEDURE DIVISION USING CBL-EXCEPTION-ID,
                                VALID-RESPONSES,
                                PGM-IN-ERROR,
                                SYS-EXCEPTION-ID,
                                MESSAGE-TEXT,
                                MESSAGE-LENGTH,
                                SYS-OPTION.

       MAIN.
           MOVE 16 TO BYTES-PROVIDED OF WS-ERROR-HANDLER.
           MOVE SYS-EXCEPTION-ID TO LOG-EXCEPTION-ID.
           IF MESSAGE-LENGTH > 0
               MOVE 1 TO MSG-OFFSET,
               MOVE MESSAGE-LENGTH TO MSG-LENGTH,
               MOVE 1 TO NBR-OF-ENTRIES,
           ELSE
               MOVE 0 TO MSG-OFFSET,
               MOVE 0 TO MSG-LENGTH,
               MOVE 0 TO NBR-OF-ENTRIES
           END-IF.
           MOVE PGM-NAME TO OBJECT-NAME.
           MOVE LIB-NAME TO LIBRARY-NAME.
           CALL "QPDLOGER" USING PGM-NAME,
                                 LOG-EXCEPTION-ID,
                                 MESSAGE-KEY,
                                 POINT-OF-FAILURE,
                                 PRINT-JOBLOG,
                                 MESSAGE-TEXT,
                                 MESSAGE-INFO,
                                 NBR-OF-ENTRIES,
                                 OBJECT-LIST,
                                 NBR-OF-OBJECTS,
                                 WS-ERROR-HANDLER.
           IF BYTES-AVAILABLE OF WS-ERROR-HANDLER > 0
               DISPLAY "Error en el llamado a la interfaz QPDLOGER"
           END-IF.
           MOVE "C" TO SYS-OPTION.
           STOP RUN.
