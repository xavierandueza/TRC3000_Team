<?php

	$weight = "---";
	$warning_message = "";
	if (isset($_POST['b7']))
	{
		
		$warning_message = "Calculating Weight...";
		// Get tilt using script
		shell_exec('python3 MPU.py');
		$file = fopen("angle_x.txt","r");
		$tilt_x = fread($file, filesize("angle_x.txt"));
		fclose($file);
		$file = fopen("angle_y.txt","r");
		$tilt_y = fread($file, filesize("angle_y.txt"));
		fclose($file);
		
		$tilt_x = intval($tilt_x);
		$tilt_y = intval($tilt_y);
		$tilt_inbound_x = ($tilt_x <15 and $tilt_x >-15);
		$tilt_inbound_y = ($tilt_y <15 and $tilt_y >-15);
		$tilt_inbound = $tilt_inbound_x and $tilt_inbound_y;
		if(! $tilt_inbound) 
		{ 
			$weight = "---";
			$warning_message = "Plaform is tilted!";
		} else
		{
			
			// Get weight using scripts
			shell_exec('python3 MAIN2.py');
			$file = fopen("weights.txt","r");
			$weight = fread($file, filesize("weights.txt"));
			fclose($file);
			
			$valid_weight = True;
			foreach (str_split($weight) as $char) {
				if (($char != ".")and ($char != "0") and ($char != "1") and ($char != "2") and ($char != "3") and ($char != "4") and ($char != "5") and ($char != "6") and ($char != "7") and ($char != "8") and ($char != "9")){ 
					$valid_weight = False;
					break;
				}
			}

					
			
			$weight_inbound = $weight>140 and $weight<160;
			if ($valid_weight){
				if ($weight_inbound)
				{
					$warning_message = "Weight is within bounds";
				} else
				{
					$warning_message = "The weight of the given sample is out of bounds of 140g and 160g.";
				}	
				
			}
			else {
				$warning_message = $weight;
				$weight = "---";
			}
		}
	}
	if (isset($_POST['next'])){
		
				// Get tilt using script
		shell_exec('python3 MPU.py');
		$file = fopen("angle_x.txt","r");
		$tilt_x = fread($file, filesize("angle_x.txt"));
		fclose($file);
		$file = fopen("angle_y.txt","r");
		$tilt_y = fread($file, filesize("angle_y.txt"));
		fclose($file);
		$tilt_x = intval($tilt_x);
		$tilt_y = intval($tilt_y);
		$tilt_inbound_x = ($tilt_x <15 and $tilt_x >-15);
		$tilt_inbound_y = ($tilt_y <15 and $tilt_y >-15);
		$tilt_inbound = $tilt_inbound_x and $tilt_inbound_y;
			if ($tilt_inbound){
				// Get weight using scripts
				shell_exec('python3 MAIN2.py');
				$file = fopen("weights.txt","r");
				$weight = fread($file, filesize("weights.txt"));
				fclose($file);
				
				$valid_weight = True;
				foreach (str_split($weight) as $char) {
					if (($char != ".")and ($char != "0") and ($char != "1") and ($char != "2") and ($char != "3") and ($char != "4") and ($char != "5") and ($char != "6") and ($char != "7") and ($char != "8") and ($char != "9")){ 
						$valid_weight = False;
						break;
					}
				}

				$weight_inbound = $weight>140 and $weight<160;
				if ($weight_inbound){
					header("Location: servo.php");
					exit();
				} else {
					$warning_message = "Make sure weight is within 140-160 grams before proceeding!";
				}

			} else {
				$warning_message = "Make sure platfrom is flat before proceeding!";
			}
		
	}
?>

<html>
<head>
<link rel = "stylesheet" href = "main.css">
</head>
<body>
	


<div class = "top ">
	<font><center><b> <p class = "header_text">Measure Weight</p><b></center></font>
</div>
<div class = "below_top">

</div>
<div class = "below_top">

</div>
<div class = "below_top">

</div>
<div class = "below_top">

</div>
	
	<center>
	<form method = "post">
	<button name = "b7" id="function_btn">
		<p class ="button_text">Display weight </p>
	</button>
	<br><br>
	<p>
	The weight of the given sample is:
	</p>
	<div class = "separator"></div>
	<p class = "sec">
	 <?=$weight ?> grams
	</p>
	<div class = "separator"></div>
	<p class = "warning">
	<?=$warning_message ?>
	</p>
	<br><br><br>
	
	
	<br>
	<button name="next">
		<p class ="button_text">Next</p>
	</button>
	</form>
	</center>

<script type = "text/javascript" >
	
</script>
</body>
</html>
