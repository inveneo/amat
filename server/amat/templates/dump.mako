<html>
<head>
<title>dump</title>
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
<th>username</th>
<th>password</th>
<th>port</th>
</tr>
% for host in c.hosts:
<td>${host.get_mac()}</td>
<td>${host.get_type()}</td>
<td>${host.get_host()}</td>
<td>${host.get_cust()}</td>
<td>${host.get_desc()}</td>
<td>${host.get_geo()}</td>
<td>${host.get_opperiod()}</td>
<td>${host.get_username()}</td>
<td>${host.get_password()}</td>
<td>${host.get_port()}</td>
</tr>
% endfor
</table>

<h3>checkins</h3>
<table cellpadding="5" border="1">
<tr>
<th>id</th>
<th>tstamp</th>
<th>mac</th>
<th>status</th>
</tr>
% for checkin in c.checkins:
<td>${checkin.get_id()}</td>
<td>${checkin.get_tstamp()}</td>
<td>${checkin.get_mac()}</td>
<td>${checkin.get_status()}</td>
</tr>
% endfor
</table>
</body>
</html>
