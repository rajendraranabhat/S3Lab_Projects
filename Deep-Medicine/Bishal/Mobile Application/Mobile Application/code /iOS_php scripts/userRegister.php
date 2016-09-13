<?php 

require("Conn.php");
require("MySQLDao.php");

$email = htmlentities($_POST["email"]);
$password = htmlentities($_POST["password"]);

echo $email;

$returnValue = array();

if(empty($email)|| empty($password)){
	$returnValue["status"] = "error";
	$returnValue["message"] = "Missing required field";
	echo json_encode($returnValue);
	return;

}

$dao = new MySQLDao();
$dao->openConnection();
$userDetails=$dao->getUserDetails($email);

if(!empty($userDetails)){

	$returnValue["status"] ="error";
	$returnValue["message"] ="User Already exists";
	echo json_encode($returnValue);
	return;


}

$secured_password = md5($password);

$result = $dao->registerUser($email, $secure_password);

if($result){
	$returnValue["status"] ="success";
	$returnValue["message"] = "User is successfully registered";
     echo json_encode($returnValue);
     return;
}

$dao->closeConnection();

?>


