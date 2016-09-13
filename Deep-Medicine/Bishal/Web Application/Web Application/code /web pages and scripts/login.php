
<!DOCTYPE HTML>
<html>
	<head>
		
		<title>Login</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
	    <script   src="https://code.jquery.com/jquery-3.1.0.min.js"   integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s="   crossorigin="anonymous"></script>
	    <script src="https://code.jquery.com/jquery.js"></script>
	    <script src="js/bootstrap.min.js"></script>
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
				height:40px;
				border-top-left-radius:20px;
				border-top-right-radius:20px; 
			}
			
			#envelope
			{
				
				border-radius:20px;
				border-color: #0086C4;
				border-style: solid; 
				width:50%;				
				alignment-baseline: central;
			}
		</style>
		<script>
			function register(){
				window.location.href = "numeracyTest.php";
			}
			
			function login(){
				username=$('#username').val();
				password=$('#password').val()
				if ($.trim(username)=="" || $.trim(password)=="") {
					$('#error').show();	
					$('#errorLabel').text("Username or Password is missing");
				}else{
					$.post("script.php",  { id: username, pass: password , login:"true"},
					  /* The callback that will get executed once the data is back from the server*/
					  function (result) {   
					    if (result==1) {
					    	window.location.href = "firstTry.php?id="+username;
					    } else if (result==0) {
					    	$('#error').show();	
							$('#errorLabel').text("Username or Password does not match our records");
					    } else{
					    	$('#error').show();	
							$('#errorLabel').text(result);
					    }
					    
					  });
				}
			}
		</script>
		</head>
    <body >
    	
    	<br />
    	<div id="envelope" class="container" align="center" >
	        <div id="headHTML" align="center">
	        		<div align="center"><font color="#ff9900"size="25px">UF Health</font></div>
	        </div>
	        <div id="error"class="alert alert-error" hidden>
		    	<label id="errorLabel"></label>
		    </div>
	        <br />
	        <table align="center">
	        			<tr>
	        				<td>Username</td>
	        				<td><input id="username" class="input-medium" type="text"></td>
	        			</tr>
	        			<tr>
	        				<td>Password</td>
	        				<td><input id="password" class="input-medium" type="password"></td>
	        			</tr>
	        			<tr>
	        				<td><button class="btn" type="button" onclick="register()">Sign Up</button></td>
	        				<td align="right"><button class="btn btn-large btn-primary" type="button" onclick="login();">Login</button></td>
	        			</tr>
	        			
	        </table>
	        <br /> 
        </div> 
         
    </body>
</html>
