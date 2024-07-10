<?php
// lodgings.php

// Path to your CSV file
$csvFile = 'lodgings.csv';

// Function to parse CSV rows into an associative array
function parseCSV($csvFile) {
    $file = fopen($csvFile, 'r');
    $headers = fgetcsv($file, 1000, ";"); // Assuming headers are semicolon-separated
    $data = [];

    while (($row = fgetcsv($file, 1000, ";")) !== false) {
        $rowData = [];
        foreach ($headers as $index => $header) {
            $rowData[$header] = isset($row[$index]) ? trim($row[$index]) : ''; // Trim whitespace
        }
        $data[] = $rowData;
    }

    fclose($file);
    return $data;
}

// Parse CSV data
$data = parseCSV($csvFile);

// Determine requested start and length for pagination
$start = isset($_POST['start']) ? intval($_POST['start']) : 0;
$length = isset($_POST['length']) ? intval($_POST['length']) : 10;

// Prepare data subset for the current page
$paginatedData = array_slice($data, $start, $length);

// Format data for DataTables
$output = [
    "draw" => intval($_POST['draw'] ?? 1), // Draw counter
    "recordsTotal" => count($data), // Total records
    "recordsFiltered" => count($data), // Total records after filtering (not implemented here)
    "data" => [] // Initialize an empty array for data
];

// Map CSV data to DataTables expected format
foreach ($paginatedData as $row) {
    $rowData = [
        "Name" => $row["name"],
        "FormattedPhoneNumber" => $row["formatted_phone_number"],
        "Vicinity" => $row["vicinity"],
        "Email" => $row["Email"],
        "Website" => $row["website"]
        // Add more fields as needed
    ];
    $output["data"][] = $rowData;
}

// Output JSON
header('Content-Type: application/json');
echo json_encode($output);
?>