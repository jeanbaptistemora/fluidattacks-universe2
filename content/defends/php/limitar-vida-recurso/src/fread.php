$myfile = fopen("test.txt","r");
$content = fread($myfile, filesize($myfile));
fclose($myfile);
print $content;