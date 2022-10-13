<?php

	$file = fopen("weights.txt","r") or die("unable to open file");
	$weight = fread($file, filesize("weights.txt"));
	fclose($file);
?>


<html>
	
	<body>
The weight of the given sample is: <?=$weight ?> g
</body>
</html>
