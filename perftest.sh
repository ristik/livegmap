while true; do curl -H "Accept: application/json" -X POST -d locality=Kolga\&x=58.${RANDOM}\&y=25.${RANDOM} http://localhost:8888/api  ; sleep 0.01; done
