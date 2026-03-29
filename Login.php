<?php
$servername = "sql8.freesqldatabase.com";
$username = "sql8821562";
$password = "xMe77Ghi88";
$dbname = "sql8821562";
$maxCount = 3;  // max retry
$count = 0;  // current number of retries

// users login details
$UserLogin = $_POST["UserLogin"];
$LoginPass = $_POST["LoginPass"];

while ($count<$maxCount){

    $conn = new mysqli($servername,$username,$password,$dbname);
    // Establishes a connection to the server 

    // to check connection 
    if ($conn->connect_error){ 
        $count++;
        echo "connection failed".$conn->connect_error;
        // if connection failes then ther error message is printed and the connection closes.
        sleep(3);// waits 3 seconds before retrying 
        if ($count >= $maxCount) {
            echo "Login failed. Maximum retries reached.";
            break; // Exit the loop after reaching the max retries
        }
    }
    else {
        // to prevent SQL injection prepared statements are used 
        $sql = "SELECT UserID, Password FROM users WHERE UserName =?";
        // writes query to select the data in the fields in the table users.
        $statement =$conn->prepare($sql); // the sql is being prepared using this command
        $statement -> bind_param("s",$UserLogin); // bind parameter used to replace the question mark with the parameter of type string 
        $statement-> execute(); // the prepared statement is executed 
        $result =$statement-> get_result();  
        // result from the connection $conn, which runs the query $sql is returned 
        if ($result-> num_rows>0){
            while ($row=$result-> fetch_assoc()){
                if(password_verify($LoginPass, $row["Password"])){
                    echo "login successful" ;
                
                    session_start(); // starts the session
                    $_SESSION['UserID'] = $row['UserID'];
                    // stores the UserID in a session so it can be called when needed.
                    $conn->close();
                    exit;
                }
                else{
                    echo "Wrong password or username";
                    $count++;
                }
            }}
        else {
           // echo "Username doesn't exist ";
            header("Location:registration.html");
            $count++;

            break;} 
        $conn->close();
       // break; 
            
        
    
    }
    if ($count >=$maxCount ){
        echo "Login failed $maxCount reached";
        break;
    }
    
    
}
?>


