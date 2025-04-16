import traceback
import random

from concurrent.futures import ThreadPoolExecutor
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from v0.errors.app_error import App_Error
from ai.chatbot_provider import Chatbot
from pets.services.get_pet_service import get_pet_service
from ai.services.update_or_create_recommendation import update_or_create_recommendation_service
from ai.services.get_many_recommendations import get_many_recommendations_service
from datetime import datetime, timedelta
from app.settings import RECOMMENDATION_EXPIRE_DAYS


def create_recommendation(type, content, pet):
    return {"content": content["data"], "pet": pet, "type": type, "update_in": datetime.now() + timedelta(days=RECOMMENDATION_EXPIRE_DAYS)}


chatbot = Chatbot()

message_nutrition = f"""
<dado>{random.choice(["problemas de saúde", "remédios", "peso", "idade", "porte", "raça"])}</dado>

Crie uma recomendação personalizada para o pet sobre "Nutrição, Dieta e Peso" baseada na informação de <dado>
1. Não inclua conteúdos sobre "Enriquecimento Ambiental e Gerenciamento de Estresse" e "Cuidados Preventivos e Proativos para Problemas de Saúde"
2. Avalie as funções dos remédios e efeitos colaterais sem citar nomes de medicações ou suplementos
3. Utilize somente o nome do pet e não mencione os demais dados informados para evitar repetição
4. Quando identificado como pet geriátrico, utilize os termos "mais idoso" ou "idoso avançado"
5. A recomendação deve formatada em 2 tópicos, sem textos antes ou depois:
    - Ações que o tutor possa realizar em sua moradia. Inicie o tópico com "Para fazer em casa:"
    - Ações com o veterinário. Inicie o tópico com "Com o veterinário:"
    - Deve conter menos de 1000 caracteres
"""

message_activity = f"""
<dado>{random.choice(["problemas de saúde", "remédios", "peso", "idade", "porte", "raça", "nível de atividade"])}</dado>

Crie uma recomendação personalizada para o pet sobre "Enriquecimento Ambiental e Gerenciamento de Estresse" baseada na informação de <dado>
1. Não inclua recomendações sobre "Cuidados Preventivos e Proativos para Problemas de Saúde" e "Nutrição, Dieta e Peso"
2. Avalie as funções dos remédios e efeitos colaterais sem citar nomes de medicações ou suplementos
3. Utilize somente o nome do pet e não mencione os demais dados informados para evitar repetição
4. Quando identificado como pet geriátrico, utilize os termos "mais idoso" ou "idoso avançado"
5. A recomendação deve formatada em 2 tópicos, sem textos antes ou depois:
    - Ações que o tutor possa realizar em sua moradia. Inicie o tópico com "Para fazer em casa:"
    - Ações com o veterinário. Inicie o tópico com "Com o veterinário:""
    - Termine com: "Ficou na dúvida? Pergunte pra IAPetSenior!"
    - Deve conter menos de 1000 caracteres
"""

message_health = f"""
<dado>{random.choice(["problemas de saúde", "remédios", "peso", "idade", "porte", "raça"])}</dado>

Crie uma recomendação personalizada para o pet sobre "Cuidados Preventivos e Proativos para Problemas de Saúde" baseada na informação de <dado>
1. Não inclua conteúdos sobre "Enriquecimento Ambiental e Gerenciamento de Estresse" e "Nutrição, Dieta e Peso"
2. Avalie as funções dos remédios e efeitos colaterais sem citar nomes de medicações ou suplementos
3. Utilize somente o nome do pet e não mencione os demais dados informados para evitar repetição
4. Quando identificado como pet geriátrico, utilize os termos "mais idoso" ou "idoso avançado"
5. A recomendação deve formatada em 2 tópicos, sem textos antes ou depois:
    - Ações que o tutor possa realizar em sua moradia. Inicie o tópico com "Para fazer em casa:"
    - Ações com o veterinário. Inicie o tópico com "Com o veterinário:"
    - Deve conter menos de 1000 caracteres
"""


def format_prompt(message, pet):
    birth_date = pet.birth_date.year - datetime.now().year
    health_problem = pet.health_problem.replace(";", ", ")
    medicines = pet.medicine.replace(";", ", ")
    specie = "cão" if pet.specie == "DOG" else "gato"
    sex = "macho" if pet.sex == "MALE" else "fêmea"
    formatted_pet_fields = f"""
    Nome: {pet.name};
    espécie: {specie};
    sexo: {sex};
    raça: {pet.race.name};
    porte: {pet.size};
    cor: {pet.color};
    nível de atividade: {pet.activity};
    idade: {birth_date};
    peso: {pet.weight};
    problemas de saúde: {health_problem};
    remédios: {medicines}

    """

    return formatted_pet_fields + message


class PromptPetRecommendations(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request):
        try:
            pet_id = request.query_params["pet_id"]
            pet = get_pet_service({"id": pet_id})

            if pet["data"] is None:
                raise App_Error("Pet not founded", 404)

            # get cached recommendation
            finded_recommendations = get_many_recommendations_service(
                {"pet": pet["data"], "update_in__gte": datetime.now()})

            if len(finded_recommendations) > 0:
                data = {}
                for r in finded_recommendations:
                    data[r.type] = {"data": r.content}
                return Response({"data": data})

            prompt_nutrition = format_prompt(message_nutrition, pet["data"])
            prompt_activity = format_prompt(message_activity, pet["data"])
            prompt_health = format_prompt(message_health, pet["data"])

            futures = {}

            with ThreadPoolExecutor(max_workers=3) as executor:
                futures["nutrition"] = executor.submit(
                    chatbot.get_recommendation, message=[
                        {"content": prompt_nutrition, "role": "user"}
                    ]

                )
                futures["activity"] = executor.submit(
                    chatbot.get_recommendation, message=[
                        {"content": prompt_activity, "role": "user"}
                    ]

                )
                futures["health"] = (executor.submit(
                    chatbot.get_recommendation, message=[
                        {"content": prompt_health, "role": "user"}
                    ]

                ))

            health_result = futures["health"].result()
            nutrition_result = futures["nutrition"].result()
            activity_result = futures["activity"].result()

            # cache recommendations
            update_or_create_recommendation_service(
                create_recommendation(
                    "health", health_result, pet["data"]))
            update_or_create_recommendation_service(
                create_recommendation(
                    "nutrition", nutrition_result, pet["data"]))
            update_or_create_recommendation_service(
                create_recommendation(
                    "activity", activity_result, pet["data"])
            )

            return Response({"data": {"health": futures["health"].result(), "nutrition": futures["nutrition"].result(), "activity": futures["activity"].result()}})

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
