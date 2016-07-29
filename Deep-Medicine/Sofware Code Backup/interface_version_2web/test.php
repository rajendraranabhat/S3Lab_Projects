<?php
ini_set('max_execution_time', 300);
			// Create connection
			$con=mysqli_connect("localhost","root","shands@UF","medical");
			
			// Check connection
			if (mysqli_connect_errno($con))
		    {
				echo "Failed to connect to MySQL: " . mysqli_connect_error();
			}
			
			
	$story=0;
	for ($i=0; $i < (12*23); $i++) {
		 
		$result = mysqli_query($con,"select count(*) cnt from idList");
			$row=mysqli_fetch_array($result);
        	$cnt=$row['cnt'];
		
			$rand=rand(0,$cnt);
			$result = mysqli_query($con,"select * from idList Limit $rand,1");
			$row=mysqli_fetch_array($result);
        	$ptID=$row['id'];
			
			if($ptID=""){
				$i--;
				continue;
			}
			
			
			$story=$story.$row['id'].",".$row['rifle'].",".$row['icu'].",".$row['mort'].",".$row['mv'].",".$row['cv'].",".$row['sepsis']."\n";;
			echo $story;
			$row=mysqli_fetch_array($result);
			
			mysqli_query($con,"insert into idListDone select * from idList where id='".$ptID."'");
			mysqli_query($con,"delete from idList where id='".$ptID."'");
			
	}
	file_put_contents("prev.csv", $story);
	
	mysqli_close($con);
?>