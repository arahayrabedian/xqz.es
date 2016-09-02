<center><H1>{{excuse_text}}</H1></center>

%if slack_installed:
<center><H5>You seem to have successfully installed xqz.es for slack, <a href=https://slack.com/apps/manage>manage your apps</a> to approve it if necessary</H5></center>
%else:
<center><a href="https://slack.com/oauth/authorize?scope={{slack_command_scope}}&client_id={{slack_client_id}}"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a></center>
%end
