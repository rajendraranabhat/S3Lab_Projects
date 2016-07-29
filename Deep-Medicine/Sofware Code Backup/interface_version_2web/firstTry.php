<!DOCTYPE HTML>
<html>
	<head>
		<?php
			
			ini_set('max_execution_time', 300);
			// Create connection
			$con=mysqli_connect("localhost","root","shands@UF","medical");
			
			// Check connection
			if (mysqli_connect_errno($con))
		    {
				echo "Failed to connect to MySQL: " . mysqli_connect_error();
			}
			

			$docID=$_GET['id'];
			$result = mysqli_query($con,"select count(*) cnt from idList");
			$row=mysqli_fetch_array($result);
        	$cnt=$row['cnt'];
			
			$rand=rand(0,$cnt);
			$result = mysqli_query($con,"select id from idList Limit $rand,1");
			$row=mysqli_fetch_array($result);
        	$ptID=$row['id'];
			
			$result = mysqli_query($con,"select count(attempt) attempt from indexPatient where user='".$docID."'");
			$row=mysqli_fetch_array($result);
			$noOfAttempt=$row['attempt'];
			$noOfAttempt=intval($noOfAttempt)+1;	
		
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='age'");
			$row=mysqli_fetch_array($result);
        	$age=$row['value'];
			
			$result = mysqli_query($con,"select varMap.value value from patientDetails ptDt, varMap where ptDt.id='".$ptID."' and feature='race' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
			$row=mysqli_fetch_array($result);
        	$race=$row['value'];
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='Gender'");
			$row=mysqli_fetch_array($result);
        	$Gender=$row['value'];
			
			# pt has XX (CCI number ) of comorbidities including
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='cci'");
			$row=mysqli_fetch_array($result);
        	$cci=$row['value'];
			
			if(intval($cci)==0){
				$Combordities="with <b>no known combordities</b>";
			}
			else{
				$result = mysqli_query($con,"select varDef.Description name from patientDetails ptDt, varDef where ptDt.id='".$ptID."' and ptDt.feature=varDef.id and varDef.type='Comorbidities' and ptDt.Value='1'");
				$row=mysqli_fetch_array($result);
	        	$Combordity=$row['name'];
				$Combordities="has <b>".$cci." combordities, including ".$Combordity;
				while($row=mysqli_fetch_array($result))
					$Combordities=$Combordities.", ".$row['name'];
				$Combordities=$Combordities."</b>";
				
			}
			
			$result = mysqli_query($con,"select varMap.value value from patientDetails ptDt,varMap where ptDt.id='".$ptID."' and feature='service' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
			$row=mysqli_fetch_array($result);
        	$service=$row['value'];
        	
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='Admission_Type'");
			$row=mysqli_fetch_array($result);
        	$admission_Type=$row['value'];
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='attend_doc'");
			$row=mysqli_fetch_array($result);
        	$attend_doc=$row['value'];
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='pr1'");
			$row=mysqli_fetch_array($result);
        	$pr1_temp=$row['value'];
			
			$result = mysqli_query($con,"select description value from pr1Map where id='".$pr1_temp."'");
			$row=mysqli_fetch_array($result);
        	$pr1=$row['value'];
			$pr1 = ($pr1=="") ? "" : "specifically $pr1" ;
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='MDC'");
			$row=mysqli_fetch_array($result);
        	$mdcVal=intval($row['value']);
			$result = mysqli_query($con,"select description from mdcMap where id='".$mdcVal."'");
			$row=mysqli_fetch_array($result);
			$MDC=$row['description'];
			
						
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='pr1_day'");
			$row=mysqli_fetch_array($result);
        	$pr1_day=$row['value'];
			$pr1_day= ($pr1_day==0)?"Today":$pr1_day." day(s) ago";
        	
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='admit_day'");
			$row=mysqli_fetch_array($result);
        	$admit_day=$row['value'];
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='Admission_Source'");
			$row=mysqli_fetch_array($result);
        	$admission_source= ($row['value']=="unknown") ? "" :$row['value'] ;
        	
        	$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='HGB'");
			$row=mysqli_fetch_array($result);
        	$HGB=$row['value'];
			$HGB = ($HGB=="") ? "Not Measured" : $HGB."g/dl" ;
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='HCT'");
			$row=mysqli_fetch_array($result);
        	$HCT=$row['value'];
        	$HCT = ($HCT=="") ? "Not Measures" : $HCT."%" ;
			
			$result = mysqli_query($con,"select varMap.value value from patientDetails ptDt,varMap where ptDt.id='".$ptID."' and ptDt.feature='PROTUR' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
			$row=mysqli_fetch_array($result);
        	$PROTUR=$row['value'];
			$PROTUR = ($PROTUR=="") ? "Not Measured" : $PROTUR ;
        	
			$result = mysqli_query($con,"select varMap.value value from patientDetails ptDt,varMap where ptDt.id='".$ptID."' and ptDt.feature='GLUURN' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
			$row=mysqli_fetch_array($result);
        	$GLUURN=$row['value'];
			$GLUURN = ($GLUURN=="") ? "Not Measured" : $GLUURN ;
			
			$result = mysqli_query($con,"select varMap.value value from patientDetails ptDt,varMap where ptDt.id='".$ptID."' and ptDt.feature='HGBUR' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
			$row=mysqli_fetch_array($result);
        	$HGBUR=$row['value'];
			$HGBUR = ($HGBUR=="") ? "Not Measured" : $HGBUR ;
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='noBlood'");
			$row=mysqli_fetch_array($result);
        	$noBlood=$row['value'];
			$noBlood = ($noBlood==0) ? "no CBC analysis": $noBlood." blood tests" ;
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='noUrine'");
			$row=mysqli_fetch_array($result);
        	$noUrine=$row['value'];
			$noUrine = ($noUrine==0) ? "no urine analysis": $noUrine." urine tests" ;
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='cr_base'");
			$row=mysqli_fetch_array($result);
        	$cr_base=$row['value'];
			
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='eGFR_epi'");
			$row=mysqli_fetch_array($result);
        	$eGFR_epi=round($row['value'],2);
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='MDRD_Cr'");
			$row=mysqli_fetch_array($result);
        	$MDRD_Cr=round($row['value'],2);
			
			$result = mysqli_query($con,"select medicine.Description name from patientDetails ptDt, medicine where ptDt.id='".$ptID."' and ptDt.feature=medicine.id  and ptDt.Value='1'");
			$row=mysqli_fetch_array($result);
        	$Medications=$row['name'];
			if($Medications=="")
				$Medications="No known medicines";
			else{
				while($row=mysqli_fetch_array($result))
					$Medications=$Medications." , ".$row['name'];
			}
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='county'");
			$row=mysqli_fetch_array($result);
        	$county=$row['value'];
        		
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='area'");
			$row=mysqli_fetch_array($result);
        	$area=$row['value'];
			
			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='med_inc'");
			$row=mysqli_fetch_array($result);
        	$med_inc=$row['value'];

			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='total'");
			$row=mysqli_fetch_array($result);
        	$total=$row['value'];

			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='Prop_pov'");
			$row=mysqli_fetch_array($result);
        	$Prop_pov=round($row['value']*100,2);


			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='prop_black'");
			$row=mysqli_fetch_array($result);
        	$prop_black=round($row['value']*100,2);

			$result = mysqli_query($con,"select value from patientDetails where id='".$ptID."' and feature='prop_hisp'");
			$row=mysqli_fetch_array($result);
        	$prop_hisp=round($row['value']*100,2);

			$result = mysqli_query($con,"select varMap.value value from patientDetails ptDt,varMap where ptDt.id='".$ptID."' and ptDt.feature='pay_grp' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
			$row=mysqli_fetch_array($result);
        	$pay_grp=$row['value'];
        	
        	$result = mysqli_query($con,"select description from outcomes order by id");        	
        	$i=0;
        	while($row=mysqli_fetch_array($result)){
				$labels[$i] = $row['description'];
				$i=$i+1;
			}
        	$net_decisions=$i;
        	
			echo "$noOfAttempt of 14";
			
		?>

		<title>What do you think?</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
	    <script src="http://code.jquery.com/jquery.js"></script>
	    <script src="js/bootstrap.min.js"></script>
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
		<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
		<script src="http://code.jquery.com/jquery-1.9.1.js"></script>
		<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
		<link rel="stylesheet" href="/resources/demos/style.css" />
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
				
				border-radius:20px;
				border-color: #0086C4;
				border-style: solid; 
				width: 99%;
			}
			
			<?php echo "#outcomes[0]" ?>
			{
				width: 65%;
				background-image: linear-gradient(to right, #00FF00 0%,#FFFF00 25%,#FFA500 75%, #FF0000 100%);
				margin: 0 auto;
			}
			
			#bar
			{
				width:80%;
				padding:5px;
				padding-top:2px;
				text-align:center; 
			}
			
			#submit{
				color: #ffffff;
				background-color: #0044cc;
			}

		</style>
		
			<script> 
				var starTime=0;
				$(function() {
	    			<?php
	    			for ($i=0; $i < $net_decisions; $i++) { 
							echo "$( '#docPredict$i' ).slider({
		        		value:50,
		        		min: 0,
		        		max: 100,
		        		step: 1,
		        		
		        		
		        		slide: function( event, ui ) {
						    $( '#docPredictVal$i' ).text( ui.value );
						    $(ui.value).val($('#docPredictVal$i').text());
							$( '#docPredictDisp$i' ).text(\"Your Prediction is \"+$('#docPredictVal$i').text()+\"%\");
							$( '#docPredictDisp$i' ).css('font-weight', 'bold');
					    }
					});";}
	    			?>	
	    			
	    			startTime=Date.now();
				});
				
				function submit(){
					var id="<?php echo $ptID?>";
					var doc="<?php echo "$docID"?>";
					var val=$( '#docPredictVal0' ).text();
					for (var i=1; i < <?php echo "$net_decisions"?>; i++) {
					  val+=","+$( '#docPredictVal'+i ).text();
					};
					var time=(Date.now()-startTime)/1000;
					window.location.href = "submit.php?attempt1=true&user="+doc+"&id="+id+"&docPredict="+val+"&time="+time;	
				}

			</script>
		</head>
    <body>
    	<br />
    	<div id="envelope" class=container align="center" >
	        <div id="headHTML" align="center">
	        		<div align="center"><font color="#ff9900"size="25px">UF Health</font></div>
	        		<!--<th align="right"><input type="search" name="search-patient" placeholder="Search Patient..." /></th>-->
	        </div> 
	        <?php
	        	$story1="Your patient is <b>$age year old $race $Gender</b>  $Combordities. The patient was admitted to hospital <b>$pr1_day</b> on <b>$admit_day</b> from <b>$admission_source</b> setting with primary diagnosis related 
	        		to <b>$MDC</b> and is scheduled to have a <b>$admission_Type  $service $pr1</b> by <b>Dr.$attend_doc</b>. On admission there were <b>$noBlood</b> and <b>$noUrine</b> done, and 
	        		the laboratories values are Hgb <b>$HGB</b>, Hct <b>$HCT</b>, urine protein <b>$PROTUR</b>, urine glucose <b>$GLUURN</b>, urine blood <b>$HGBUR</b>. The patient's serum creatinine on admission was <b>$cr_base mg/dl</b> with calculated estimated GFR of <b>
	     			$eGFR_epi ml/min/1.72m2</b> while estimated baseline creatinine using age, gender, and race with MDRD equation is <b>$MDRD_Cr </b>. Admission medications are: <b>$Medications</b>.";
	     			
	     		$story2="Patient has <b>$pay_grp</b> insurance and resides in <b>$county</b> county in  <b>$area</b>  area with total population of <b>$total</b> . The percentage of African-Americans and Hispanics in his neighborhood is 
	     			<b>$prop_black% and $prop_hisp%</b> respectively. The overall median income for his neighborhood is <b>$med_inc $</b> and <b>$Prop_pov%</b>  of population lives below poverty level.";
	     			
	     		file_put_contents("story1", $story1);
	     		file_put_contents("story2", $story2);
	        ?>
	        <p>
	     		<?php 
	     			echo $story1;	
	     		?>
	        </p>
	        
	        <p>
	        	<?php
	     			echo $story2;
				?>
	        </p>
	        
	        
	        <br />
	        <b>On the scale from 0 ("no chance") to 100 ("certainty") what is your estimate of the likelihood for this patient to develop following complications in the first seven days after surgery?</b> 
			<br />
			Please  touch screen on each of the scale below to assign corresponding risk for this patient.
	        <div id="bar" align="center">
	        	<table align="center" width="95%">
	        		
  				<?php
  					for ($i=0; $i < $net_decisions ; $i++) {
  						echo "<tr><td align=\"center\">"; 
						echo "<p><b>$labels[$i]?</b></p>
						<div id=\"docPredict$i\" align=\"center\" style=\"background-image: linear-gradient(to right, #00FF00 0%,#FFFF00 25%,#FFA500 75%, #FF0000 100%); width:65%\" ></div>
		       			<label id=\"docPredictVal$i\" style=\"display:none\">50</label>
		       			<p><label id=\"docPredictDisp$i\" style=\"font-weight:bold\">Your Prediction is 50%</label></p>";
						echo "</td></tr>";	  
					}
        			
        		?>
        		</table>
        		<button name="submit" class="btn btn-primary btn-large" onclick="submit()">SUBMIT</button>
        		<!--<div id=\"docPredictICU\" ></div>
		        			<label id=\"docPredictValICU\" style=\"font-weight:bold\" hidden>50</label>
		        			<p><label id=\"docPredictValICUval\" style=\"font-weight:bold\">Your Prediction is 50%</label></p> -->
        	</div>
        </div>  
    </body>
    <?php
       		mysqli_close($con);
    ?>
</html>
