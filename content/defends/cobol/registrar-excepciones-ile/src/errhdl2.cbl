       IDENTIFICATION DIVISION.
       PROGRAM-ID. ERRHDL2.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT LOG-FILE ASSIGN TO 'LOGGER'
           ORGANIZATION IS SEQUENTIAL
           FILE STATUS IS LOG-STATUS.

       DATA DIVISION.
       FILE SECTION.
       FD LOG-FILE.
       01 LOG-RECORD.
           05 LOG-DATE         PIC X(21).
           05 LOG-PGM-IN-ERROR PIC X(20).
           05 LOG-EXCEPTION-ID PIC X(10).
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
       01 ERR-MODULE-NAME      PIC  X(10).
       01 CBL-PGM-NAME         PIC X(256).
       WORKING-STORAGE SECTION.
       01 WS-CURRENT-DATE      PIC X(21).
       01 LOG-STATUS           PIC 99.

       PROCEDURE DIVISION USING CBL-EXCEPTION-ID,
                                VALID-RESPONSES,
                                PGM-IN-ERROR,
                                SYS-EXCEPTION-ID,
                                MESSAGE-LENGTH,
                                SYS-OPTION,
                                MESSAGE-TEXT,
                                ERR-MODULE-NAME,
                                CBL-PGM-NAME.
       MAIN.
           OPEN EXTEND LOG-FILE.
           MOVE FUNCTION CURRENT-DATE TO WS-CURRENT-DATE.
           MOVE WS-CURRENT-DATE  TO LOG-DATE.
           MOVE PGM-IN-ERROR     TO LOG-PGM-IN-ERROR.
           MOVE SYS-EXCEPTION-ID TO LOG-EXCEPTION-ID.
           WRITE LOG-RECORD.
           CLOSE LOG-FILE.
           MOVE "C" TO SYS-OPTION.
           STOP RUN.
