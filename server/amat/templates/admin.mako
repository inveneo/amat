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

% for (mac, enabled, port, type, host, cust, desc, tstamp, blurb, temp) in c.rows:
<td><input type="checkbox" ${enabled} name="${mac}"></td>
<td>${port}</td>
<td>${mac}</td>
<td>${type}</td>
<td>${host}</td>
<td>${cust}</td>
<td>${desc}</td>
<td>${tstamp} (${blurb})</td>
<td>${temp}</td>
</tr>
% endfor

</table>

<input type="hidden" name="update">
<input type="submit" value="Update">
</form>

</body>
</html>
