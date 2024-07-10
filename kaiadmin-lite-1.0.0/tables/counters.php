<?php

$csvFilePath = '../forms/lodgings.csv';

// Initialize a counter for rows with formatted phone numbers
$count = 0;
$countemails = 0;
$countTOT = 0;

// Open the CSV file for reading
if (($handle = fopen($csvFilePath, 'r')) !== false) {
    // Loop through each row in the CSV file
    while (($data = fgetcsv($handle, 1000, ';')) !== false) {
        // Check if the column with the phone number is formatted
        // Assuming the phone number is in a specific column, e.g., column 8 (index 7)
        $phoneNumber = $data[6];
		$email = $data[10];
    	$total = $data[0];
    
    	if ($total != NULL){
        $countTOT++;
        }
        // Regex pattern to match formatted phone number (e.g., (123) 456-7890)
        // Here you would typically have a regex pattern to check if the phone number is formatted
        if ($email != "x"){
        $countemails++;
        }
        // Increment the counter if the phone number is formatted
        if (strlen($phoneNumber) > 0) {
            $count++;
        }
    }
    // Close the file handle
    fclose($handle);
}

// $count now holds the number of formatted phone numbers

// Prepare JSON response
$response = [
    'phonenumber' => $count,
	'emails' => $countemails,
	'total' => $countTOT
];

// Send JSON response
header('Content-Type: application/json');
echo json_encode($response);
?>
