# flasky-vosk

curl -i -X POST -H "Content-Type: multipart/form-data" -F "data=@test.wav" localhost:5000^C



# Créer l'utilisateur administrateur des moteurs de recherche

## Création de l'utilisateur
```
curl --location --request POST 'localhost:8080/api/v1/user/guest/register' --header 'Content-Type: application/json' --data-raw '
{"avatar":{},"avatarId":"","authorities":[],"followedSearchEngine":[],"firstName":"Météo","lastName":"France","username":"admin_search@meteo.fr","password":"6L1u2@fv"}
'
```
La réponse devrait être similaire à celle-ci :
```
{"firstName":"Météo","lastName":"France","username":"admin_search@meteo.fr","active":true,"authorities":["ADMIN"],"id":"602a5a0cccd41e1f687da8e2","followedSearchEngine":[],"verified":false}
```

## Activation de l'utilisateur
Connexion à au service Mongo DB : 
```
$ docker exec -it mongo /bin/bash
```
```
root@c5b4b277ab91:/# mongo
MongoDB shell version v4.4.3
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("16a76fb5-7c96-4bd4-9517-6467ebcffc70") }
MongoDB server version: 4.4.3
Welcome to the MongoDB shell.
...
```
```
> use all-backend
switched to db all-backend
```
Puis en utilisant l'identifiant reçu à la commande de création de l'utilisateur :
```
> db['users'].update({ _id : ObjectId("602a5a0cccd41e1f687da8e2") }, { $set: { verified : true }})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
```
Bien vérifier `nModified` : il devrait être `1`

```
> exit
bye
root@c5b4b277ab91:/# exit
exit
```

# Initialisation des sources de données


## Login et obtention du token
```
curl --location --request POST 'localhost:8080/api/v1/user/guest/login' \
--header 'Content-Type: application/json' \
--data-raw '{
  "password": "6L1u2@fv",
  "username": "admin_search@meteo.fr"
}'
```
-->
```
{"accessToken":"eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbl9zZWFyY2hAbWV0ZW8uZnIiLCJhdXRoIjoiUk9MRV9BRE1JTiIsImV4cCI6MTYxNDI1Nzc4OH0.BrM41t8wq1GRpISEq6ZsCohhYFKuPhGLqpdmAXmYuNIayDskf4upS4CUsTJl1joYa-vPGnDxTFhoDa4JSUfsSQ","user":{"firstName":"Meteo","lastName":"France","username":"admin_search@meteo.fr","active":true,"authorities":["ADMIN"],"id":"602a5a0cccd41e1f687da8e2","followedSearchEngine":[],"verified":true}}
```
Ensuite, avec le token obtenu à l'étape précédente : 
```
export Token="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbl9zZWFyY2hAbWV0ZW8uZnIiLCJhdXRoIjoiUk9MRV9BRE1JTiIsImV4cCI6MTYxNDI1Nzc4OH0.BrM41t8wq1GRpISEq6ZsCohhYFKuPhGLqpdmAXmYuNIayDskf4upS4CUsTJl1joYa-vPGnDxTFhoDa4JSUfsSQ"
```

## Obtention de l'id du moteur de recherche
```
curl --location --request GET 'localhost:8080/api/v1/admin/me/search-engines' \
--header 'Authorization: '"${Token}"''
```
-->
```
{"content":[{"active":true,"alias":"","avatar":{"id":"6017c98c8ecdff4f8263d468","length":0,"path":"./assets/img/theme/jean-dujardin.png"},"description":"","id":"601a7808721bfa78036db52f","label":"","owner":{"active":true,"firstName":"Jean","id":"6017c98c8ecdff4f8263d469","lastName":"Dujardin"},"searchable":true,"trending":[],"trendingWeight":0}]}
```
Ensuite, avec l'id obtenu à l'étape précédente : 
```
export searchEngineId="601a7808721bfa78036db52f"
```

## Source Confluence
 - Label : Confluence
 - Type : Confluence
 - URI : http://confluence.meteo.fr/

