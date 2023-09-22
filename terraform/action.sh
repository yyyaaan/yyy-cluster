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
# if not on pipeline or using service principle, need set subscription
az aks get-credentials --resource-group $(terraform output --raw rg_name) --name $(terraform output --raw aks_name)

kubectl config use-context $(terraform output --raw aks_name)
# kubectl config get-contexts

kubectl create secret generic file-share-secrets \
  --from-literal=azurestorageaccountname=$(terraform output --raw file_share_account) \
  --from-literal=azurestorageaccountkey=$(terraform output --raw file_share_key)

# install ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.7.1/deploy/static/provider/cloud/deploy.yaml