<?php
	if(isset($_POST['submit_image']))
	{
	  $uploadfile=$_FILES["upload_file"]["tmp_name"];
	  $folder="images/";
	  move_uploaded_file($_FILES["upload_file"]["tmp_name"], $folder.$_FILES["upload_file"]["name"]);
	  echo $_FILES["upload_file"]["name"];
	  exit();
	}
?>