```
curl --location --request POST 'localhost:8080/api/v1/search-engine/'"${searchEngineId}"'/source' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "label": "Confluence",
    "type": "CONFLUENCE",
    "uri": "http://confluence.meteo.fr/",
    "advancedSettings": {
        "excludeUrlPatterns": [
            "Bac à sable"
        ]
    }
}'
```

dans le cas de source de type confluence, nous utilisons le champ "excludeUrlPatterns" pour exclure les pages des espaces confluence qu'on ne souhaite pas indexer.

## Source Intramet
 - Label : Intramet
 - Type : Plone
 - URI : http://intramet.meteo.fr
 - Exclude Url Patterns : /search, /acl_users, position=, /image_view_fullscreen, /image_preview, /image_thumb, /image_mini, /sendto_form, /folder_contents, /manage_propertiesForm, /@@notifyform, /edit, /RSS, /local-sitemap, /members, /vous-a-meteo-france/petites_annonces, /download, /saint-mande, /qualite, /acnet, acnet.meteo.fr, qualite.meteo.fr, saintmande.meteo.fr

```
curl --location --request POST 'localhost:8080/api/v1/search-engine/'"${searchEngineId}"'/source' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "label": "Intramet",
    "type": "PLONE",
    "uri": "http://intramet.meteo.fr",
    "advancedSettings": {
        "excludeUrlPatterns": [
            "/search", "/acl_users", "position=", "/image_view_fullscreen", "/image_preview", "/image_thumb", "/image_mini", "/sendto_form", "/folder_contents", "/manage_propertiesForm", "/@@notifyform", "/edit", "/RSS", "/local-sitemap", "/members", "/vous-a-meteo-france/petites_annonces", "/download", "/saint-mande", "/qualite", "/acnet", "acnet.meteo.fr", "qualite.meteo.fr", "saintmande.meteo.fr"
        ]
    }
}'
```

## Source Qualité
 - Label : Qualité
 - Type : Plone
 - URI : http://qualite.meteo.fr
 - Exclude Url Patterns : /search, /acl_users, position=, /image_view_fullscreen, /image_preview, /image_thumb, /image_mini, /sendto_form, /folder_contents, /manage_propertiesForm, /@@notifyform, /edit, /RSS, /local-sitemap, /members, /meteo-france, /sg, /actus, /vous-a-meteo-france/petites_annonces, /download, /intramet, /saint-mande, /acnet, intramet.meteo.fr, acnet.meteo.fr, saintmande.meteo.fr

```
curl --location --request POST 'localhost:8080/api/v1/search-engine/'"${searchEngineId}"'/source' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "label": "Qualité",
    "type": "PLONE",
    "uri": "http://qualite.meteo.fr",
    "advancedSettings": {
        "excludeUrlPatterns": [
            "/search", "/acl_users", "position=", "/image_view_fullscreen", "/image_preview", "/image_thumb", "/image_mini", "/sendto_form", "/folder_contents", "/manage_propertiesForm", "/@@notifyform", "/edit", "/RSS", "/local-sitemap", "/members",  "/meteo-france", "/sg", "/actus", "/vous-a-meteo-france/petites_annonces", "/download", "intramet", "/saint-mande", "/acnet", "acnet.meteo.fr", "intramet.meteo.fr", "saintmande.meteo.fr"
        ]
    }
}'
```

## Source Saint Mandé
 - Label : Saint Mandé
 - Type : Plone
 - URI : http://saintmande.meteo.fr
 - Exclude Url Patterns : /search, /acl_users, position=, /image_view_fullscreen, /image_preview, /image_thumb, /image_mini, /sendto_form, /folder_contents, /manage_propertiesForm, /@@notifyform, /edit, /RSS, /local-sitemap, /members, /meteo-france, /sg, /actus, /vous-a-meteo-france/petites_annonces, /download, /intramet, /qualite, /acnet, intramet.meteo.fr, qualite.meteo.fr, acnet.meteo.fr 

