<?php
	function S2T($S_input){
	  $gb = iconv('UTF-8', 'GB2312', $S_input);
	  $big5 = iconv('GB2312', 'Big5//ignore', $gb);
	  $T = iconv('Big5//ignore', 'UTF-8', $big5);
	  return $T;
	}
	function getip(){
	if (!empty($_SERVER["HTTP_CLIENT_IP"])){
		$ip = $_SERVER["HTTP_CLIENT_IP"];
	}elseif(!empty($_SERVER["HTTP_X_FORWARDED_FOR"])){
		$ip = $_SERVER["HTTP_X_FORWARDED_FOR"];
	}else{
		$ip = $_SERVER["REMOTE_ADDR"];
	}
	return $ip;
}	
	echo getip();
	$a = '123.epub';
	shell_exec("echo '".getip()." Convert ".$a."\n'>>log");
	
	/*if($Strpos=strpos('123.php','.epub')>0){
		echo 'yes';
	}else{
		echo 'no';
	}
	
	$array = explode('.',$name2);
	echo count($array);
	echo $array[count($array)-1];
	
	$string = "Convert ../EPubFile/[渡航].我的青春戀愛喜劇果然有問題.6.75.epub to ../EPubFile/[渡航].我的青春戀愛喜劇果然有問題.6.75_tc.epub Sucessfully.";
	
	if($Strpos=strpos($string,'Sucessfully')>0){
		echo 'yes';
	}else{
		echo 'no';
	}*/
?>