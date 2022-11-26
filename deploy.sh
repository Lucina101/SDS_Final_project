#!/bin/bash
sudo kubectl apply -f persistent_volume.yaml
sudo kubectl apply -f db-deployment.yaml
sudo kubectl apply -f front-deployment.yaml
sudo kubectl apply -f back-deployment1.yaml
sudo kubectl apply -f back-deployment2.yaml
sudo kubectl apply -f back-deployment3.yaml
sudo kubectl apply -f ingress.yaml