```
curl --location --request POST 'localhost:8080/api/v1/search-engine/'"${searchEngineId}"'/source' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "label": "Saint Mandé",
    "type": "PLONE",
    "uri": "http://saintmande.meteo.fr",
    "advancedSettings": {
        "excludeUrlPatterns": [
            "/search", "/acl_users", "position=", "/image_view_fullscreen", "/image_preview", "/image_thumb", "/image_mini", "/sendto_form", "/folder_contents", "/manage_propertiesForm", "/@@notifyform", "/edit", "/RSS", "/local-sitemap", "/members", "/meteo-france", "/sg", "/actus", "/vous-a-meteo-france/petites_annonces", "/download", "/intramet", "/qualite", "/acnet", "intramet.meteo.fr", "qualite.meteo.fr", "acnet.meteo.fr" 
        ]
    }
}'
```

## Source Acnet
 - Label : Acnet
 - Type : Plone
 - URI : http://acnet.meteo.fr
 - Exclude Url Patterns : /search, /acl_users, position=, /image_view_fullscreen, /image_preview, /image_thumb, /image_mini, /sendto_form, /folder_contents, /manage_propertiesForm, /@@notifyform, /edit, /RSS, /local-sitemap, /members, /meteo-france, /sg, /actus, /vous-a-meteo-france/petites_annonces, /intramet, /saint-mande, /qualite, intramet.meteo.fr, qualite.meteo.fr, saintmande.meteo.fr

```
curl --location --request POST 'localhost:8080/api/v1/search-engine/'"${searchEngineId}"'/source' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "label": "Acnet",
    "type": "PLONE",
    "uri": "http://acnet.meteo.fr",
    "advancedSettings": {
        "excludeUrlPatterns": [
            "/search", "/acl_users", "position=", "/image_view_fullscreen", "/image_preview", "/image_thumb", "/image_mini", "/sendto_form", "/folder_contents", "/manage_propertiesForm", "/@@notifyform", "/edit", "/RSS", "/local-sitemap", "/members", "/meteo-france", "/sg", "/actus", "/vous-a-meteo-france/petites_annonces", "/intramet", "/saint-mande", "/qualite", "intramet.meteo.fr", "qualite.meteo.fr", "saintmande.meteo.fr"
        ]
    }
}'
```

## Vérification

Vérification avec l'interface utilisateur. L'écran Espace de l'administrateur // Mes Moteurs // Sources devrait ressembler à ceci : 

![Illustration pour la vérification de la bonne création des sources de données](add_all_sources_confirmation.png)

# Initialisation des facettes

## Création des facettes
```
curl --location --request POST 'http://localhost:8080/api/v1/search-facet' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Domaine",
    "fieldName": "metadata.domainName.keyword",
    "type": "TERMS",
    "order": 10
}'

curl --location --request POST 'http://localhost:8080/api/v1/search-facet' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Type de document",
    "fieldName": "json.documentTypeDisplay.keyword",
    "type": "TERMS",
    "order": 20
}'

curl --location --request POST 'http://localhost:8080/api/v1/search-facet' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Date de modification",
    "fieldName": "source.lastModified",
    "type": "DATE_RANGE",
    "order": 30,
    "ranges": [
        {
            "key": "Moins d'\''un jour",
            "from": "now-1d/d",
            "to": "now",
            "order": 1
        },
        {
            "key": "Moins d'\''une semaine",
            "from": "now-7d/d",
            "to": "now",
            "order": 2
        },
        {
            "key": "Moins d'\''un mois",
            "from": "now-1M/d",
            "to": "now",
            "order": 3
        },
        {
            "key": "Plus d'\''un mois",
            "from": "now-20y/y",
            "to": "now-1M/d",
            "order": 4
        }
    ]
}'

curl --location --request POST 'http://localhost:8080/api/v1/search-facet' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Date de création",
    "fieldName": "json.createdDate",
    "type": "DATE_HISTOGRAM",
    "interval": "YEAR",
    "order": 40
}'

curl --location --request POST 'http://localhost:8080/api/v1/search-facet' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Mots-clés",
    "fieldName": "json.keywords.keyword",
    "type": "TERMS",
    "order": 50
}'

curl --location --request POST 'http://localhost:8080/api/v1/search-facet' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Espace Confluence",
    "fieldName": "json.spaceName.keyword",
    "type": "TERMS",
    "order": 60,
    "parentFacet": {
        "name": "Domaine",
        "value": "confluence.meteo.fr"
    }
}'

curl --location --request POST 'http://localhost:8080/api/v1/search-facet' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "International",
    "fieldName": "attachment.language",
    "type": "TERMS",
    "order": 70
}'
```

