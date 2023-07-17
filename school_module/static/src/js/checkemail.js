odoo.define('school_module.checkemail', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.checkemail = publicWidget.Widget.extend({
        selector: '#email',
        events: {
            'blur': '_onEmailBlur',
        },
        _onEmailBlur: function (ev) {
            var email = ev.target.value;
            this._checkEmailExists(email);
        },
        _checkEmailExists: function (email) {
            return ajax.jsonRpc('/admission/check_email', 'call', {
                email: email
            }).then(function (response) {
                var messageElement = document.getElementById("email-message");
                if(response.email_exist == true){
                    messageElement.textContent = "Email is already exists!";
                    messageElement.classList.add('text-danger');
                }
                else{
                   messageElement.textContent = "";
                   messageElement.classList.remove('text-danger');
                }
            });
        },
    });
});