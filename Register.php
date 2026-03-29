<?php
$servername = "sql8.freesqldatabase.com";
$username = "sql8821562";
$password = "xMe77Ghi88";
$dbname = "sql8821562";
$maxCount = 3;  // max retry
$count = 0;  // current number of retries
// users login details

$UserLogin = $_POST ["UserLogin"]; 
$LoginPass = $_POST ["LoginPass"]; 
$LoginEmail = $_POST ["LoginEmail"]; 

function passwordHashing($password) {
   
    $hash = 0; // initalises hash value to 0 so it's not affected by any previous calculations 
    $prime = 19; // I chose the prime number 19 for hashing to ensure that hash values are distributed hash values more evenly across the table, and to minimise collisions where multiple keys map to the same index. To improve performance for lookups and insertions in the hash table.
 
    for ($i = 0; $i < strlen($password); $i++)// this loops until i is bigger than the length of the password 
    {
        $charValue = ord($password[$i]); // this gets  ASCII value of the character of the password and does this for each character in password as the for loop loops
        $hash = ($hash * $prime + $charValue) | 0xFFFFFFFF; // this applies arithmetic and bitwise operations to produce a hash value 
    }
    return  $hash;
 }
while ($count<$maxCount){

    $conn = new mysqli($servername,$username,$password,$dbname);
    // Establishes a connection to the server 
   
    // to check connection 
    if ($conn->connect_error){
        //$count+= $count; logic error 
        $count++;
        //die("connection failed".$conn->connect_error);logic error
        echo "connection failed".$conn->connect_error;
        // if connection failes then ther error message is printed and the connection closes.
        sleep(3);// waits 3 seconds before retrying 
    }
        else {
        echo "Connection successful"."<br>" ; // if connection successful then database can be accessed and we can make querys.
        $sql =  "SELECT UserName FROM users WHERE UserName = ? OR Email =?";
        // writes query to select the data in the fields in the table users.
        $statement =$conn->prepare($sql); // the sql is being prepared using this command
        $statement -> bind_param("ss",$UserLogin, $Email); // bind parameter used to replace the question mark with the parameter of type string 
        $statement-> execute(); // the preparedstatement is executed 
        $result =$statement-> get_result();
        if ($result-> num_rows>0){
            echo "username or email is taken.";
            } 
        else {
            
            $hashedPassword = passwordHashing($LoginPass);
            
            $sql= "INSERT INTO users (UserName,Password,Email) VALUES (?,?,?)";
            $statement = $conn->prepare($sql);
            $statement->bind_param("sss", $UserLogin, $hashedPassword, $LoginEmail);
            if ($statement-> execute()){
                echo " New user created successfully";
            }
            else{
                echo"Error:".$statement->error;
            }
        }
        $statement->close();
        $conn->close();// closes the connection
        break;// stops the loop as the while loop condition is no longer met
        

    }

    
}
?>