## Vérification des facettes

```
curl --location --request GET 'http://localhost:8080/api/v1/search-facet' \
--header 'Authorization: '"${Token}"'' \
--header 'Content-Type: application/json' | jq
```
-->
```
{
  "content": [
    {
      "fieldName": "metadata.domainName.keyword",
      "id": "603668bfd2900c498bd614af",
      "name": "Domaine",
      "order": 10,
      "ranges": [],
      "size": 10,
      "sortAsc": false,
      "type": "TERMS"
    },
    {
      "fieldName": "json.documentTypeDisplay.keyword",
      "id": "603668bfd2900c498bd614b0",
      "name": "Type de document",
      "order": 20,
      "ranges": [],
      "size": 10,
      "sortAsc": false,
      "type": "TERMS"
    },
    {
      "fieldName": "source.lastModified",
      "id": "603668c0d2900c498bd614b1",
      "name": "Date de modification",
      "order": 30,
      "ranges": [
        {
          "from": "now-1d/d",
          "key": "Moins d'un jour",
          "order": 1,
          "to": "now"
        },
        {
          "from": "now-7d/d",
          "key": "Moins d'une semaine",
          "order": 2,
          "to": "now"
        },
        {
          "from": "now-1M/d",
          "key": "Moins d'un mois",
          "order": 3,
          "to": "now"
        },
        {
          "from": "now-20y/y",
          "key": "Plus d'un mois",
          "order": 4,
          "to": "now-1M/d"
        }
      ],
      "size": 10,
      "sortAsc": false,
      "type": "DATE_RANGE"
    },
    {
      "fieldName": "json.createdDate",
      "id": "603668c0d2900c498bd614b2",
      "interval": "year",
      "name": "Date de création",
      "order": 40,
      "ranges": [],
      "size": 10,
      "sortAsc": false,
      "type": "DATE_HISTOGRAM"
    },
    {
      "fieldName": "json.keywords.keyword",
      "id": "603668c0d2900c498bd614b3",
      "name": "Mots-clés",
      "order": 50,
      "ranges": [],
      "size": 10,
      "sortAsc": false,
      "type": "TERMS"
    },
    {
      "fieldName": "json.spaceName.keyword",
      "id": "603668c0d2900c498bd614b4",
      "name": "Espace Confluence",
      "order": 60,
      "parent": {
        "name": "Domaine",
        "value": "confluence.meteo.fr"
      },
      "ranges": [],
      "size": 10,
      "sortAsc": false,
      "type": "TERMS"
    },
    {
      "fieldName": "attachment.language",
      "id": "603668c0d2900c498bd614b5",
      "name": "International",
      "order": 70,
      "ranges": [],
      "size": 10,
      "sortAsc": false,
      "type": "TERMS"
    }
  ],
  "empty": false,
  "first": true,
  "last": true,
  "number": 0,
  "numberOfElements": 7,
  "pageable": {
    "offset": 0,
    "pageNumber": 0,
    "pageSize": 20,
    "paged": true,
    "sort": {
      "empty": true,
      "sorted": false,
      "unsorted": true
    },
    "unpaged": false
  },
  "size": 20,
  "sort": {
    "empty": true,
    "sorted": false,
    "unsorted": true
  },
  "totalElements": 7,
  "totalPages": 1
}
```
