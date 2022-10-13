<?php
function rotate_motor_script_exec_30()
{
	echo shell_exec('python3 Servo_30.py');
}
function rotate_motor_script_exec_120()
{
	shell_exec('python3 test.py');
}

?>

<html>
<head>
<link rel = "stylesheet" href = "main.css">
</head>
<body onLoad = "startMeasure()">
	<h1 class = "header_text" id = "text">
		Main Functionality page
	</h1>
	<button onClick = rotateMotor_30()>
		30 Degrees
	</button>
	<button onClick = rotateMotor_60()>
		60 Degrees
	</button>
	<button onClick = rotateMotor_90()>
		90 Degrees
	</button>
	<button onClick = myFunction_click_120()>
		120 Degrees
	</button>
	<button onClick = rotateMotor_150()>
		150 Degrees
	</button>
	<button onClick = rotateMotor_180()>
		180 Degrees
	</button>
<script>

function startMeasure(){
	alert("Starting weight measurement now.");
}
function rotateMotor_30()
{
	var res = <?php rotate_motor_script_exec_30(); ?>; 
	console.log(res);
}
function rotateMotor_120(){
	<?php rotate_motor_script_exec_120(); ?>; 

	}
function myFunction_click_30(){
	$.ajax({
		url:"Servo_30.py",
		context: document.body
		}).done(function() {
			console.log("Python script should have run 30")
			})
	}
function myFunction_click_120(){
	$.ajax({
		url:"Servo_120.py",
		context: document.body
		}).done(function() {
			console.log("Python script should have run 120")
			})
	}
</script>
<script type = "text/javascript" src = "https://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js"></script>
</body>
</html>

