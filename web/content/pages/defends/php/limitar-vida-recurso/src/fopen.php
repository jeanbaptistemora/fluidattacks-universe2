<?php
  $myresource = fopen("test.txt","r");

  while (!feof($myresource)) {
    $line = fgets($myresource);
    echo $line;
  }

  fclose($myresource);
