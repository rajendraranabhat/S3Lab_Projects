<!DOCTYPE HTML>
<html>
	<head>
		<title>Register</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
	    <script   src="https://code.jquery.com/jquery-3.1.0.min.js"   integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s="   crossorigin="anonymous"></script>
	    <script src="https://code.jquery.com/jquery.js"></script>
	    <script src="/js/bootstrap.min.js"></script>
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
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
			
			#table
			{
				table-layout: fixed;
				border-collapse:separate;
				border-spacing: 200px;
			}
			
			#td
			{
				border-collapse:separate;
				border-spacing: 200px;
				border-bottom: 100px;
			}
			
			#input{
				width: 2500px;
			}
		</style>
		<script>
			USER_EXIST=-1;
			function goto(varPage){
				$('#tab a[href="#tab'+varPage+'"]').tab('show');
			}
			
			function checkUser(){
				username=$('#question15').val();
				$.post("script.php",  { id: username, usercheck:"true"},
					function (result) {   
					    if (result==1) {
					    	$('#error').show();	
							$('#errorLabel').text(username+" already exists!");
							USER_EXIST=0;
					    } else if (result==0) {
					    	USER_EXIST=1;
					    } else{
					    	$('#error').show();	
							$('#errorLabel').text(result);
							USER_EXIST=-1;
					    }
					    
					  });
			}
			
			function submit(){
				if(USER_EXIST==0){
					return;
				}
				var result="";
				var error=""
				for (var i=1;i<=22;i++)
				{
					result=result+$('#question'+i).val()+";";
					if($('#question'+i).val()==""){
						error=error+i+",";
					}
							
				} 
				if (error!="") {
					error=error.substring(0,error.length - 1);
					$('#error').show();	
					$('#errorLabel').text("Please answer question numbers "+error+" to register successfully");
				}else{
					username=$('#question15').val();
					$.post("script.php",  { res: result, answers:"true"},
						function (result) {   
						  		window.location.href = "index.html";			    
						  });
				}
			}

			</script>
	</head>
    <body>
		        	
    	<br />
    	<div id="envelope" class="container" align="center" >
	        <div id="headHTML" align="center">
	        		<div align="center"><font color="#ff9900"size="20px">UF Health</font></div>
	        </div>
	        <br />
	        <div id="error"class="alert alert-error" hidden>
		    	<label id="errorLabel">Fill in the following information</label>
		    </div>
	        <div class="testTab" style="margin-bottom: 18px;">
              	<ul class="nav nav-tabs" id="tab">
	                <li class="active"><a href="#tab1" data-toggle="tab">Numeracy Test</a></li>
	                <li><a href="#tab2" data-toggle="tab">Expanded Numeracy Test</a></li>
	                <li><a href="#tab3" data-toggle="tab">CRT Test</a></li>
	                <li><a href="#tab4" data-toggle="tab">Personal Information</a></li>
              	</ul>
              	<div class="tab-content" style="padding-bottom: 9px; border-bottom: 1px solid #ddd;">
	            	<div class="tab-pane active" id="tab1">
	                	<table class="table table-striped" width="80%">
		                  	<col width="60%" />
		                  	<col width="20%" />
		                  	<tr>
		                  		<td>
		                  			1.Imagine that we rolled a fair, six-sided die 1,000 times. Out of 1,000 rolls, how many times do you think the die would come up even (2, 4, or 6)?
		                  		</td>
		                  		<td>
		                  			    <div class="input-append">
										    <input class="span2" id="question1" type="text">
										    <span class="add-on"> out of 1000</span>
									    </div>
		                  		</td>
		                  	</tr>
		                  	
		                  	<tr>
		                  		<td>
		                  			2.In the BIG BUCKS LOTTERY, the chances of winning a $10.00 prize is 1%. What is your best guess about how many people would win a $10.00 prize if 1,000 people each buy a single ticket to BIG BUCKS?
		                  		</td>
		                  		<td>
		                  			    <div class="input-append">
										    <input class="span2" id="question2" type="text">
										    <span class="add-on"> out of 1000</span>
									    </div>
		                  		</td>
		                  	</tr>
		                  	
		                  	<tr>
		                  		<td>
		                  			3.In the ACME PUBLISHING SWEEPSTAKES, the chance of winning a car is 1 in 1,000. What percent of tickets to ACME PUBLISHING SWEEPSTAKES win a car? 	
		                  		</td>
		                  		<td>
		                  			    <div class="input-append">
										    <input class="span2" id="question3" type="text">
										    <span class="add-on">%</span>
									    </div>
		                  		</td>
		                  	</tr>
	                	</table>
	                	<table width="100%">
	                		<tr>
	                			<td align="right"><button class="btn btn-primary" type="button" onclick="goto(2)">Next</button></td>
	                		</tr>
	                	</table>
                	</div>
	                <div class="tab-pane" id="tab2">
	                  <table class="table table-striped" width="80%">
		                  	<col width="60%" />
		                  	<col width="20%" />
		                  	<tr>
		                  		<td>
		                  			4.Which of the following numbers represents the biggest risk of getting a disease?   
		                  		</td>
		                  		<td>
		                  			<select id="question4">
		                  				<option></option>
										<option>1 in 10</option>
										<option>1 in 100</option>
										<option>1 in 1000</option>
									</select>
		                  		</td>
		                  	</tr>
		                  	
		                  	<tr>
		                  		<td>
		                  			5.Which of the following numbers represents the biggest risk of getting a disease?  
		                  		</td>
		                  		<td>
	                  			    <select id="question5">
	                  			    	<option></option>
										<option>1%</option>
										<option>10%</option>
										<option>5%</option>
									</select>
		                  		</td>
		                  	</tr>
		                  	
		                  	<tr>
		                  		<td>
		                  			6.If Person A's risk of getting a disease is 1% in ten years, and person B's risk is double that of A's, what is B's risk?   	
		                  		</td>
		                  		<td>
		                  			    <div class="input-append">
										    <input class="span14" id="question6" type="text">
										    <span class="add-on"> %</span>
									    </div>
		                  		</td>
		                  	</tr>
		                  	
		                  	<tr>
		                  		<td>
		                  			7.If Person A's chance of getting a disease is 1 in 100 in ten years, and person B's risk is double that of A's, what is B's risk?  	
		                  		</td>
		                  		<td>
		                  			    <div class="input-append">
										    <input class="span14" id="question7" type="text">
										    <span class="add-on"> out of 100</span>
									    </div>
		                  		</td>
		                  	</tr>
		                  	
		                  	<tr>
		                  		<td>
		                  			8 and 9.If the chance of getting a disease is 10%, how many people would be expected to get the disease?  	
		                  		</td>
		                  		<td>
		                  			    <div class="input-append">
										    <input class="span14" id="question8" type="text">
										    <span class="add-on"> Out of 100</span>
									    </div>
		                
		                  			    <div class="input-append">
										    <input class="span14" id="question9" type="text">
										    <span class="add-on"> Out of 1000</span>
									    </div>
		                  		</td>
		                  	</tr>
		                  	
		                  	<tr>
		                  		<td>
		                  			10.If the chance of getting a disease is 20 out of 100, this would be the same as having a ____% chance of getting the disease  	
		                  		</td>
		                  		<td>
		                  			<input class="span14" id="question10" type="text">
		                  		</td>
		                  	</tr>
		                  	
		                  	<tr>
		                  		<td>
		                  			11.The chance of getting a viral infection is .0005. Out of 10,000 people, about how many of them are expected to get infected?   	
		                  		</td>
		                  		<td>
		                  			    <div class="input-append">
										    <input class="span14" id="question11" type="text">
										    <span class="add-on"> people</span>
									    </div>
		                  		</td>
		                  	</tr>
	                	</table>
	                	<table width="100%">
	                		<tr>
	                			<td align="left"><button class="btn btn-primary" type="button" onclick="goto(1)">Previous</button></td>
	                			<td align="right"><button class="btn btn-primary" type="button" onclick="goto(3)">Next</button></td>
	                		</tr>
	                	</table>
	                </div>
	                
	                <div class="tab-pane" id="tab3">
	                	<table class="table table-striped" width="80%">
		                  	<col width="60%" />
		                  	<col width="20%" />
		                  	<tr>
		                  		<td>
		                  			12.A bat and a ball cost $1.10 in total. The bat cost $1.00 more than the ball. How much does the ball cost?
		                  		</td>
		                  		<td>
		                  			    <div class="input-append">
										    <input class="span2" id="question12" type="text">
										    <span class="add-on"> cents</span>
									    </div>
		                  		</td>
		                  	</tr>
		                  	
		                  	<tr>
		                  		<td>
		                  			13.If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?
		                  		</td>
		                  		<td>
		                  			    <div class="input-append">
										    <input class="span2" id="question13" type="text">
										    <span class="add-on"> minutes</span>
									    </div>
		                  		</td>
		                  	</tr>
		                  	
		                  	<tr>
		                  		<td>
		                  			14.In a lake there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how long would it take for the patch to cover half of the lake?  	
		                  		</td>
		                  		<td>
		                  			    <div class="input-append">
										    <input class="span2" id="question14" type="text">
										    <span class="add-on"> days</span>
									    </div>
		                  		</td>
		                  	</tr>
	                	</table>
	                	<table width="100%">
	                		<tr>
	                			<td align="left"><button class="btn btn-primary" type="button" onclick="goto(2)">Previous</button></td>
	                			<td align="right"><button class="btn btn-primary" type="button" onclick="goto(4)">Next</button></td>
	                		</tr>
	                	</table>
	                </div>
	                <div class="tab-pane" id="tab4">
	                	<table class="table table-striped" width="80%">
		                  	<col width="60%" />
		                  	<col width="20%" />
	                	</table>
	                	<table width="100%">
	                		<tr>
	                			<td>
		                  			15.Full Name  	
		                  		</td>
		                  		<td>
									<input class="span14" id="question22" type="text">  
		                  		</td>
		                  	</tr>
	                      	<tr>
	                			<td>
		                  			15.User Name  	
		                  		</td>
		                  		<td>
									<input class="span14" id="question15" type="text" onblur="checkUser();">  
		                  		</td>
		                  	</tr>
		                  	<tr>
	                			<td>
		                  			16.Password  	
		                  		</td>
		                  		<td>
									<input class="span14" id="question16" type="password">  
		                  		</td>
		                  	</tr>
		                  	<tr>
	                			<td>
		                  			17.Gender   	
		                  		</td>
		                  		<td>
									<select id="question17">
										<option>Male</option>
										<option>Female</option>
									</select>
		                  		</td>
		                  	</tr>
		                  	<tr>
	                		<td>
		                  			18.Age   	
		                  		</td>
		                  		<td>
									<select id="question18">
										<option>30 years or less</option>
										<option>31 years TO 40 years</option>
										<option>41 years TO 50 years</option>
										<option>51 years TO 60 years</option>
										<option>more than 60 years</option>
									</select>
		                  		</td>
		                  	</tr>
		                  	<tr>
	                			<td>
		                  			19.Current Role   	
		                  		</td>
		                  		<td>
									<select id="question19">
										<option>Attending Doctor</option>
										<option>Resident</option>
									</select>
		                  		</td>
		                  	</tr>
		                  	<tr>
	                			<td>
		                  			20.Speciality  	
		                  		</td>
		                  		<td>
									<select id="question20">
										<option>ER</option>
										<option>Medicine</option>
										<option>Surgery</option>
										<option>Anesthesiology</option>
									</select>  
		                  		</td>
		                  	</tr>
		                  	<tr>
	                			<td>
		                  			21.Number of years since graduation from Medical school  	
		                  		</td>
		                  		<td>
									<input class="span14" id="question21" type="text">  
		                  		</td>
		                  	</tr>
	                			<td align="left"><button class="btn btn-primary" type="button"  onclick="goto(3)">Previous</button></td>
	                		</tr>
	                	</table>
	                </div>
	                <button class="btn btn-large btn-primary" type="button"  onclick="submit()">Register</button>
              	</div>
            </div>
        <br /> 
    	</div>  
    </body>
</html>
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

