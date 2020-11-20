#Apache Route

Listen 80

<VirtualHost \*:80>
ServerName localhost
WSGIScriptAlias / M:\Shipping-Integrator\app.wsgi
<Directory M:\Shipping-Integrator>
Require all granted
</Directory>
</VirtualHost>
