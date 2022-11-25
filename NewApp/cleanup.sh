#!/bin/bash
sudo kubectl delete deployment/front-deployment
sudo kubectl delete deployment/back-deployment1
sudo kubectl delete deployment/back-deployment2
sudo kubectl delete deployment/back-deployment3
sudo kubectl delete deployment/db-deployment

sudo kubectl delete service/frontend-service
sudo kubectl delete service/backend-service1
sudo kubectl delete service/backend-service2
sudo kubectl delete service/backend-service3
sudo kubectl delete service/db-service3
#  kubectl delete deployment/front-deployment
#  kubectl delete deployment/back-deployment1
#  kubectl delete deployment/back-deployment2
#  kubectl delete deployment/back-deployment3

#  kubectl delete service/frontend-service
#  kubectl delete service/backend-service1
#  kubectl delete service/backend-service2
#  kubectl delete service/backend-service3