<html>
<head>
%include common/header
</head>

<center><H1>{{excuse_text}}</H1></center>

%if slack_installed:
<center><H5>You seem to have successfully installed xqz.es for slack, <a href=https://slack.com/apps/manage>manage your apps</a> to approve it if necessary</H5></center>
%else:
<center>
%include common/add_to_slack_button
</center>
%end
</html>