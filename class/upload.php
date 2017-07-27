<?php
session_start();
	$token_post = @$_POST['token'];
	$_SESSION['token'] = $token_post;
	$token = $_SESSION['token'];
/*Convert file name from Simplified Chinese to Traditional Chinese*/
	function S2T($S_input){
		$gb2312 = iconv('UTF-8', 'GB2312', $S_input);
		$big5 = iconv('GB2312', 'Big5//ignore', $gb2312);
		$T = iconv('Big5//ignore', 'UTF-8', $big5);
		return $T;
	}

	if ($_FILES["EPubFile"]["error"] > 0||$token==null){
		$FileError = $_FILES["EPubFile"]["error"];
		echo "Error: " . $FileError;
		header("Location: ../?Error=UploadError#upload");
	}else{
		$EPubFileName = S2T(urldecode($_FILES["EPubFile"]["name"]));
		echo "檔案名稱: " . $EPubFileName."<br/>";
		
		if(strpos($EPubFileName,'.epub')>0){
			if (file_exists("../EPubFile/" . $EPubFileName)){
				header("Location: ../?Error=DoubleFile#upload");
			}else{
				move_uploaded_file($_FILES["EPubFile"]["tmp_name"],"../EPubFile/".$EPubFileName);
				header("Location: conv.php?token=$token&EPubName=$EPubFileName");
			}
		}else{
			$array = explode('.',$EPubFileName);
			$ErrorType = $array[count($array)-1];
			header("Location: ../?Error=TypeError&ErrorFileType=$ErrorType#upload");
		}
	}
?>