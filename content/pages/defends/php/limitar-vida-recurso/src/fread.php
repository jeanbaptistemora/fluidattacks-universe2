<?php
  $myfile = fopen("test.txt","r");
  $content = fread($myfile, filesize("test.txt"));
  fclose($myfile);
  print $content;
