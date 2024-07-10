<?php
// Define the log file paths
$logFile = 'access.log';
$csvFile = 'openedemail.csv';

// Get the current date and time
$dateTime = date('Y-m-d H:i:s');

// Get the visitor's IP address
$ipAddress = $_SERVER['REMOTE_ADDR'];

// Check if IP address already exists in the log
$logContents = file_get_contents($logFile);
if (strpos($logContents, $ipAddress) !== false) {
    // If IP address exists, do not log again
    exit(); // Optionally, you can choose to exit the script or perform other actions
}

// Get the referring page, if available
$referrer = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'Unknown';

// Get the device type, if available
$userAgent = $_SERVER['HTTP_USER_AGENT'];
$deviceType = getDeviceType($userAgent);

// Generate a unique identifier for this access
$uniqueIdentifier = uniqid();

// Construct the log message
$logMessage = "$dateTime - IP: $ipAddress, Device Type: $deviceType, Referrer: $referrer, Unique ID: $uniqueIdentifier\n";

// Write the log message to the log file
file_put_contents($logFile, $logMessage, FILE_APPEND | LOCK_EX);

// Append the log data to the CSV file
$csvData = [$dateTime, $ipAddress, $deviceType, $referrer, $uniqueIdentifier];
$csvFileHandle = fopen($csvFile, 'a');
fputcsv($csvFileHandle, $csvData);
fclose($csvFileHandle);

// Output a transparent pixel image
header("Content-Type: image/png");
header("Cache-Control: no-cache, no-store, must-revalidate"); // Prevent caching by the browser
echo base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAgEBAYoLRtIAAAAASUVORK5CYII=');

function getDeviceType($userAgent) {
    $deviceTypes = array(
        'Windows Phone' => 'Windows Phone',
        'Windows NT' => 'Windows PC',
        'iPhone' => 'iPhone',
        'iPad' => 'iPad',
        'Macintosh' => 'Mac',
        'Android' => 'Android',
        'Linux' => 'Linux PC',
    );

    foreach ($deviceTypes as $key => $value) {
        if (strpos($userAgent, $key) !== false) {
            return $value;
        }
    }

    return 'Unknown';
}
?>
