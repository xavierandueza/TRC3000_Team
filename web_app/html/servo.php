<?php

	$img = "";
	$warning_message = "";
	if (isset($_POST['b1'])){
		
		// Get tilt using script
		shell_exec('python3 MPU.py');
		$file = fopen("angle_x.txt","r");
		$tilt_x = fread($file, filesize("angle_x.txt"));
		fclose($file);
		$file = fopen("angle_y.txt","r");
		$tilt_y = fread($file, filesize("angle_y.txt"));
		fclose($file);
		$tilt_inbound = ($tilt_x <15 and $tilt_x >-15) and ($tilt_y <15 and $tilt_y >-15);
			if ($tilt_inbound){
				$warning_message = "";
				shell_exec('python3 Servo_0.py');
			} else {
				$warning_message = "Platform is too tilted!";
			}
			
		}
	if (isset($_POST['b2'])){
					// Get tilt using script
		shell_exec('python3 MPU.py');
		$file = fopen("angle_x.txt","r");
		$tilt_x = fread($file, filesize("angle_x.txt"));
		fclose($file);
		$file = fopen("angle_y.txt","r");
		$tilt_y = fread($file, filesize("angle_y.txt"));
		fclose($file);
		$tilt_inbound = ($tilt_x <15 and $tilt_x >-15) and ($tilt_y <15 and $tilt_y >-15);
			if ($tilt_inbound){
				$warning_message = "";
				shell_exec('python3 Servo_45.py');
			} else {
				$warning_message = "Platform is too tilted!";
			}
		}
	if (isset($_POST['b3'])){
					// Get tilt using script
		shell_exec('python3 MPU.py');
		$file = fopen("angle_x.txt","r");
		$tilt_x = fread($file, filesize("angle_x.txt"));
		fclose($file);
		$file = fopen("angle_y.txt","r");
		$tilt_y = fread($file, filesize("angle_y.txt"));
		fclose($file);
		$tilt_inbound = ($tilt_x <15 and $tilt_x >-15) and ($tilt_y <15 and $tilt_y >-15);
			if ($tilt_inbound){
				$warning_message = "";
				shell_exec('python3 Servo_90.py');
			} else {
				$warning_message = "Platform is too tilted!";
			}
		}
	if (isset($_POST['b4'])){
					// Get tilt using script
		shell_exec('python3 MPU.py');
		$file = fopen("angle_x.txt","r");
		$tilt_x = fread($file, filesize("angle_x.txt"));
		fclose($file);
		$file = fopen("angle_y.txt","r");
		$tilt_y = fread($file, filesize("angle_y.txt"));
		fclose($file);
		$tilt_inbound = ($tilt_x <15 and $tilt_x >-15) and ($tilt_y <15 and $tilt_y >-15);
			if ($tilt_inbound){
				shell_exec('python3 Servo_135.py');
			} else {
				$warning_message = "Platform is too tilted!";
			}
		}
	if (isset($_POST['b5'])){
					// Get tilt using script
		shell_exec('python3 MPU.py');
		$file = fopen("angle_x.txt","r");
		$tilt_x = fread($file, filesize("angle_x.txt"));
		fclose($file);
		$file = fopen("angle_y.txt","r");
		$tilt_y = fread($file, filesize("angle_y.txt"));
		fclose($file);
		$tilt_inbound = ($tilt_x <15 and $tilt_x >-15) and ($tilt_y <15 and $tilt_y >-15);
			if ($tilt_inbound){
				$warning_message = "";
				shell_exec('python3 Servo_180.py');
			} else {
				$warning_message = "Platform is too tilted!";
			}
		}

	if(True){
		// shell_exec('python3 camera_image.py');
		// $file = fopen("img_num.txt","r");
		// $img_num= fread($file, filesize("img_num.txt"));
		//fclose($file);
		//$file_name = "images/foam_img".$img_num.".png";
		sleep(1);
		$img = '<center> <img src = foam_img.jpg alt = "Sample Image"></center>';
	}
	if (isset($_POST['pic'])){
		
				// Get tilt using script
		shell_exec('python3 MPU.py');
		$file = fopen("angle_x.txt","r");
		$tilt_x = fread($file, filesize("angle_x.txt"));
		fclose($file);
		$file = fopen("angle_y.txt","r");
		$tilt_y = fread($file, filesize("angle_y.txt"));
		fclose($file);
		$tilt_inbound = ($tilt_x <15 and $tilt_x >-15) and ($tilt_y <15 and $tilt_y >-15);
			if ($tilt_inbound){
				$warning_message = "Analyzing...";
				shell_exec('python3 client_pi.py');
				header("Location: foam.php");
				exit();
			} else {
				$warning_message = "Platform is too tilted!";
			}
		
	}

?>

<html>
<head>
<link rel = "stylesheet" href = "main.css">
</head>
<body>
	
<div class = "top ">
	<font><center><b> <p class = "header_text">Capture Image</p><b></center></font>
</div>
<div class = "below_top">

</div>


	<center>
	<?= $img ?>
	<br><br>
		<div class = "separator"></div>
	<form method = "post">
<p>Select the angle for servo rotation:</p>
	<div class = "button_row">
	<button name = "b1" id="function_btn1">
		<p class ="button_text"> 0 &nbsp &nbsp Degrees </p>
	</button>
	&nbsp &nbsp
	<button name = "b2" id="function_btn2">
	<p class ="button_text">	45 &nbsp Degrees </p>
	</button>
	</div>
	<div class = "button_row">
	<button name = "b3" id="function_btn1" >
		<p class ="button_text">90 &nbsp Degrees</p>
	</button> 
	&nbsp &nbsp
	<button name = "b4" id="function_btn2">
		<p class ="button_text">135 &nbsp Degree</p>
	</button>
	</div>
	<div class = "button_row">
	<button name = "b5" id="function_btn3">
		<p class ="button_text">180 Degrees</p>
	</button>
	</div>
	<br><br>
	<div class = "separator"></div>
	<br><br>
	<button name = "pic" onClick = redirectToMain()>
		<p class ="button_text">Analyse Image</p>
	</button>
	<br><br>
	<?=$warning_message ?>

	</form>
	</center>

<script type = "text/javascript" >
	
	function redirectToMain()
	{
		window.location.replace("foam.php")
	}
</script>
</body>
</html>
