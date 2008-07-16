<html>
<head>
<title>hosts</title>
</head>
<body>
<h3>hosts</h3>
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
% for host in c.hosts:
<td>${host.get_mac()}</td>
<td>${host.get_type()}</td>
<td>${host.get_host()}</td>
<td>${host.get_cust()}</td>
<td>${host.get_desc()}</td>
<td>${host.get_geo()}</td>
<td>${host.get_opperiod()}</td>
</tr>
% endfor
</table>
</body>
</html>
