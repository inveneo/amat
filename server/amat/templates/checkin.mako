<html>
<head>
<title>checkin</title>
</head>
<body>
<h3>You sent me:</h3>
<table cellpadding="5" border="1">
<tr>
<th>mac</th>
<th>status</th>
</tr>
<tr>
<td>${c.checkin.get_mac()}</td>
<td>${c.checkin.get_status()}</td>
</tr>
</table>
at ${c.checkin.get_tstamp()}
</body>
</html>
