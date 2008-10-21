<html>
<head>
<title>reg</title>
</head>
<body>
<h3>You sent me:</h3>
<table cellpadding="5" border="1">
<tr>
<th>mac</th>
<th>type</th>
<th>host</th>
<th>cust</th>
<th>desc</th>
<th>geo</th>
<th>opperiod</th>
</tr>
<tr>
<td>${c.host.get_mac()}</td>
<td>${c.host.get_type()}</td>
<td>${c.host.get_host()}</td>
<td>${c.host.get_cust()}</td>
<td>${c.host.get_desc()}</td>
<td>${c.host.get_geo()}</td>
<td>${c.host.get_opperiod()}</td>
</tr>
</table>

<h3>I made tunnel record:</h3>
<tr>
<th>id</th>
<th>mac</th>
<th>username</th>
<th>password</th>
<th>port</th>
</tr>
<tr>
<td>${c.tunnel.get_id()}</td>
<td>${c.tunnel.get_mac()}</td>
<td>${c.tunnel.get_username()}</td>
<td>${c.tunnel.get_password()}</td>
<td>${c.tunnel.get_port()}</td>
</tr>
</body>
</html>
