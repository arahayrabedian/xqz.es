<html>
<head>
	<link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
	%include common/header

	<H1>{{excuse_text}}</H1>

	%if slack_installed:
		<H5>You seem to have successfully installed xqz.es for slack, <a href=https://slack.com/apps/manage>manage your apps</a> to approve it if necessary</H5>
	%else:
		%include common/add_to_slack_button
	%end
</body>
</html>