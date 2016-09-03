<html>
<head>
</head>
<body>
<H1>Contact Us</H1>

<p style="width:50%">
Use this form to send the developers behind
xqz.es an email. We prefer
<a href=https://github.com/arahayrabedian/xqz.es/issues>github issues</a>
where possible, but are happy to accept praise,
feature requests, bug reports or reports of
security flaws below as well.
</p>

%if contacted:
<p style="width:50%">
<font color="green">Your feedback is hurtling it's way towards the nearest
developer's inbox. Please don't resubmit the form again unless you have
something to add. Thanks.</font>
</p>
%end

<form method="POST" action="/contact/">

    <p>
    <div>Your email address</div>
    <div> {{ !form.email }}</div>
    %for error in form.email.errors:
    <font color="red">{{ error }}</font>
    %end
    </p>


    <p>
    <div>{{ !form.contact_text.label }}</div>
    <div>{{ !form.contact_text }}</div>
    %for error in form.contact_text.errors:
    <font color="red"> {{ error }}</font>
    %end
    </p>

    <p>
    <div>{{ !form.recaptcha }}</div>
    %for error in form.recaptcha.errors:
    <font color="red"> {{ error }}</font>
    %end
    </p>

    <p>
    <div><button type="submit">Contact!</button></div>
    </p>
</form>
</body>
</html>