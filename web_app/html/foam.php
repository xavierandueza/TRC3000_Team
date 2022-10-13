<?php
	$digestate =  '<img src = transferred_files/digestate_colour.jpg alt = "digestate colour" style="width:300px; height:100px; margin-left:125px">';
	$foam =  '<img src = transferred_files/foam_colour.jpg alt = "foam colour" style="width:300px; height:100px; margin-left:125px">';
	if (isset($_POST['pic'])){
		header("Location: servo.php");
		exit();
	}

	if (isset($_POST['foam'])){
		if (isset($_POST['foam_height'])){
			if (isset($_POST['digestate'])){
				if (isset($_POST['digestate_height'])){
					//1111
					$img = '<img src = transferred_files/viz1111.jpg alt = "Sample Image">';
				} else {
					//1110
					$img =  '<img src = transferred_files/viz1110.jpg alt = "Sample Image">';
				}
			} else {
				if (isset($_POST['digestate_height'])){
					//1101
					$img =  '<img src = transferred_files/viz1101.jpg alt = "Sample Image">';
				} else {
					//1100
					$img =  '<img src = transferred_files/viz1100.jpg alt = "Sample Image">';
				}
			}
		} else {
			if (isset($_POST['digestate'])){
				if (isset($_POST['digestate_height'])){
					//1011
					$img =  '<img src = transferred_files/viz1011.jpg alt = "Sample Image">';
				} else {
					//1010
					$img =  '<img src = transferred_files/viz1010.jpg alt = "Sample Image">';
				}
			} else {
				if (isset($_POST['digestate_height'])){
					//1001
					$img =  '<img src = transferred_files/viz1001.jpg alt = "Sample Image">';
				} else {
					//1000
					$img =  '<img src = transferred_files/viz1000.jpg alt = "Sample Image">';
				}
			}
		}
	} else {
		if (isset($_POST['foam_height'])){
			if (isset($_POST['digestate'])){
				if (isset($_POST['digestate_height'])){
					//0111
					$img =  '<img src = transferred_files/viz0111.jpg alt = "Sample Image">';
				} else {
					//0110
					$img =  '<img src = transferred_files/viz0110.jpg alt = "Sample Image">';
				}
			} else {
				if (isset($_POST['digestate_height'])){
					//0101
					$img =  '<img src = transferred_files/viz0101.jpg alt = "Sample Image">';
				} else {
					//0100
					$img =  '<img src = transferred_files/viz0100.jpg alt = "Sample Image">';
				}
			}
		} else {
			if (isset($_POST['digestate'])){
				if (isset($_POST['digestate_height'])){
					//0011
					$img =  '<img src = transferred_files/viz0011.jpg alt = "Sample Image">';
				} else {
					//0010
					$img =  '<img src = transferred_files/viz0010.jpg alt = "Sample Image">';
				}
			} else {
				if (isset($_POST['digestate_height'])){
					//0001
					$img =  '<img src = transferred_files/viz0001.jpg alt = "Sample Image">';
				} else {
					//0000
					$img =  '<img src = transferred_files/viz0000.jpg alt = "Sample Image">';
				}
			}
		}
	}

?>

<html>
<head>
<link rel = "stylesheet" href = "main.css">
</head>
<body> 
	
<div class = "top ">
	<font><center><b> <p class = "header_text">Analysis Results</p><b></center></font>
</div>
<div class = "below_top">

</div>
	<center><?=$img?></center>
<div class = "below_top">

</div>

	<div style="width:100%; overflow: hidden;">
		<div style = "width:500px; float: left;"> 			
			<p class = "colour"> Foam Colour: </p>
			<?=$foam?>
			<br>
			<p class = "colour"> Digestate Colour: </p>
			<?=$digestate?>
			
		</div>
		<div style = "margin-left: 550px; margin-top: 0;"> 
			<p> Display Options: </p>
			<form method = "post">
			<input type ="checkbox" name = "foam" >
			<label for ="foam" class = "cform">Foam Area</label><br><br>
			<input type ="checkbox" name = "foam_height">
			<label for ="foam_height" class = "cform">Foam Height</label><br><br>
			<input type ="checkbox" name = "digestate">
			<label for ="digestate" class = "cform">Digestate Area</label><br><br>
			<input type ="checkbox" name = "digestate_height">
			<label for ="digestate_height" class = "cform">Digestate Height</label><br><br>
			<br>
			<button name = "submit" onClick = submit()>
				<p class ="button_text">Submit</p>
			</button> <br>
			
		</div>
	</div>
	
	<center>
		
		<br><br>
		<div class = "separator"></div>
		<br><br>
	<button name = "pic">
		<p class ="button_text">Retake Image</p>
	</button>
	</form>
	</center>
</body>
</html>

<script>
/*
document.addEventListener('DOMContentLoaded',()=>{
    let chk=document.querySelector('input[type="checkbox"][name="foam"]');
        chk.checked=localStorage.getItem( chk.name )==null || localStorage.getItem( chk.name )=='false' ? false : true;
        
        chk.addEventListener('click',e=>{
            localStorage.setItem( chk.name, chk.checked )
            //location.reload();
        });
});

function set_state(){
	*/
}
</script>
