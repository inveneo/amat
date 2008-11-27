<html>

<head>
<title>admin</title>
</head>

<body>
<h3>admin</h3>

<table cellpadding="5" border="1">

<tr>
<th>enable</th>
<th>port</th>
<th>mac</th>
<th>type</th>
<th>host</th>
<th>cust</th>
<th>desc</th>
</tr>

% for row in c.rows:
<td><input type="checkbox"></td>
<td>${row[1].get_port()}</td>
<td>${row[0].get_mac()}</td>
<td>${row[0].get_type()}</td>
<td>${row[0].get_host()}</td>
<td>${row[0].get_cust()}</td>
<td>${row[0].get_desc()}</td>
</tr>
% endfor

</table>
</body>
</html>
