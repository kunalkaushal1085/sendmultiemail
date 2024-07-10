<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Email Sender</title>
</head>
<body>
    <h2>Email Sender Form</h2>
   <form action="/cgi-bin/process_form.py" method="post" enctype="multipart/form-data">
    <label for="num_emails_to_send">Number of Emails to Send:</label>
    <input type="text" id="num_emails_to_send" name="num_emails_to_send"><br><br>
    
    <label for="recipient_csv">Recipient CSV File:</label>
    <input type="file" id="recipient_csv" name="recipient_csv"><br><br>
    
    <label for="email_html">Email HTML Template:</label>
    <input type="file" id="email_html" name="email_html"><br><br>
    
    <input type="submit" value="Submit">
</form>

    <script>
        function submitForm() {
            const form = document.getElementById('emailForm');
            const formData = new FormData(form);

            const xhr = new XMLHttpRequest();
            xhr.open("POST", "process_form.py", true);

            xhr.onload = function() {
                if (xhr.status === 200) {
                    alert('Emails are being sent.');
                } else {
                    alert('An error occurred!');
                }
            };

            xhr.send(formData);
        }
    </script>
</body>
</html>
