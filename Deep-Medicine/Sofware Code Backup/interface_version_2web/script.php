<?php
	$con=mysqli_connect("localhost","root","shands@UF","medical");
	
	if(isset($_POST['login'])){
		// Check connection
		if (mysqli_connect_errno($con))
	    {
			echo "Failed to connect to MySQL: " . mysqli_connect_error();
		}else{
			$username=$_POST['id'];
			$password=$_POST['pass'];
			
			$result = mysqli_query($con,"select count(*) cnt from userInfo where id='".$username."' and password='".$password."'");
			$row=mysqli_fetch_array($result);
	    	echo $row['cnt'];
		}
		
	}else if(isset($_POST['usercheck'])){
		if (mysqli_connect_errno($con))
	    {
			echo "Failed to connect to MySQL: " . mysqli_connect_error();
		}else{
			$username=$_POST['id'];
			$result = mysqli_query($con,"select count(*) cnt from userInfo where id='".$username."'");
			$row=mysqli_fetch_array($result);
	    	echo $row['cnt'];
		}
		
	}
	else if(isset($_POST['answers'])){
		$ans=$_POST['res'];
		$ans=substr($ans, 0, -1);
		$array = explode(';', $ans);
		//echo $features;
		$i=0;
		$username=$array[14];
		
		for ($i=0; $i < 14 ; $i++) { 
			mysqli_query($con,"insert into doctorTestResults values('".$username."',".$i.",'".$array[$i]."')");
		}
		echo "insert into userInfo values('".$username."','".$array[15]."','".$array[16]."','".$array[17]."','".$array[18]."','".$array[19]."','".$array[20]."')";
		mysqli_query($con,"insert into userInfo values('".$username."','".$array[15]."','".$array[16]."','".$array[17]."','".$array[18]."','".$array[19]."','".$array[20]."')");
		#echo "insert into userInfo values('".$username."','".$array[14]."','".$array[16]."','".$array[17]."','".$array[18]."','".$array[19]."')";
	}
	
	mysqli_close($con);
?>