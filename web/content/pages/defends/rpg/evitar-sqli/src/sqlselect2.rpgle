  D sqlnombre       S             20A   INZ('fsg'' OR 1=1--')

  D sqlcommand      S            256A   INZ('SELECT nombre, edad +
  D                                          FROM FLUID/ESTUDIANTES +
  D                                          WHERE nombre = ? ')
  D                                     VARYING

  D datastructure   DS
  D  nombre                       30A   VARYING
  D  edad                         10S 0

  C/exec sql
  C+   SET OPTION
  C+   COMMIT = *NONE,
  C+   CLOSQLCSR = *ENDMOD
  C/end-exec

  C/exec sql
  C+ PREPARE SQLSTATEMENT FROM :sqlcommand
  C/end-exec

  C/exec sql
  C+ DECLARE CURSORSQL CURSOR FOR SQLSTATEMENT
  C/end-exec

  C/exec sql
  C+ OPEN CURSORSQL USING :sqlnombre
  C/end-exec

  C/exec sql
  C+ FETCH NEXT FROM CURSORSQL INTO :datastructure
  C/end-exec

  C                   DOW       SQLSTT = '00000'
  C     datastructure DSPLY

  C/exec sql
  C+ FETCH NEXT FROM CURSORSQL INTO :datastructure
  C/end-exec

  C                   ENDDO

  C                   RETURN
