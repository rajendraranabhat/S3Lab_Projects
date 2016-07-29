<?php
	$con=mysqli_connect("localhost","root","shands@UF","medical");
	
	if(isset($_GET['attempt1'])){
		// Check connection
		$username=$_GET['user'];
		$ptID=$_GET['id'];
		$attempts=$_GET['docPredict'];
		$time=$_GET['time'];
		
		$result = mysqli_query($con,"select count(attempt) attempt from indexPatient where user='".$username."'");
		$row=mysqli_fetch_array($result);
		$noOfAttempt=$row['attempt'];
		$noOfAttempt=intval($noOfAttempt);
		if ($noOfAttempt < 1 || ($noOfAttempt >=14 && $noOfAttempt<=14)) {
			$noOfAttempt=$noOfAttempt+1;
			mysqli_query($con,"insert into indexPatient values('".$username."','".$ptID."',".$noOfAttempt.",".$time.")");
			$outcomes=explode(",", $attempts);
			$i=1;
			foreach ($outcomes as $outcome) {
				mysqli_query($con,"insert into outcomeResult values('".$username."','".$ptID."',".$i.",".$outcome.",-1)");
				$i=$i+1;	
			}
			mysqli_query($con,"delete from idList where id='".$ptID."'");
			echo $noOfAttempt;
			if($noOfAttempt=1)
				header( 'Location: LastScreen.php?id='.$username.'&scrnID=1');
			else if($noOfAttempt==15)
				header( 'Location: LastScreen.php?id='.$username.'&scrnID=3');
			else
				header( 'Location: firstTry.php?id='.$username);
		} else {
			file_put_contents("firstTry", $attempts.";".$time);
			#echo "$noOfAttempt";
			header( 'Location: modelResults_v2.php?ptID='.$ptID.'&user='.$username.'&outcome=1' );	
		}	
	}else if(isset($_GET['feedback'])){
		$username=$_GET['user'];
		$ptID=$_GET['id'];
		$outcome=$_GET['outcome'];
		$time=$_GET['time'];
		$features=$_GET['features'];
		$noReview=$_GET['noReview'];
		file_put_contents("screen1_".$outcome, $features.";".$time.";".$noReview);
		header( 'Location: reviewResults.php?ptID='.$ptID.'&user='.$username.'&outcome='.$outcome );
	
	}else if(isset($_GET['recoNeg'])){
			$ptID=$_GET['id'];
			$username=$_GET['user'];
			mysqli_query($con,"insert into recoTakenTable values('".$ptID."','".$username."','no')");
			$time=$_GET['time'];
			
			mysqli_query($con,"insert into outcomeStats values('".$username."','".$ptID."',-1,".$time.",-1,-1,-1)");
			$result = mysqli_query($con,"select count(attempt) attempt from indexPatient where user='".$username."'");
			$row=mysqli_fetch_array($result);
			$noOfAttempt=$row['attempt'];
			
			if($noOfAttempt==14)
				header( 'Location: LastScreen.php?id='.$username.'&scrnID=2');
			else
				header( 'Location: firstTry.php?id='.$username );
	}else if(isset($_GET['recoPos'])){
			$ptID=$_GET['id'];
			$username=$_GET['user'];
			mysqli_query($con,"insert into recoTakenTable values('".$ptID."','".$username."','yes')");
			
			$caseTemp=$_GET['cases'];
			$time=$_GET['time'];
			$cases=substr($caseTemp, 0, -1);
			$cases=explode(";", $cases);
				
			foreach ($cases as $case) {
				if($case!="")
					mysqli_query($con,"insert into recoCaseTable values('".$ptID."','".$username."','".$case."')");
			}

			$recoTemp=$_GET['recos'];
			$recos=substr($recoTemp, 0, -1);
			$recos=explode(";", $recos);
				
			foreach ($recos as $reco) {
				if($reco!="")
					mysqli_query($con,"insert into recoTable values('".$ptID."','".$username."','".$reco."')");
			}
			
			mysqli_query($con,"insert into outcomeStats values('".$username."','".$ptID."',-1,".$time.",-1,-1,-1)");
			$result = mysqli_query($con,"select count(attempt) attempt from indexPatient where user='".$username."'");
			$row=mysqli_fetch_array($result);
			$noOfAttempt=$row['attempt'];
			if($noOfAttempt==11)
				header( 'Location: LastScreen.php?id='.$username.'&scrnID=2');
			else
				header( 'Location: firstTry.php?id='.$username );
			
	}else{
		
		$username=$_GET['user'];
		$ptID=$_GET['id'];
		$outcome=$_GET['outcome'];
		$time=$_GET['time'];
		$attempt2=$_GET['attempt'];
		$noReview=$_GET['noReview'];
		$outcome_next=$outcome+1;
		$result = mysqli_query($con,"select outcome,description from outcomes where id=".$outcome_next);
		$row=mysqli_fetch_array($result);
		$outcomeHold=$row['outcome'];
		file_put_contents("screen2_".$outcome, $attempt2.";".$time.";".$noReview);
		if($outcomeHold==""){
			
			$string=file_get_contents("firstTry");
			$firstArr=explode(";", $string);
			$result = mysqli_query($con,"select count(attempt) attempt from indexPatient where user='".$username."'");
			$row=mysqli_fetch_array($result);
			$noOfAttempt=$row['attempt'];
			$noOfAttempt=$noOfAttempt+1;
			echo "insert into indexPatient values('".$username."','".$ptID."',".$noOfAttempt.",".$firstArr[1].")";
			mysqli_query($con,"insert into indexPatient values('".$username."','".$ptID."',".$noOfAttempt.",".$firstArr[1].")");
			$firstAttempts=explode(",", $firstArr[0]);
			for ($i=1; $i <= $outcome ; $i++) { 
				$screen1String=file_get_contents("screen1_".$i);
				$screen2String=file_get_contents("screen2_".$i);
				
				$screen1Arr=explode(";", $screen1String);
				$screen2Arr=explode(";", $screen2String);
				$features=substr($screen1Arr[0], 0, -1);
				$featureArr=explode(":", $features);
				
				foreach ($featureArr as $feature) {
					if($featureArr!="")
						mysqli_query($con,"insert into outcomeRank values('".$username."','".$ptID."',".$i.",'".$feature."')");
				}
				
				mysqli_query($con,"insert into outcomeResult values('".$username."','".$ptID."',".$i.",".$firstAttempts[$i-1].",".$screen2Arr[0].")");
				mysqli_query($con,"insert into outcomeStats values('".$username."','".$ptID."',".$i.",".$screen1Arr[1].",".$screen2Arr[1].",".$screen1Arr[2].",".$screen2Arr[2].")");	
				
				unlink("screen1_".$i);
				unlink("screen2_".$i);
			}
			mysqli_query($con,"delete from idList where id='".$ptID."'");
			unlink("firstTry");
			unlink("story1");
			unlink("story2");
			header( 'Location: recommendations.php?ptID='.$ptID.'&user='.$username);
			
		}else{
			//echo $outcome_next;
			header( 'Location: modelResults_v2.php?ptID='.$ptID.'&user='.$username.'&outcome='.$outcome_next );
		}
	}
	
	
	#mysqli_close($con);
?>