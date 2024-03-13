#!/bin/bash
echo "Informe o Dominio whitelabel - api"
read -r DOMAPI

echo "Realizando chegagem de dns ..."
    echo "Aplicando ajustes necessários ..."
    # Gera Template do Vhost
    sudo cp /migre/default_api.conf /etc/nginx/conf.d/"${DOMAPI}".conf
    # Altera o Server_name
    sudo sed -i "s/server_name/server_name $DOMAPI\;/g"   /etc/nginx/conf.d/"${DOMAPI}".conf
    sleep 2
    # Testa o nginx 
    if nginx -t 2>&1 | grep "test is successful" ; then
        sudo certbot --nginx -d "${DOMAPI}" --redirect --non-interactive
        sudo nginx -s reload
        echo $(date) "-- O dominio ""${DOMAPI}"" foi ajustado com sucesso !" >> /migre/nginx.log
    else
        echo "$(date) -- O dominio ""${DOMAPI}"" não foi ajustado Verifique !!" >> /migre/nginx.log
    fi
