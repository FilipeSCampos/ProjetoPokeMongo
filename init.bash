# Criação do ambiente virtual
python -m venv venv

# Ativação do ambiente virtual
# No Windows:
venv\Scripts\activate
# No Unix ou MacOS:
source venv/bin/activate

# Instalação das dependências
pip install django
pip install mongoengine
pip install django-mongoengine
pip install djangorestframework


--------------------------------Aqui0--é-a-inicializacao----------------------------------------

django-admin startproject pokemon_battle
cd pokemon_battle
python manage.py startapp game
