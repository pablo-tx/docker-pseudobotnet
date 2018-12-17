#!/bin/bash

echo "
random_chain
proxy_dns 
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
" > proxychains.conf 

echo "
global
        daemon
        user root
        group root
defaults
        mode tcp
        maxconn 3000
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms
listen funnel_proxy
        bind *:1337
        mode tcp
        balance roundrobin
        default_backend vpns
        
backend vpns
" > haproxy/haproxy.cfg 

if [ "$#" -ne 1 ]; then
  echo "Pasar por parametro numero de contenedores a lanzar"
  exit 1
fi

port=5000
for f in $(cd VPN; bash -c ls); do
    if (( (port-5000) == $1 )); then break; fi

    port=$((port+1)); 
    echo "http 127.0.0.1 $port" >> proxychains.conf; 
    echo "server vpn$port 127.0.0.1:$port check" >> haproxy/haproxy.cfg; 
    docker run -d --privileged -p 127.0.0.1:$port:8080 -e "vpn=$f" fr-botnet; 
done

docker build -q -t fr-botnet-haproxy ./haproxy
docker run -d --rm --network host fr-botnet-haproxy;
