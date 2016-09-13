<!DOCTYPE HTML>
<html>
	<?php
			ini_set('max_execution_time', 300);
			$con=mysqli_connect("localhost","root","root","shands_web");
			
			// Check connection
			if (mysqli_connect_errno($con))
		    {
				echo "Failed to connect to MySQL: " . mysqli_connect_error();
			}
			
			$ptID=$_GET['ptID'];
			$outcomeID=$_GET['outcome'];
			$docID=$_GET['user'];
			$result = mysqli_query($con,"select outcome,description from outcomes where id=".$outcomeID);
			$row=mysqli_fetch_array($result);
			$outcomeTable=$row['outcome'];
			$label=$row['description'];
		?>
	<head>
		<title>Let's Review</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
	    <script   src="https://code.jquery.com/jquery-3.1.0.min.js"   integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s="   crossorigin="anonymous"></script>
	    <script src="https://code.jquery.com/jquery.js"></script>
	    <script src="js/bootstrap.min.js"></script>
	    <script type="text/javascript" src="https://platform.twitter.com/widgets.js"></script>
		<script src="js/jquery.js"></script>
		<script src="js/bootstrap-transition.js"></script>
		<script src="js/bootstrap-alert.js"></script>
		<script src="js/bootstrap-modal.js"></script>
		<script src="js/bootstrap-dropdown.js"></script>
		<script src="js/bootstrap-scrollspy.js"></script>
		<script src="js/bootstrap-tab.js"></script>
		<script src="js/bootstrap-tooltip.js"></script>
		<script src="js/bootstrap-popover.js"></script>
		<script src="js/bootstrap-button.js"></script>
		<script src="js/bootstrap-collapse.js"></script>
		<script src="js/bootstrap-carousel.js"></script>
		<script src="js/bootstrap-typeahead.js"></script>
		<script src="js/bootstrap-affix.js"></script>
		<script src="js/holder/holder.js"></script>
		<script src="js/google-code-prettify/prettify.js"></script>
		<script src="js/application.js"></script>
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
		<script type="text/javascript" src="https://www.google.com/jsapi"></script>
		<link rel="stylesheet" href="https://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
		<script src="https://code.jquery.com/jquery-1.9.1.js"></script>
		<script src="https://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
		<!-- <link rel="stylesheet" href="/resources/demos/style.css" /> -->
		<style> 
			#headHTML
			{
				padding:10px 40px; 
				background:#0086C4;
				height:28px;
				border-top-left-radius:20px;
				border-top-right-radius:20px;
			}
			#envelope
			{
				border-radius:20px;
				border-color: #0086C4;
				border-style: solid; 
				width:80%;				
				alignment-baseline: central;
			}
			
			#docPredict{
				width: 90%;
				/*background-color:#00FF00;
				filter:progid:DXImageTransform.Microsoft.gradient(GradientType=1,startColorstr=#00FF00, endColorstr=#FFFF00);
				background-image:-moz-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-o-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-ms-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-gradient(linear, left bottom, right bottom, color-stop(0%,#00FF00), color-stop(25%,#FFFF00),color-stop(50%,#FFA500),color-stop(100%,#FF0000));
				background-image: linear-gradient(to right, #00FF00 0%,#FFFF00 25%,#FFA500 75%, #FF0000 100%);
				*/
				margin: 0 auto;
			}
			.ab {	

				width: 90%;
				background-color:#00FF00;
				filter:progid:DXImageTransform.Microsoft.gradient(GradientType=1,startColorstr=#00FF00, endColorstr=#FFFF00);
				background-image:-moz-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-o-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-ms-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-gradient(linear, left bottom, right bottom, color-stop(0%,#00FF00), color-stop(25%,#FFFF00),color-stop(50%,#FFA500),color-stop(100%,#FF0000));
				background-image: linear-gradient(to right, #00FF00 0%,#FFFF00 25%,#FFA500 75%, #FF0000 100%);
			}
			.ab1 {
				width: 90%;
				background-color:#00FF00;
				filter:progid:DXImageTransform.Microsoft.gradient(GradientType=1,startColorstr=#00FF00, endColorstr=#FFFF00);
				background-image:-moz-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-o-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-ms-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-gradient(linear, left bottom, right bottom, color-stop(0%,#00FF00), color-stop(25%,#FFFF00),color-stop(50%,#FFA500),color-stop(100%,#FF0000));
				background-image: linear-gradient(to right, #00FF00 0%,#FFFF00 35%, #FF0000 47%);
				
				
			}

			.ab2 {
				width: 90%;
				background-color:#00FF00;
				filter:progid:DXImageTransform.Microsoft.gradient(GradientType=1,startColorstr=#00FF00, endColorstr=#FFFF00);
				background-image:-moz-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-o-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-ms-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-gradient(linear, left bottom, right bottom, color-stop(0%,#00FF00), color-stop(25%,#FFFF00),color-stop(50%,#FFA500),color-stop(100%,#FF0000));
				background-image: linear-gradient(to right, #00FF00 0%,#FFFF00 13%, #FF0000 40%);
				
				
			}
			.ab3 {

				width: 90%;
				background-color:#00FF00;
				filter:progid:DXImageTransform.Microsoft.gradient(GradientType=1,startColorstr=#00FF00, endColorstr=#FFFF00);
				background-image:-moz-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-o-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-ms-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-gradient(linear, left bottom, right bottom, color-stop(0%,#00FF00), color-stop(25%,#FFFF00),color-stop(50%,#FFA500),color-stop(100%,#FF0000));
				background-image: linear-gradient(to right, #00FF00 0%,#FFFF00 7%, #FF0000 43%);
				
				
			}
			.ab4 {

				width: 90%;
				background-color:#00FF00;
				filter:progid:DXImageTransform.Microsoft.gradient(GradientType=1,startColorstr=#00FF00, endColorstr=#FFFF00);
				background-image:-moz-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-o-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-ms-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-gradient(linear, left bottom, right bottom, color-stop(0%,#00FF00), color-stop(25%,#FFFF00),color-stop(50%,#FFA500),color-stop(100%,#FF0000));
				background-image: linear-gradient(to right, #00FF00 0%,#FFFF00 25%,#FFA500 75%, #FF0000 100%);
				
				
			}

			.ab5 {

				width: 90%;
				background-color:#00FF00;
				filter:progid:DXImageTransform.Microsoft.gradient(GradientType=1,startColorstr=#00FF00, endColorstr=#FFFF00);
				background-image:-moz-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-o-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-ms-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-gradient(linear, left bottom, right bottom, color-stop(0%,#00FF00), color-stop(25%,#FFFF00),color-stop(50%,#FFA500),color-stop(100%,#FF0000));
				background-image: linear-gradient(to right, #00FF00 0%,#FFFF00 3%,#FF0000 41%);
				
				
			}
		</style>
		
		<script>
			var startTimeScrn=0;
			var endTimeScrn=0
			var noReview=0;
			$(function() {
				startTimeScrn=Date.now();						
				$( "#docPredict" ).slider({
	        		value:50,
	        		min: 0,
	        		max: 100,
	        		step: 1,
	        
	        		slide: function( event, ui ) {
					    $( "#docPredictVal" ).text( ui.value);
					    $(ui.value).val($('#docPredictVal').text());
					    $( '#docPredictDisp' ).text("Your Prediction is "+$('#docPredictVal').text()+"%");
						$( '#docPredictDisp' ).css('font-weight', 'bold');
				    }
				});		    
			});	
				    
		    function checkIn(){
		    	//alert("hi");
		    	endTimeScrn=Date.now();
		    	var time=(endTimeScrn-startTimeScrn)/1000;
		    	var id="<?php echo $ptID?>";
				var doc="<?php echo "$docID"?>";
		 		var outcome="<?php echo $outcomeID?>";
		 		var attempt2=$( '#docPredictVal' ).text();
		    	window.location.href = "submit.php?id="+id+"&user="+doc+"&outcome="+outcome+"&attempt="+attempt2+"&time="+time+"&noReview="+noReview;;
			}
			
			function checkStory(){
		    	noReview=noReview+1;
		    	$('#reviewResults').hide();
		  		$('#storyBoard').show();	
		    }
		    
		    function goBack(){
		    	$('#reviewResults').show();
		  		$('#storyBoard').hide();	
		    }
			
		</script>
		
		</head>
	    <body>
	    	<br />
	    	<div id="envelope" class="container" align="center">
		        <div id="headHTML" align="center">
		        		<div align="center"><font color="#ff9900"size="20px">UF Health</font></div>
		        </div>
		        <br />
		    
        		<div id="reviewResults"align="center">
        		 <b>After reviewing computer algorithm's calculated risk scores and explanations for the risk please reconsider your assessment and provide our scores again, on the scale from 1 ("no chance") to 100 ("certainty").</b> 
					<br />
					Please  touch screen on each of the scale below to assign corresponding risk for this patient.
		
			        <div id="bar" class="container" align="center">
		        			
		        			<br />
		        			<p><b><?php echo $label ?></b></p>
		        			<div id="docPredict" align="center" class="ab<?php if($outcomeTable =="ICU"){echo "1";}else if($outcomeTable=="ventilator"){echo "2";}else if($outcomeTable == "cardioVascular"){echo "3";}elseif ($outcomeTable == "sepsis"){echo "";}else if($outcomeTable == "mortality"){echo "5";}else{echo "";} 
		        				# code...?>"></div>
		        			<label id="docPredictVal" style="display:none">50</label>
		       				<p><label id="docPredictDisp" style="font-weight:bold">Your Prediction is 50%</label></p>
		        			
		        			<br />
		        			
		        			<button name="submit" class="btn btn-primary btn-large" onclick="checkIn();">SUBMIT</button>
		        			<button id="story" class="btn btn-warning" onclick="checkStory();">Review Patient</button>
		        			
		        	</div>
		        	<br />
        		</div>
        		<div id="storyBoard" style="display: none;">
						<?php
							$story1=file_get_contents("story1");
							$story2=file_get_contents("story2");
							echo "<p>$story1</p><p>$story2</p>"
						?>
						<button id="back" class="btn btn-warning" onclick="goBack();">Go Back</button>
						<br />
	        	</div>
	        </div>  
	    </body>
</html>
