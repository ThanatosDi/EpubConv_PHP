<?php
$ReCaptchaResponse=filter_input(INPUT_POST, 'reCaptchaResponse');
$secretkey = "6LcceVIUAAAAAAFteSEnV0XBO1DwVpIvt1A6CAFQ";
$Response=file_get_contents('https://www.google.com/recaptcha/api/siteverify?secret='.$secretkey.'"&response='.$ReCaptchaResponse."&remoteip=".$_SERVER['REMOTE_ADDR']);
echo ($Response)?'OK':'ERROR';
?>