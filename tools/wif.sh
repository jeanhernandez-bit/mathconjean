# Configuracion unica: permite que GitHub Actions publique en Firebase Hosting
# sin claves privadas. Pegar en Cloud Shell (console.cloud.google.com).
PROJECT=mathconjean
REPO=jeanhernandez-bit/mathconjean
SA=github-deploy@$PROJECT.iam.gserviceaccount.com

gcloud config set project $PROJECT
NUM=$(gcloud projects describe $PROJECT --format='value(projectNumber)')
echo "Numero de proyecto: $NUM (debe ser 108727229400)"

gcloud services enable iamcredentials.googleapis.com sts.googleapis.com firebasehosting.googleapis.com

gcloud iam service-accounts create github-deploy --display-name="GitHub deploy"
for ROLE in roles/firebasehosting.admin roles/run.viewer roles/serviceusage.apiKeysViewer roles/serviceusage.serviceUsageConsumer; do
  gcloud projects add-iam-policy-binding $PROJECT --member="serviceAccount:$SA" --role=$ROLE --condition=None >/dev/null
done

gcloud iam workload-identity-pools create github --location=global --display-name="GitHub"
gcloud iam workload-identity-pools providers create-oidc github --location=global \
  --workload-identity-pool=github --display-name="GitHub" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository=='$REPO'"

gcloud iam service-accounts add-iam-policy-binding $SA --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$NUM/locations/global/workloadIdentityPools/github/attribute.repository/$REPO"

echo "Listo."
