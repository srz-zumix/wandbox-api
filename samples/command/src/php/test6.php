<?php

print("Test6\n");

set_include_path('lib');
set_include_path(get_include_path() . PATH_SEPARATOR . 'lib2');
set_include_path(get_include_path() . PATH_SEPARATOR . PATH_SEPARATOR . ';lib3' . PATH_SEPARATOR . ':lib3');
set_include_path(get_include_path() . PATH_SEPARATOR . 'lib3' . '/subdir');

include 'test7.php';
include 'test8.php';
include 'test9.php';
include 'test10.php';

ini_set('include_path', 'lib4');

include 'test11.php';

?>
