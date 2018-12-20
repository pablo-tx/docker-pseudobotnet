#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Pasar por parametro numero de contenedores a lanzar"
  exit 1
fi

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

listen  stats  
        bind *:1936
        mode            http
        log             global

        maxconn 10

        clitimeout      100s
        srvtimeout      100s
        contimeout      100s
        timeout queue   100s

        stats enable
        stats hide-version
        stats refresh 30s
        stats show-node
        stats auth admin:admin
        stats uri  /haproxy?stats

listen funnel_proxy
        bind *:1337
        mode tcp
        balance roundrobin
        default_backend vpns
        
backend vpns
        option tcp-check
	tcp-check connect
	tcp-check send-binary 050100
	tcp-check expect binary 0500 # obtener status
	tcp-check send-binary 050100030a676f6f676c652e636f6d0050 # acceder a google
	tcp-check expect binary 0500

" > haproxy/haproxy.cfg 


port=5000
for f in $(cd VPN; bash -c ls); do
    if (( (port-5000) == $1 )); then break; fi

    port=$((port+1)); 
    echo "socks5 127.0.0.1 $port" >> proxychains.conf; 
    echo -e "\tserver vpn$port 127.0.0.1:$port check inter 5s port $port" >> haproxy/haproxy.cfg; 
    docker run -d --privileged -p 127.0.0.1:$port:8080 -e "vpn=$f" fr-botnet; 
done

docker build -q -t fr-botnet-haproxy ./haproxy
docker run -d --rm --network host fr-botnet-haproxy;
