<%!
from authkit.authorize.pylons_adaptors import authorized
from authkit.permissions import UserIn
%>
<html>

<head>
<title>admin</title>
</head>

<body>
<h3><span>admin</span>
% if authorized(UserIn(["admin"])):
<span style="padding: 8px">|</span><span><a href='/auth/signout'>signout</a></span>
% endif
</h3>
<form action="admin" method="POST">
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
