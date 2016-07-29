<!DOCTYPE HTML>
<html>
	<head>
		<?php
			ini_set('max_execution_time', 300);
			$con=mysqli_connect("localhost","root","shands@UF","medical");
			
			// Check connection
			if (mysqli_connect_errno($con))
		    {
				echo "Failed to connect to MySQL: " . mysqli_connect_error();
			}
			
			$ptID=$_GET['id'];
			$attempt1=$_GET['docValue'];
			
			//$results=mysqli_query($con,"insert into docPredictICU values('".$id."','".$attempt1."','')");
			
		?>
		<title>Here is what we think</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="/css/bootstrap.min.css" rel="stylesheet" media="screen">
	    <script src="http://code.jquery.com/jquery.js"></script>
	    <script src="/js/bootstrap.min.js"></script>
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
				border-radius:25px;
				border-color: #0086C4;
				border-style: solid; 
			}
			
			#pbarICU,#pbarICU{
				width: 75%;
				margin: 0 auto;
			}
			
			
		</style>
		
		<script>
			   
		    function submit(){
		    	var i=1;
		    	var features=""; 
		    	var id="<?php echo $ptID ?>"
		    	var attempt1="<?php echo $attempt1 ?>"
		    	while(i<=10){
		    		var component="#top"+i+"Val";
		    		if(!$(component).prop('disabled'))
		    			features+=$('#top'+i+'Var').val()+":";
		    		i++;
		    	}
		    	
		    	window.location ="reviewResults.php?id="+id+"&attempt1="+attempt1+"&features="+features;
		    }

				
			$(function() {
    			$("#pbarICU").progressbar();
	            $("#pbarICU").bind('progressbarchange', function(event, ui) {
	                var value =this.getAttribute( "aria-valuenow" );
	                
	                var selector = "#" + this.id + " > div";
	           
	                if (value >= 75){
	                    $(selector).css({ 'background': '#FF0000' });
	                } else if (value >= 50){
	                    $(selector).css({ 'background': '#FFA500' });
	                }else if (value >= 25){
	                    $(selector).css({ 'background': '#FFFF00' });
	                }else{
	                    $(selector).css({ 'background': '#00FF00' });
	                }
	                
	            });
	            var val=parseInt($('#mcPredictICU').text());
				$("#pbarICU").progressbar({ "value":val});		    
			});		    
			
			function plus(var1){
		    	var plusBttn="#top"+var1+"Plus";
		    	var minusBttn="#top"+var1+"Minus";
		    	var val="#top"+var1+"Val";
		    	var label="#top"+var1	    	
		    	$(plusBttn).attr("disabled", "disabled");
		    	$(val).removeAttr("disabled");
		    	$(minusBttn).removeAttr("disabled");
		    	$(label).css({color:"black"})
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
			
		</script>
		
		</head>
	    <body>
	    	<div id="envelope" class=container align="center" >
		        <div id="headHTML" class="container" align="center">
		        		<div class="span9" align="center"><font color="#ff9900"size="25px">UF&SHANDS</font></div>
		        		<!--<th align="right"><input type="search" name="search-patient" placeholder="Search Patient..." /></th>-->
		        </div>
		        
		        <b>The computer algorithms have calculated that probability risk scores for this patient are:</b> 
		        <br />
		        <div class="container">
			  		<?php
        				$result = mysqli_query($con,"select rifle7 from acctDetailsICU where id='".$ptID."'");
						$row=mysqli_fetch_array($result);
        				$value=$row['rifle7'];
        			?>
	        		<p><b>Admission to Intensive Care Unit for longer than 48 hours?</b></p>
	        		<div id='pbarICU' style="height: 10px;"></div>
	        		<p>According to the predictor the chances are <b><label id="mcPredictICU"><?php echo $value?></label>%</b></p>
	        		
        		</div>
        		
        		<div id="tableInfo" align="center" class="container">
        			<p><b>These are the main factors contributing to this patients' risk. Please touch screen next to each factor to see how strongly it contributes to risk. Please agree or disagree with each reason by touching Agree/Disagree button next to it. </b></p>
        			<table width="80%" name="table-1">
        				<?php        					
							mysqli_query($con,"create or replace view tempViewICU as Select val.var var, details.name name, val.value value From acctValuesICU val, acctRankingICU rank, varDetails details Where val.id='$ptID'and val.id=rank.id and val.var=rank.var and val.var=details.var order by rank.rank");
							
							$result = mysqli_query($con,"Select temp.var var,temp.name name,temp.value map, val.value value from tempViewICU temp left outer join varValues val on (temp.var=val.var and temp.value=val.map)");
							$i=1;
							while($row = mysqli_fetch_array($result))
							{
								echo "<tr>";
		        				echo "	<td><label id=\"top".$i."\">".$row['name']."</label></td>";
								if ($row['value']!=NULL) 
									echo "	<td><input id=\"top".$i."Val\" value=\"".$row['value']."\" readonly/></td>";	
								else 
									echo "	<td><input id=\"top".$i."Val\" style={width:35%} value=\"".$row['map']."\" readonly/></td>";
								echo "	<td><input id=\"top".$i."Var\" value=\"".$row['var']."\" hidden /></td>";
		        				echo "	<td><button id=\"top".$i."Plus\" onclick=\"plus(".$i.");\" disabled>+</button></td>";
		        				echo "	<td><button id=\"top".$i."Minus\" onclick=\"minus(".$i.");\" >-</button></td>";
		        				echo "</tr>";
								$i=$i+1;
							}	
							mysqli_query($con,"drop view tempView");
						?>
						</table>
        			<div>
        					<button id="feedBack" onclick="submit();">Submit Feedback</button>
        			</div>
        		</div>
	        </div>  
	    </body>
	     <?php
       		mysqli_close($con);
       	?>

</html>
