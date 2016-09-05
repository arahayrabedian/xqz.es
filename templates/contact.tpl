<html>
    <head>
        <link rel="stylesheet" type="text/css" href="/static/style.css">
    </head>

    <body>
        %include common/header

        <H1>Contact Us</H1>

        <p>Use this form to send the developers behind xqz.es an email.<br> We prefer <a href=https://github.com/arahayrabedian/xqz.es/issues>github issues</a> where possible, but are happy to accept praise, feature requests, bug reports or reports of security flaws below as well.</p>

        %if contacted:
            <p class="success">Your feedback is hurtling it's way towards the nearest developer's inbox. Please don't resubmit the form again unless you have something to add. Thanks.</p>
        %end

        <form id="contact" method="POST" action="/contact/">
            <div>
                <label>Your email address</label>
                {{ !form.email }}
                %for error in form.email.errors:
                    <p class="error">{{ error }}</p>
                %end
            </div>

            <div>
                <label>{{ !form.contact_text.label }}</label>
                {{ !form.contact_text }}
                %for error in form.contact_text.errors:
                    <p class="error"> {{ error }}</p>
                %end
            </div>

            <div>
                <label>{{ !form.recaptcha }}</label>
                %for error in form.recaptcha.errors:
                    <p class="error"> {{ error }}</p>
                %end
            </div>

            <div><button type="submit">Contact!</button></div>
        </form>
    </body>
</html>
