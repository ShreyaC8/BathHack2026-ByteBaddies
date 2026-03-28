<?php
$servername = "sql8.freesqldatabase.com";
$username = "sql8821562";
$password = "xMe77Ghi88";
$dbname = "sql8821562";
$maxCount = 3;  // max retry
$count = 0;  // current number of retries

while ($count < $maxCount) {

    $conn = new mysqli($servername, $username, $password, $dbname);
    // creates a connection to the server 

    // check connection
    if ($conn->connect_error) {
        $count++;
        echo "Connection failed: " . $conn->connect_error;
        // if connection fails, then the error message is printed and the connection closed.
        sleep(3);  // waits 3 seconds before retrying
    } else {
        echo "Connection successful" . "<br>";

        // This sql statement prepares the SQL query
        $sql = "SELECT UserName, UserID, level FROM users";
        
        // This prepares the preapared statements 
        if ($statement = $conn->prepare($sql)) {
            // Executes the prepared statement
            $statement->execute();
            
            // Gets the result of the query
            $result = $statement->get_result();

            if ($result->num_rows > 0) {
                // Fetch and display results of the SQL query
                while ($row = $result->fetch_assoc()) {
                    echo "UserName: " . $row["UserName"] . "-id: " . $row["UserID"] . "-level: " . $row["level"] . "<br>";
                }
            } else {
                echo "No results";
            }
            
            // Close the statement
            $statement->close();
        } else {
            echo "There's been an error whilst preparing the prepared statement. Try again : " . $conn->error;
        }

        $count = $maxCount;  // stop the while loop when the count equals to the maximum count
    }

    // Close the connection
    $conn->close();
}
?>



