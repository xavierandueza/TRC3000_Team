document.getElementById("text").innerHTML = "Weight of the given sample is   " + weight + "  g";

function rotateMotor(){
	console.log("HELLO")
}
function startMeasurement()
{
		alert("Measuring weight");
		var weight = "<?php measure_weight(); ?>";
		document.getElementById("text").innerHTML = "The weight of the sample is: " + weight

		if(weight>190 && weight<210)
		{
			var off = "<?php load_cell_off(); ?>";
			var IMU_result = "<?php IMU_ON(); ?>";
			
			if(IMU_result > soft_limit)
			{
				alert("Moving too quick");
			}
			else
			{
				document.getElementById("text2").innerHTML = "Set the rotation angle";
				document.getElementById("text2").innerHTML = "Please select the angle";
			}
		}
		else
		{
			if(weight>200)
			{
				alert("Too much digest!! Please empty flask and refill.");
				PRATEEK BHAI REDIRECT
			}
			else
			{
				alert("Not enough Digest");
				PRATEEK BHAI REDIRECT
			}
		}
}
function redirectToHome()
{
	window.location.replace("index.php") 
}
function camera_function()
{
	var capture = "<?php camera_php_function(); ?>";				
}
