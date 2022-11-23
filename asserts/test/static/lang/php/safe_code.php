<?php
/* avoid using 0xA0 (\240) in ereg ranges. RH73 does not like that */
if ( ! preg_match( "/[\200-\237]/", $string ) and ! preg_match( "/[\241-\377]/", $string ) )
        return $string;
?>
