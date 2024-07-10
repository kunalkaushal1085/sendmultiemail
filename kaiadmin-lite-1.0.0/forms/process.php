<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $contactFile = $_POST['contactFile'];
    $emailFile = $_POST['emailFile'];

        $command = escapeshellcmd("python3 send.py");
        $output = shell_exec($command);
        echo "<pre>$output</pre>";
}
?>
