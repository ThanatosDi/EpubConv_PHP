<?php
/*Convert file name from Simplified Chinese to Traditional Chinese*/
	function S2T($S_input){
		$T = shell_exec("echo {$S_input}| opencc -c zhs2zhtw_vp.ini");
		$T = substr($T,0,-1);
		return $T;
	}
	
	if ($_FILES["EPubFile"]["error"] > 0){
		$FileError = $_FILES["EPubFile"]["error"];
		echo "Error: " . $FileError;
		//header("Location: ../?Error=UploadError#upload");
	}else{
		$EPubFileName = S2T(urldecode($_FILES["EPubFile"]["name"]));
		//echo "檔案名稱: " . $EPubFileName."<br/>";
		
		if(strpos($EPubFileName,'.epub')>0){
			if (file_exists("../epubfiles/" . $EPubFileName)){
				unlink("../epubfiles/" . $EPubFileName);
			}
			move_uploaded_file($_FILES["EPubFile"]["tmp_name"],"../epubfiles/".$EPubFileName);
			echo "
					<form id=\"conv\" action=\"../conv.php\" class=\"form-horizontal\" method=\"POST\">
							<input type=\"hidden\" name=\"FileName\" id=\"FileName\" value={$EPubFileName} />
						</form>
						<script>
							conv.submit();
						</script>
						";
		}else{
			echo "
					<form id=\"POST\" action=\"../index.html#upload\" class=\"form-horizontal\" method=\"POST\">
							<input type=\"hidden\" name=\"Messages\" id=\"Messages\" value=\"TypeError\" />
						</form>
						<script>
							POST.submit();
						</script>
						";
		}
	}
?>