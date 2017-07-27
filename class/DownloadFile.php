<?php
session_start();
	$GET_token = $_GET['token'];
	$token = $_SESSION['token'];
	$EPubDownloadName = urldecode($_GET["EPubDownloadName"]);
	$path = "../EPubFile/";
	if($token==$GET_token && $EPubDownloadName!=null){
		header("Pragma: public");
		header("Expires: 0");
		header("Cache-Control: must-revalidate, post-check=0, pre-check=0");
		header("Cache-Control: private",false);
		header("Content-Type: application/octet-stream");
		header("Content-Disposition: attachment; filename=".basename('"'.$EPubDownloadName.'"'));
		header("Content-Transfer-Encoding: binary");
		$fd = fopen($path.$EPubDownloadName, "rb");  //大檔案下載的解決方法～readfile($file)會出問題～
		if($fd){
			ob_end_clean();
			fpassthru($fd);
		}
		fclose($fd);
		sleep(3);
		unset($_SESSION['token']);
		unlink($path.$EPubDownloadName);
	}else{
		header("Location: ../?Error=DownloadTimeOut#upload");
	}
	
?>