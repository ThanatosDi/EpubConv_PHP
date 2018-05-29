<?php
	$EPubDownloadName = ($_GET["f"]);
	$path = "../epubfiles/";
	if($EPubDownloadName!=null && file_exists($path.$EPubDownloadName)){
		header("Content-type:application");
		header("Content-Length: " .(string)(filesize($path.$EPubDownloadName)));
		header("Content-Disposition: attachment; filename=".$EPubDownloadName);
		readfile($path.$EPubDownloadName);
		unlink($path.$EPubDownloadName);
	}else{
		echo "<form id=\"POST\" action=\"../index.html#StartDownload\" class=\"form-horizontal\" method=\"POST\">
							<input type=\"hidden\" name=\"Messages\" id=\"Messages\" value=\"FileNotFound\" />
						</form>
						<script>
							POST.submit();
						</script>";
	}
	
?>