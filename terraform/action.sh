# Yan Pan
# az login required 
# az account set --subscription c6b8ec28-2ed5-4ac4-9410-4e9db46c1365
checkov -d . --soft-fail  # --output junitxml --skip-check xxx > $(pwd)/CheckovReport.xml
terraform init
terraform validate
terraform plan -out tfplan
terraform apply
# terraform apply -var-file dev.tfvars / terraform destroy 


# use output for kubectl set secrets
az aks get-credentials --resource-group $(terraform output --raw rg_name) --name $(terraform output --raw aks_name)
kubectl config use-context $(terraform output --raw aks_name)

kubectl create secret generic file-share-secrets \
  --from-literal=azurestorageaccountname=$(terraform output --raw file_share_account) \
  --from-literal=azurestorageaccountkey=$(terraform output --raw file_share_key)

# install CRD
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# add secrets!!!
cd ../
sh tmp.sh

# helm install
cd kubernetes-helm
helm install yyy-release-v1 --set shareName=yandemoprjtestfileshare001,dnsLabel=yyy-play-a001 .


# ip address routes
helm upgrade --install yyy-release-v1 --set shareName=yandemoprjtestfileshare001,dnsLabel=yyy-play-a001 .