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
			
			$result = mysqli_query($con,"select outcome from outcome_".$outcomeTable." where id='".$ptID."'");
			$row=mysqli_fetch_array($result);
			$outcome=$row['outcome'];
		
		?>
	<head>
		<title>Here is what we think</title>
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
	<!-- 	<link rel="stylesheet" href="/resources/demos/style.css" /> -->
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
			
			#pbar{
				width: 65%;
				margin: 0 auto;
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
			var startTimeScrn1=0;
			var endTimeScrn1=0
			var noReview=0
			
		    function submit(){
		    	endTimeScrn=Date.now();
		  		var time=(endTimeScrn-startTimeScrn)/1000;
		    	var id="<?php echo $ptID?>";
				var doc="<?php echo "$docID"?>";
		 		var outcome="<?php echo $outcomeID?>";
		 		var features="";
		 		for (var i=0; i <= 10; i++) {
		    		var component="#top"+i+"Val";
		    		
		    		if($('#top'+i+'Var').val()==null)
		    			continue;
		    		
		    		if(!$(component).prop('disabled'))
		    			features+=$('#top'+i+'Var').val()+":";
		    	}
		    	window.location.href = "submit.php?feedback=true&id="+id+"&user="+doc+"&outcome="+outcome+"&time="+time+"&features="+features+"&noReview="+noReview;
		    			    	
		    }

				
			$(function() {
				var label = "<?php echo $outcomeTable?>";
				startTimeScrn=Date.now();
    			$("#pbar").progressbar();
	            $("#pbar").bind('progressbarchange', function(event, ui) {
	                var value =this.getAttribute( "aria-valuenow" );
	                //console.log(value);
	                var selector = "#" + this.id + " > div";
	                //console.log(this.id);

	           	if(label == "rifle7"){
	           		colorcode(value,1 ,4);
	           	}else if(label == "ICU"){
	           		colorcode(value,35 , 47);
	           	}else if(label== "ventilator"){
	           		colorcode(value,13 ,40);
	           	}else if(label=="cardioVascular"){
	           		colorcode(value, 7,43);
	           	}else if(label == "sepsis"){
	           		colorcode(value, 6,35 );
	           	}else if(label == "mortality"){
	           		colorcode(value, 3, 41)
	           	}else { colorcode(value,25 ,50 );

	           	}
	               
	               function colorcode( value ,cut1, cut2){
					if (value >= cut2){
	                    $(selector).css({ 'background': '#FF0000' });
	                } else if (value >= cut1){
	                    $(selector).css({ 'background': '#FFFF00' });
	                
	                }else{
	                    $(selector).css({ 'background': '#00FF00' });
	                }

					} 
	                
	            });
	            
	            var val=parseInt($('#mcPredict').val());
				$("#pbar").progressbar({ "value":val});		    
			});	

			
			
			
			$(function(){
				for (var i = 1; i <=5; i++){
					var barName="positive"+i;
					var barValue=barName+"Val";
					$("#"+barName).progressbar();
		            $("#"+barName).bind('progressbarchange', function(event, ui) {
		                var value =this.getAttribute( "aria-valuenow" ); 
		                console.log(value);   
		                var selector = "#" + barName + " > div";
		                $(selector).css({ 'background': '#FF0000' });
		            });
		            
		            var val=parseInt($('#'+barValue).val());
					$("#"+barName).progressbar({ "value":val});  
				};
				
				for (var i = 6; i <=10; i++){
					var barName="negative"+i;
					var barValue=barName+"Val";
					$("#"+barName).progressbar();
		            $("#"+barName).bind('progressbarchange', function(event, ui) {
		                var value =this.getAttribute( "aria-valuenow" ); 
		                console.log(value);   
		                var selector = "#" + barName + " > div";
		                $(selector).css({ 'background': '#00FF00' });
		            });
		            
		            var val=parseInt($('#'+barValue).val());
					$("#"+barName).progressbar({ "value":val});  
				};
				
			});    
			
			function reset(){
				for (var i=1; i <= 10; i++) {
					var plusBttn="#top"+i+"Plus";
			    	var minusBttn="#top"+i+"Minus";
			    	var val="#top"+i+"Val";
			    	var label="#top"+i;	    	
			    	$(plusBttn).attr("disabled", "disabled");
			    	$(val).removeAttr("disabled");
			    	$(minusBttn).removeAttr("disabled");
			    	$(label).css({color:"black"})
				};
		    	
		    }
		    
			function minus(var1){
		    	var plusBttn="#top"+var1+"Plus";
		    	var minusBttn="#top"+var1+"Minus";
		    	var val="#top"+var1+"Val";
		    	var label="#top"+var1;
		    	$(val).attr("disabled", "disabled");
		    	$(minusBttn).attr("disabled", "disabled");
		    	$(plusBttn).removeAttr("disabled");
		    	$(label).css({color:"silver"})
		    }	
		    
		    function checkStory(){
		    	noReview=noReview+1;
		    	$('#reviewFeatures').hide();
		  		$('#storyBoard').show();	
		    }
		    
		    function goBack(){
		    	$('#reviewFeatures').show();
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
		        <div id="reviewFeatures">
			        The computer algorithms have calculated that probability risk scores for <strong><?php echo $label?>:</strong> 
			        <br />
			        <div>
		        		<div id="pbar" style="height: 10px;" ></div>
		        		<input id="mcPredict" value="<?php echo $outcome?>" type="hidden" />
	        		</div>
	      
	        		<div id="tableInfo" align="center" >
	        			<br />
	        			<p><b>These are the main factors contributing to this patients' risk. If you disagree with any factors, please touch the Disagree button next to it. </b></p>
	        			<br />
	        			<table width="90%">
	        				<colgroup >
							    <col width="20%">
								<col span="3"/>
							    <col width="20%">
							</colgroup>
	        				<th colspan="3">Factors Increasing Risk</th>
	        				<th colspan="3">Factors Decreasing Risk</th>
	        				<?php
	        					// mysqli_query($con,"create or replace view tempViewPositive as select outc.id ID,rank,var,description,ptDt.value value,weight from outcomeRank_".$outcomeTable." outc, varDef, patientDetails ptDt where outc.id='".$ptID."' and outc.id=ptDt.ID and outc.weight > 0 and outc.var=varDef.id and ptDt.feature=outc.var and rank<=5 limit 5");
	        					// mysqli_query($con,"create or replace view tempViewNegative as select outc.id ID,rank,var,description,ptDt.value value,outc.weight*-1 weight from outcomeRank_".$outcomeTable." outc, varDef, patientDetails ptDt where outc.id='".$ptID."' and outc.id=ptDt.ID and outc.weight < 0 and outc.var=varDef.id and ptDt.feature=outc.var order by rank desc limit 5");
	        					
	        					
	        					mysqli_query($con,"create or replace view tempViewPositive as select outc.id ID,rank,var,description,ptDt.value value,weight from outcomeRank_".$outcomeTable." outc, varDef, patientDetails ptDt where outc.id='".$ptID."' and outc.id=ptDt.ID and outc.weight > 0 and outc.var=varDef.type and ptDt.feature=outc.var and rank<=5 limit 5");
	        					mysqli_query($con,"create or replace view tempViewNegative as select outc.id ID,rank,var,description,ptDt.value value,outc.weight*-1 weight from outcomeRank_".$outcomeTable." outc, varDef, patientDetails ptDt where outc.id='".$ptID."' and outc.id=ptDt.ID and outc.weight < 0 and outc.var=varDef.type and ptDt.feature=outc.var order by rank desc limit 5");
	        					

	        					$resultPositive = mysqli_query($con,"select temp.id id, temp.var var, description, weight, temp.value actual,varMap.value value from tempViewPositive temp left outer join varMap on (temp.var=varMap.id and temp.value=varMap.map) order by rank");
								$resultNegative = mysqli_query($con,"select temp.id id, temp.var var, description, weight, temp.value actual,varMap.value value from tempViewNegative temp left outer join varMap on (temp.var=varMap.id and temp.value=varMap.map) order by rank desc");
								
							
								for ($i=1; $i <= 5; $i++) {
									$rowPositive = mysqli_fetch_array($resultPositive);
									$rowNegative = mysqli_fetch_array($resultNegative);
									if( $i == 1 ){
										$max = ($rowPositive['weight']>=$rowNegative['weight']) ? $rowPositive['weight'] : $rowNegative['weight'];
									}
									
 									$j=$i+5;
									echo "<tr>";
									#$rowPostive['id']
								
									if($rowPositive['id']==""){
										echo "<td colspan=\"3\">";
									} 
									else {
										echo "<td width=\"30%\"><label id=\"top".$i."\">".$rowPositive['description']."</label></td>";
			        					echo "<td width=\"5%\"><table><tr>";
			        					echo "<td><div id='positive".$i."' style=\"height: 4px;\"></div></td>";
			        					echo "<td><input id='positive".$i."Val' value=\"".(($rowPositive['weight']*100)/$max)."\" type=\"hidden\" /></td>";			
										echo "</tr><tr>";
							
										if($rowPositive['var']=="pr1"){
											$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='pr1'");
											$row=mysqli_fetch_array($result);
								        	$pr1_temp=$row['value'];
											
										
											
											$result = mysqli_query($con,"select description from pr1Map where id='".$pr1_temp."'");
											$row=mysqli_fetch_array($result);
											echo "<td><input id=\"top".$i."Val\" value=\"".$row['description']."\" readonly/></td>";
										}else if($rowPositive['var']=="MDC"){
											$mdcVal=intval($rowPositive['actual']);
											$result = mysqli_query($con,"select description from mdcMap where id='".$mdcVal."'");
											$row=mysqli_fetch_array($result);
											echo "<td><input id=\"top".$i."Val\" value=\"".$row['description']."\" readonly/></td>";
										}else{
											if ($rowPositive['value']==NULL) 
												echo "<td><input id=\"top".$i."Val\" value=\"".$rowPositive['actual']."\" readonly/></td>";
											else 
												echo "<td><input id=\"top".$i."Val\" value=\"".$rowPositive['value']."\" readonly/></td>";
										}
			        					echo "<td><input id=\"top".$i."Var\" value=\"".$rowPositive['var']."\" type=\"hidden\" /></td>";
			        					echo "</tr></table></td>";			
										echo "<td width=\"5%\"><button id=\"top".$i."Minus\" class=\"btn btn-danger\" onclick=\"minus(".$i.");\" ><i class=\"icon-thumbs-down\"></i></button></td>";
									}
									
									if($rowNegative['id']==""){
										echo "<td colspan=\"3\">";
									} 
									else {
										echo "<td width=\"30%\"><label id=\"top".$j."\">".$rowNegative['description']."</label></td>";
			        					echo "<td width=\"5%\"><table><tr>";
			        					echo "<td><div id='negative".$j."' style=\"height: 4px;\"></div></td>";
			        					echo "<td><input id='negative".$j."Val' value=\"".(($rowNegative['weight']*100)/$max)."\" type=\"hidden\" /></td>";			
										echo "</tr><tr>";
										if($rowNegative['var']=="pr1"){
											$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='pr1'");
											$row=mysqli_fetch_array($result);
								        	$pr1_temp=$row['value'];
										
											$result = mysqli_query($con,"select description from pr1Map where id='".$pr1_temp."'");
											$row=mysqli_fetch_array($result);
								        								
											echo "<td><input id=\"top".$j."Val\" value=\"".$row['description']."\" readonly/></td>";
										}else if($rowNegative['var']=="MDC"){
											$mdcVal=intval($rowNegative['actual']);
											$result = mysqli_query($con,"select description from mdcMap where id='".$mdcVal."'");
											$row=mysqli_fetch_array($result);
											echo "<td><input id=\"top".$j."Val\" value=\"".$row['description']."\" readonly/></td>";
										}else{
											if ($rowNegative['value']==NULL) 
												echo "<td><input id=\"top".$j."Val\" value=\"".$rowNegative['actual']."\" readonly/></td>";
											else 
												echo "<td><input id=\"top".$j."Val\" value=\"".$rowNegative['value']."\" readonly/></td>";
										}
			        					echo "<td><input id=\"top".$j."Var\" value=\"".$rowNegative['var']."\" type=\"hidden\" /></td>";
			        					echo "</tr></table></td>";			
										echo "<td width=\"5%\"><button id=\"top".$j."Minus\" class=\"btn btn-danger\" onclick=\"minus(".$j.");\" ><i class=\"icon-thumbs-down\"></i></button></td>";
									}	
									echo "</tr>";
					
								}	        					
	        					
	        				?>
	        				
	        				<tr><td colspan="6" align="center"><button id="feedBack" class="btn btn-info" type="button" onclick="reset();">Reset</button></td></tr>
	
						</table>
						<br />
	        			<div>
	        					<button id="feedBack" class="btn btn-large btn-primary" type="button" onclick="submit();">Submit Feedback</button>
	        					<button id="story" class="btn btn-warning" onclick="checkStory();">Review Patient</button>
	        			</div>
	        			<br />
	        		</div>
	        		
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
