
<!DOCTYPE HTML>
<html>
	<head>
		<?php
			
			ini_set('max_execution_time', 300);
			// Create connection
			$con=mysqli_connect("localhost","root","root","shands_web");
			
			// Check connection
			if (mysqli_connect_errno($con))
		    {
				echo "Failed to connect to MySQL: " . mysqli_connect_error();
			}
			
			$docID=$_GET['id'];



			$result1 = mysqli_query($con,"select name from userInfo where id='".$docID."'");
			$row=mysqli_fetch_array($result1);
			$docName=$row['name'];


			

		?>
		<title>patients for a Dr.</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
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

			table, th, td {
			 
    			border-style : solid; 
    			outline-color: #0086C4;  
    			border-color: #0086C4;
    			padding:5px;
    			padding-bottom: 20px;
			}

		</style>
		<script type="text/javascript">
        $("document").ready(function() {
            // $("body").append("<p>The page just loaded!</p>");
            $("#here_table").on("click",function(evt){



            });
        });
    </script>


	</head>
    <body>
    	<br />
    	<div id="envelope" class=container align="center" >
	        <div id="headHTML" align="center">
	        		<div align="center"><font color="#ff9900"size="25px">UF Health</font></div>
	        		<!--<th align="right"><input type="search" name="search-patient" placeholder="Search Patient..." /></th>-->
	        </div>
	        		<div id = "patientlist"> 
	        			<h2><!-- <font color="#0086C4" > --> Dr. <?php echo $docName ?>, you will be operating on following patients today. </font></h2>
	        		</div>
	        		
	        		<div id="here_table" align="center"> 
						
						<table width="80%">
	        
							<tr>
	        				<th ><font color="#ff9900"size="6px">Patient IDs</font></th>
	        				<th ><font color="#ff9900"size="6px">Description</font></th>
	        				</tr>

	        			<?php
								
					 
								//echo "<tr><font color =\"#ff9900\" border-color= \"#ff9900\"> Patient ID </font>    </tr> </br>";
					  $i = 0;
					//require 'firstTry.php';

					
	     			file_put_contents("description", $story1);

	     			$result2 = mysqli_query($con,"select id from Patientdetails where feature = 'attend_doc' and value ='".$docID."'");

								while($row=mysqli_fetch_array($result2)){
							 	
							    $PtID[$i]= $row['id'];
							    //echo $PtID[$i];

							    $result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature = 'name'");
								$row=mysqli_fetch_array($result);
								$name=$row['value'];
								//echo $name;

								$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='age'");
								$row=mysqli_fetch_array($result);
					        	$age=$row['value'];
					        	//echo $age;

					        	$result = mysqli_query($con,"select varMap.value value from patientDetails ptDt, varMap where ptDt.id='".$PtID[$i]."' and feature='race' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
								$row=mysqli_fetch_array($result);
					        	$race=$row['value'];
								
								$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='Gender'");
								$row=mysqli_fetch_array($result);
					        	$Gender=$row['value'];

								$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='cci'");
								$row=mysqli_fetch_array($result);
					        	$cci=$row['value'];
								

								if(intval($cci)==0){
									$Combordities="with <b>no known combordities</b>";
								}
								else{
									$result = mysqli_query($con,"select varDef.Description name from patientDetails ptDt, varDef where ptDt.id='".$PtID[$i]."' and ptDt.feature=varDef.id and varDef.type='Comorbidities' and ptDt.Value='1'");
									$row=mysqli_fetch_array($result);
						        	$Combordity=$row['name'];
									$Combordities="has <b>".$cci." combordities, including ".$Combordity;
									while($row=mysqli_fetch_array($result))
										$Combordities=$Combordities.", ".$row['name'];
									$Combordities=$Combordities."</b>";
									
									}

								$result = mysqli_query($con,"select varMap.value value from patientDetails ptDt,varMap where ptDt.id='".$PtID[$i]."' and feature='service' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
								$row=mysqli_fetch_array($result);
					        	$service=$row['value'];
					        	
								$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='Admission_Type'");
								$row=mysqli_fetch_array($result);
					        	$admission_Type=$row['value'];
								
								$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='attend_doc'");
								$row=mysqli_fetch_array($result);
					        	$attend_doc=$row['value'];
								
								$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='pr1'");
								$row=mysqli_fetch_array($result);
					        	$pr1_temp=$row['value'];
								
								$result = mysqli_query($con,"select description value from pr1Map where id='".$pr1_temp."'");
								$row=mysqli_fetch_array($result);
					        	$pr1=$row['value'];
								$pr1 = ($pr1=="") ? "" : "specifically $pr1" ;
								
								$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='MDC'");
								$row=mysqli_fetch_array($result);
					        	$mdcVal=intval($row['value']);

								$result = mysqli_query($con,"select description from mdcMap where id='".$mdcVal."'");
								$row=mysqli_fetch_array($result);
								$MDC=$row['description'];

									$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='pr1_day'");
								$row=mysqli_fetch_array($result);
					        	$pr1_day=$row['value'];
								$pr1_day= ($pr1_day==0)?"Today":$pr1_day." day(s) ago";
					        	
								$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='admit_day'");
								$row=mysqli_fetch_array($result);
					        	$admit_day=$row['value'];
								
								$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='Admission_Source'");
								$row=mysqli_fetch_array($result);
					        	$admission_source= ($row['value']=="unknown") ? "" :$row['value'] ;
					        	
					   //      	$result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='HGB'");
								// $row=mysqli_fetch_array($result);
					   //      	$HGB=$row['value'];
								// $HGB = ($HGB=="") ? "Not Measured" : $HGB."g/dl" ;
								
								// $result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='HCT'");
								// $row=mysqli_fetch_array($result);
					   //      	$HCT=$row['value'];
					   //      	$HCT = ($HCT=="") ? "Not Measures" : $HCT."%" ;
								
								// $result = mysqli_query($con,"select varMap.value value from patientDetails ptDt,varMap where ptDt.id='".$PtID[$i]."' and ptDt.feature='PROTUR' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
								// $row=mysqli_fetch_array($result);
					   //      	$PROTUR=$row['value'];
								// $PROTUR = ($PROTUR=="") ? "Not Measured" : $PROTUR ;
					        	
								// $result = mysqli_query($con,"select varMap.value value from patientDetails ptDt,varMap where ptDt.id='".$PtID[$i]."' and ptDt.feature='GLUURN' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
								// $row=mysqli_fetch_array($result);
					   //      	$GLUURN=$row['value'];
								// $GLUURN = ($GLUURN=="") ? "Not Measured" : $GLUURN ;
								
								// $result = mysqli_query($con,"select varMap.value value from patientDetails ptDt,varMap where ptDt.id='".$PtID[$i]."' and ptDt.feature='HGBUR' and ptDt.feature=varMap.id and varMap.map=ptDt.Value");
								// $row=mysqli_fetch_array($result);
					   //      	$HGBUR=$row['value'];
								// $HGBUR = ($HGBUR=="") ? "Not Measured" : $HGBUR ;
								
								// $result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='noBlood'");
								// $row=mysqli_fetch_array($result);
					   //      	$noBlood=$row['value'];
								// $noBlood = ($noBlood==0) ? "no CBC analysis": $noBlood." blood tests" ;
								
								// $result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='noUrine'");
								// $row=mysqli_fetch_array($result);
					   //      	$noUrine=$row['value'];
								// $noUrine = ($noUrine==0) ? "no urine analysis": $noUrine." urine tests" ;
								
								// $result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='cr_base'");
								// $row=mysqli_fetch_array($result);
					   //      	$cr_base=$row['value'];
								
								
								// $result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='eGFR_epi'");
								// $row=mysqli_fetch_array($result);
					   //      	$eGFR_epi=round($row['value'],2);
								
								// $result = mysqli_query($con,"select value from patientDetails where id='".$PtID[$i]."' and feature='MDRD_Cr'");
								// $row=mysqli_fetch_array($result);
					   //      	$MDRD_Cr=round($row['value'],2);
								
								// $result = mysqli_query($con,"select medicine.Description name from patientDetails ptDt, medicine where ptDt.id='".$PtID[$i]."' and ptDt.feature=medicine.id  and ptDt.Value='1'");
								// $row=mysqli_fetch_array($result);
					   			//      	$Medications=$row['name'];
								// if($Medications=="")
								// 	$Medications="No known medicines";
								// else{
								// 	while($row=mysqli_fetch_array($result))
								// 		$Medications=$Medications." , ".$row['name'];
								// }

							    $story ="Your patient is <b> $name</b>, and is <b> $age year old $race $Gender</b>  $Combordities. The patient was admitted to hospital <b>$pr1_day</b> on <b>$admit_day</b> from <b>$admission_source</b> setting with primary diagnosis related 
	        		to <b>$MDC</b> and is scheduled to have a <b>$admission_Type  $service $pr1</b> by <b>Dr.$docName</b>.";

							    //echo "<td>".$PtID[$i]."</td>"."</br>";
							    echo "<tr>";
							    echo "<td width=\"20%\"><label id=\"ID".$i."\"><a href=\"firstTry.php?id=$PtID[$i]&docid=$docID\">".$PtID[$i]."</a></label></td>";
							    echo "<td width=\"80%\"><label id=\"des".$i."\"><a href= \"firstTry.php?id=$PtID[$i]&docid=$docID\">".$story."</a></label></td>";
							    $i +=1;
							    echo "</tr>";
							 	}
						?>

						</table>
	        		</div>  
	         </br>
	    </div>
	    </body>