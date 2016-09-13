
<!DOCTYPE HTML>
<html>
	<head>
		<?php
			
			// ini_set('max_execution_time', 300);
			// // Create connection
			// $con=mysqli_connect("localhost","root","root","shands_web");
			
			// // Check connection
			// if (mysqli_connect_errno($con))
		 //    {
			// 	echo "Failed to connect to MySQL: " . mysqli_connect_error();
			// }
			

			$docID=$_GET['id'];
			$scrnID=$_GET['scrnID'];
		?>
		<title>Next Steps</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
	    <script   src="https://code.jquery.com/jquery-3.1.0.min.js"   integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s="  
	     crossorigin="anonymous"></script>
	    <script src="https://code.jquery.com/jquery.js"></script>
	    <script src="js/bootstrap.min.js"></script>
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
		<link rel="stylesheet" href="https://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
		<script src="https://code.jquery.com/jquery-1.9.1.js"></script>
		<script src="https://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
		<!-- <link rel="stylesheet" href="/resources/demos/style.css" /> -->
		<style> 
			#headHTML
			{
				padding:10px 40px; 
				background:#0086C4;
				height:40px;
				border-top-left-radius:20px;
				border-top-right-radius:20px; 
			}
			
			#envelope
			{
				
				border-radius:25px;
				border-color: #0086C4;
				border-style: solid; 
				width:60%;				
				alignment-baseline: central;
			}
		</style>
		<script>
			function submit(){
				
				var link="<?php if ($scrnID<="2") {
					echo "tableview.php?id=$docID";
				} else {
					echo "index.html";
				}
				?>"

				 window.location.href = link;
				
				// if ( id == "continue"){
				// 	window.location.href = "<?php echo "tableview.php?id=$docID"?>";  
				// }else {
				// 	window.location.href = "index.html";
				// }
				
				
			}
			
		</script>
		</head>
    <body>
    	
    	<br />
    	<div id="envelope" class="container" align="center" >
	        <div id="headHTML" align="center">
	        		<div align="center"><font color="#ff9900"size="25px">UF Health</font></div>
	        </div>
	        
	        <br />
	       	<p><?php

	       	// if ($scrnID=="2") {
				echo "Thanks for participating in the study. Please spare a few minutes with our representative to record your feedback and views. </br>
				Have a Nice Day !!";	   
			// } elseif ($scrnID=="2") {
			// 	echo "Great Job! Its almost over. Lets finish this study without the predictor.";
			// } else {
				 // echo "Thanks for participating in the study. Please spare a few minutes with our representative to record your feedback and views";  
			   // }
			   
	       	
	       	?></p>
	        <button class="btn btn-primary" type="button" id="continue" onclick="submit();">Continue</button>
	        <button class="btn btn-primary" type="button" id="logoff" onclick ="window.location.href='index.html'">LogOff</button>

	        <br /> 
	        <br />
        </div> 
         
    </body>
</html>
