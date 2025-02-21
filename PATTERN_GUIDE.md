# guia de padrões de desenvolvimento da API

- para adicionar novas endpoints, você precisa especificar a url no arquivo **v0/urls.py**

```python
from django.urls import path, include

urlpatterns = [
    path("/core", include("core.urls")),
    path("/pet", include("pets.pet_urls")),
    path("/pets", include("pets.pets_urls"))
]
```

- caso o escopo da funcionalidade seja nova, criar novo django app

```bash
python manage.py startapp <nome-do-app>
```

- deste jeito, o django irá criar um novo diretório com a estrutura adequada.

- agora, você adicionar a endpoint no arquivo **urls.py** do recém criado diretório

- em **urls.py** você especifica a url e vincula a view que você quer

- as views ficam em uma pasta view

- nas views, você chama os services

- nos services, você chama os repositórios (que são as classes que fazem interface com o banco de dados, por meio dos modelos)
