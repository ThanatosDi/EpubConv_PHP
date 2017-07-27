<?php
session_start();

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
	
	$EPubName = $_GET['EPubName'];
	$token = $_SESSION['token'];
	$GET_token = $_GET['token'];
	if($token==$GET_token){
		$output = shell_exec('../convert2tex/epubs2t.py "../EPubFile/'.$EPubName.'"');
		if(strpos($output,'Sucessfully')>0){
			$Strpos=strpos($EPubName,'.epub');
			$EPubDownloadName = substr_replace($EPubName, '_tc', $Strpos, 0);
			header("Location: ../?EPubName=$EPubDownloadName&Sucessfully=$token#StartDownload");
			unlink('../EPubFile/'.$EPubName);
		}else{
			header("Location: ../?Error=FileConvFile#upload");
		}
	}else{
		header("Location: ../?Error=DownloadTimeOut#upload");
	}
?>