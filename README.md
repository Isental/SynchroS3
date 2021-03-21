# SynchroS3

Script python pour synchroniser un bucket S3 avec un dossier.

Actuellement il n'utilise pas de fichier de configuration pour selectionner l'utilisateur, la clé ou la région.
Il prend en argument le lien du dossier a synchroniser en premier et le nom du bucket en second. 
Il déclanche une erreur lorsque les arguments ne sont pas ceux demandés.
