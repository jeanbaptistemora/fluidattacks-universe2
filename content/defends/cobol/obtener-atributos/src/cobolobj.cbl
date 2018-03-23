       IDENTIFICATION DIVISION.
       PROGRAM-ID. COBOLOBJ.

       DATA DIVISION.

       WORKING-STORAGE SECTION.
      * Qualified object name = "OBJECT    " + "LIBRARY   "
       01 REQUIRED-PARAMETER.
           02 R-RECEIVER-LENGTH PIC S9(9) BINARY VALUE 653.
           02 R-FORMAT-NAME     PIC X(08) VALUE "OBJD0400".
           02 R-QOBJECT-NAME.
              03 R-OBJECT-NAME  PIC X(10) VALUE "".
              03 R-LIBRARY-NAME PIC X(10) VALUE "".
           02 R-OBJECT-TYPE     PIC X(10) VALUE "".

       01 OPTIONAL-PARAMETER.
           02 O-BYTES-PROVIDED   PIC S9(9) BINARY VALUE 256.
           02 O-BYTES-AVAILABLE  PIC S9(9) BINARY VALUE 0.
           02 O-EXCEPTION-ID     PIC X(08).
           02 O-RESERVED         PIC X(01).
           02 O-EXCEPTION-DATA   PIC X(240).
       COPY QUSROBJD OF QSYSINC-QCBLLESRC.

       PROCEDURE DIVISION.
       MAIN.
           DISPLAY "Nombre del objeto: ".
           ACCEPT R-OBJECT-NAME.

           DISPLAY "Tipo del objeto (*FILE, *SRC, etc): ".
           ACCEPT R-OBJECT-TYPE.

           DISPLAY "Nombre de la bilbioteca: ".
           ACCEPT R-LIBRARY-NAME.
           CALL "QUSROBJD" USING
               QUS-OBJD0400
               R-RECEIVER-LENGTH
               R-FORMAT-NAME
               R-OBJECT-NAME
               R-OBJECT-TYPE
               OPTIONAL-PARAMETER.
           IF O-BYTES-AVAILABLE = 0 THEN
               IF OBJECT-SIZE < 100000 THEN
                   DISPLAY "Tamanio del objeto: " OBJECT-SIZE
               ELSE
                   DISPLAY "Tamanio del objeto no es valido"
               END-IF

               IF DIGITALLY-SIGNED NOT = 0 THEN
                   DISPLAY "Objeto firmado digitalmente"
               ELSE
                   DISPLAY "Objeto no firmado digitalmente"
               END-IF
           ELSE
               DISPLAY "Ha ocurrido un error: " O-EXCEPTION-ID
           END-IF.

           STOP RUN.
