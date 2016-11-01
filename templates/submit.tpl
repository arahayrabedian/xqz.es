<html>
    <head>
        <link rel="stylesheet" type="text/css" href="/static/style.css">
    </head>

    <body>
        %include common/header

        <H1>Submit a New Excuse</H1>

        <p>Use this form to submit new excuses (subject to moderator approval)</p>

        %if submitted:
            <p class="success">Our moderators are gonna take their sweet time, but promise to take a look at your excuse... sooner or later.</p>
        %end

        <form id="submit" method="POST" action="/submit/">
            <div>
                <label>{{ !form.attribution_name.label }}</label>
                {{ !form.attribution_name}}
                %for error in form.attribution_name.errors:
                    <p class="error">{{ error }}</p>
                %end
            </div>

            <div>
                <label>{{ !form.excuse.label }}</label>
                {{ !form.excuse }}
                %for error in form.excuse.errors:
                    <p class="error"> {{ error }}</p>
                %end
            </div>

            <div>
                <label>{{ !form.nocaptcha }}</label>
                %for error in form.nocaptcha.errors:
                    <p class="error"> {{ error }}</p>
                %end
            </div>

            <div><button type="submit">Excuse-ify! Enhance!</button></div>
        </form>
    </body>
</html>
