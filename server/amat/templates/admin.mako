<html>

<head>
<title>admin</title>
</head>

<body>
<h3>admin</h3>

<form action="admin" method="GET">

<table cellpadding="5" border="1">

<tr>
<th>enable</th>
<th>port</th>
<th>mac</th>
<th>type</th>
<th>host</th>
<th>cust</th>
<th>desc</th>
<th>last heard from</th>
<th>temperature</th>
</tr>

% for row in c.rows:
<td><input type="checkbox" ${row[2]} name="${row[0].get_mac()}"></td>
<td>${row[1].get_port()}</td>
<td>${row[0].get_mac()}</td>
<td>${row[0].get_type()}</td>
<td>${row[0].get_host()}</td>
<td>${row[0].get_cust()}</td>
<td>${row[0].get_desc()}</td>
<td>${row[3]} (${row[4]})</td>
<td>${row[5]}</td>
</tr>
% endfor

</table>

<input type="hidden" name="update">
<input type="submit" value="Update">
</form>

</body>
</html>
