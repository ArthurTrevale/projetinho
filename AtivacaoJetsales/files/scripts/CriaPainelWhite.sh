#!/bin/bash
echo "Informe o Dominio whitelabel - Painel"
read -r DOM
echo "Realizando chegagem de dns ..."
    echo "Aplicando ajustes necessários ..."
    # Gera Template do Vhost
    sudo cp /migre/default_painel.conf /etc/nginx/conf.d/"${DOM}".conf
    # Altera o Server_name
    sudo sed -i "s/server_name/server_name $DOM\;/g"   /etc/nginx/conf.d/"${DOM}".conf
    sleep 2
    # Testa o nginx 
    if nginx -t 2>&1 | grep "test is successful" ; then
        sudo certbot --nginx -d "${DOM}" --redirect --non-interactive
        sudo nginx -s reload
        echo $(date) "-- O dominio ""${DOM}"" foi ajustado com sucesso !" >> /migre/nginx.log
    else
        echo "$(date) -- O dominio ""${DOM}"" não foi ajustado Verifique !!" >> /migre/nginx.log
    fi
