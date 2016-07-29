<!DOCTYPE HTML>
<html>
	<?php
			ini_set('max_execution_time', 300);
			$con=mysqli_connect("localhost","root","shands@UF","medical");
			
			// Check connection
			if (mysqli_connect_errno($con))
		    {
				echo "Failed to connect to MySQL: " . mysqli_connect_error();
			}
			
			$ptID=$_GET['ptID'];
			$user=$_GET['user'];
		?>
	<head>
		<title>Have you considered this?</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
	    <script src="http://code.jquery.com/jquery.js"></script>
	    <script src="js/bootstrap.min.js"></script>
	    <script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>
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
		<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
		<script src="http://code.jquer.com/jquery-1.9.1.js"></script>
		<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
		<link rel="stylesheet" href="/resources/demos/style.css" />
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
				background-color:#00FF00;
				filter:progid:DXImageTransform.Microsoft.gradient(GradientType=1,startColorstr=#00FF00, endColorstr=#FFFF00);
				background-image:-moz-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-o-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-ms-linear-gradient(left, #00FF00 0%, #FFFF00 25%,#FFA500 50%,#FF0000 100%);
				background-image:-webkit-gradient(linear, left bottom, right bottom, color-stop(0%,#00FF00), color-stop(25%,#FFFF00),color-stop(50%,#FFA500),color-stop(100%,#FF0000));
				background-image: linear-gradient(to right, #00FF00 0%,#FFFF00 25%,#FFA500 75%, #FF0000 100%);
				
				margin: 0 auto;
			}
			
		</style>
		
		<script>
			var startTime=Date.now();
			function submit(){
				var recoTaken=$('input[name=FeedBack]:checked').val();
				var recomendation="";
				var cases="";
				var id="<?php echo $ptID?>";
				var user="<?php echo $user?>";
				
				var time=(Date.now()-startTime)/1000;
				
				if(recoTaken=="Yes"){
					for (var i=1; i < 11; i++) {
						if($('input[name=reco'+i+']:checked').val())
							recomendation+=$('input[name=reco'+i+']:checked').val()+";";
					};
					if($('input[name=reco11]:checked').val())
							recomendation+='Other:'+$('input[name=otherIP]').val()+";";
							
					for (var i=1; i <= 6; i++) {
						if($('input[name=case'+i+']:checked').val())
							cases+=$('input[name=case'+i+']:checked').val()+";";
					}
					//alert("submit.php?recoPos=true&id="+id+"&user="+user+"&recos="+recomendation+"&cases="+cases)
					window.location.href = "submit.php?recoPos=true&id="+id+"&user="+user+"&recos="+recomendation+"&cases="+cases+"&time="+time;
				}else{
					window.location.href = "submit.php?recoNeg=true&id="+id+"&user="+user+"&time="+time;
				}
		    			    	
		    }
		    
		    function changeEnable(){
		    	
		    	
		    	if($('input[name=reco11]:checked').val()){
		    		$('input[name=otherIP]').removeAttr("disabled");
		    	}else{
		    		$('input[name=otherIP]').attr("disabled", "disabled");
		    	}
		    }
		    
		    
		    function changeVisibility(visible){
		    	if(visible==true){
		    		document.getElementById('recomendationSec').style.display= 'block';
		    	}else{
		    		document.getElementById('recomendationSec').style.display= 'none';
		    	}
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
		    
        		<div id="Feedback Section"align="center">
        			<b>Based on the presented risk scores would you consider any specific intervention?</b> 
					<br />
					<div>
						<input type="radio" name="FeedBack" value="No" checked onchange="changeVisibility(false);">No&nbsp;&nbsp;
						<input type="radio" name="FeedBack" value="Yes" onchange="changeVisibility(true);">Yes
		        	</div>
		        	<br />
        		</div>
        		<div id="recomendationSec" align="left" style="display: none;">
					<b>If Yes chose one or more from the following:</b>
					<form>
					<input type="checkbox" name="reco1" value="arterial">Place arterial line<br>
					<input type="checkbox" name="reco2" value="arterialHemodynamic">Place arterial line and use hemodynamic monitoring<br>
					<input type="checkbox" name="reco3" value="CVP">Place central venous line and use CVP<br>
					<input type="checkbox" name="reco4" value="PA">Place PA catheter<br>
					<input type="checkbox" name="reco5" value="therapy">Goal directed therapy<br>
					<input type="checkbox" name="reco6" value="diuretics">Avoid diuretics<br>
					<input type="checkbox" name="reco7" value="transfusion">Restrictive blood transfusions<br>
					<input type="checkbox" name="reco8" value="resuscitation">Restrictive crystalloid resuscitation<br>
					<input type="checkbox" name="reco9" value="colloid">Use colloid resuscitation<br>
					<input type="checkbox" name="reco10" value="albumin">Use albumin<br>
					<input type="checkbox" name="reco11" value="other" onclick="changeEnable();">Other:<input type="text" name="otherIP" disabled /><br>
					</form>
					<br/><br/>
					<b>This interventions would mitigate risk for which postoperative complications:</b><br />
					<input type="checkbox" name="case1" value="rifle7">RIFLE-AKI occurring in the first seven postoperative days<br>
					<input type="checkbox" name="case2" value="ICU">Admission to ICU more than two days<br>
					<input type="checkbox" name="case3" value="ventilator">Mechanical ventilation days more than two days<br>
					<input type="checkbox" name="case4" value="cardioVascular">Cardiovascular complications<br>
					<input type="checkbox" name="case5" value="sepsis">Severe sepsis<br>
					<input type="checkbox" name="case6" value="mortality">30-day mortality<br>
					</form>
					
					<br />
					</div>
					<button name="submit" class="btn btn-primary btn-large" onclick="submit()">SUBMIT</button>
	        </div>  
	    </body>
</html>
