<?php 

 class MySQLDao{

 	var $dbhost =null;
 	var $dbuser =null;
 	var $dbpass =null;
 	var $conn =null;
 	var $dbname =null ;
 	var $result = null;


 	function __construct(){
 		$this->dbhost = Conn::$dbhost;
 		$this->dbuser = Conn::$dbuser;
 		$this->dbpass = Conn::$dbpass;
 		$this->dbname = Conn::$dbname;
 	}

 	public function openConnection(){

 		$this->conn = new mysqli($this->dbhost, $this->dbuser, $this->dbpass, $this->dbname);
 		if(mysqli_connect_errno())
 			throw new Exception("Could not establish conncetion with the database");

 	}

 	public function getConnection(){
 		return $this->conn;
 	}

 	public function closeConnection(){
 		if($this->conn != null)
 			$this->conn->close();
 	}

 	public fucntion getUserDetails($email){
 		$returnValue = array();
 		$sql = "Select * from users where user_email='".$email."'";

 		$result = $this->conn->query($sql);
 		if($result != null && (mysqli_num_rows($result)>= 1)) {
 			$row = $result->fetch_array(MYSQLI_ASSOC);
 			if(!empty($row)){
 				$returnValue = $row;

 			}
 			return $returnValue;
 		}

 	public fucntion getUserDetails($email, $userPassword){
 		$returnValue = array();
 		$sql = "Select * from users where user_email='".$email."' and user_password='".$userPassword."'"	;

 		$result = $this->conn->query($sql);
 		if($result != null && (mysqli_num_rows($result)>= 1)) {
 			$row = $result->fetch_array(MYSQLI_ASSOC);
 			if(!empty($row)){
 				$returnValue = $row;

 			}
 			return $returnValue;
 		}

 	public function registerUser($email, $password){
 		$sql = "insert into users set user_email=? , user_password =?";
 		$statement = $this->conn->prepare($sql);
 		
 		if(!$statement)
 			throw new Exception($statement->error);

 		$statement->bind_param("ss", $email, $password);
 		$returnValue = $statement->execute();

 		return $returnValue;
 	}

 	}
 ?>