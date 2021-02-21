<?php
// This file is a "Hello, world!" in PHP for wandbox.
print("Hello, Wandbox!\n");

include 'test1.php';
require "test2.php";
include_once "subdir/test3.php";
require_once "subdir/test4.php";

$test5 = include "test5.php";
print($test5);

include('test6.php');


// PHP references:
//   http://php.net
