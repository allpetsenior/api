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

chatbot = Chatbot()


def create_recommendation(type, content, pet):
    return {"content": content["data"], "pet": pet, "type": type, "update_in": datetime.now() + timedelta(days=RECOMMENDATION_EXPIRE_DAYS)}


def get_pet_activity(activity):
    if activity == "LOW":
        return "baixa"
    if activity == "MEDIUM":
        return "média"
    if activity == "HIGH":
        return "alta"
    return activity


def format_prompt(message, pet):
    birth_date = datetime.now().year - pet.birth_date.year
    health_problem = pet.health_problem.replace(
        ";", ", ") if pet.health_problem else ""
    medicines = pet.medicine.replace(";", ", ") if pet.medicine else ""
    specie = "cão" if pet.specie == "DOG" else "gato"
    sex = "macho" if pet.sex == "MALE" else "fêmea"
    activity = get_pet_activity(pet.activity)
    formatted_pet_fields = f"<cadastro>Nome: {pet.name}; espécie: {specie}; sexo: {sex}; raça: {pet.race.name}; porte: {pet.size}; cor: {pet.color}; moradia: {pet.habitation}; nível de atividade: {activity}; idade: {birth_date}; peso: {pet.weight}; problemas de saúde: {health_problem}; remédios: {medicines}</cadastro>\n"

    return formatted_pet_fields + message


message_nutrition = f"""
<dado>{random.choice(["problemas de saúde", "remédios", "peso", "idade", "porte", "raça"])}</dado>

Com base no <cadastro> do pet, crie uma recomendação personalizada sobre "Alimentação, Nutrição e Peso", adaptada à fase da vida e às possíveis limitações, relacionada com a informação de <dado>
1. Não inclua recomendações sobre "Enriquecimento Ambiental" e "Cuidados Preventivos e Proativos para Problemas de Saúde"
2. Avalie diferentes tipos de alimentos, mencionado os benefícios para a condição do pet 
3. Utilize somente o nome do pet no texto e não repita os demais dados do <cadastro>
4. Se o pet for geriátrico, utilize os termos "mais idoso" ou "idoso avançado"
5. A recomendação deve formatada exatamente em 2 tópicos, sem textos antes ou depois:    
    - "Para fazer em casa:", citando ações práticas para o tutor realizar em sua moradia
    - "Com o veterinário:", citando ações clínicas ou profissionais. 
    - O texto deve conter aproximadamente 1000 caracteres, sem ultrapassar este limite
"""

message_activity = f"""
<dado>{random.choice(["problemas de saúde", "remédios", "peso", "idade", "porte", "raça", "nível de atividade"])}</dado>

Com base no <cadastro> do pet, elabore uma recomendação personalizada sobre "Enriquecimento Ambiental", adaptada à fase da vida e às possíveis limitações, baseada na informação de <dado>
1. Não inclua recomendações sobre "Cuidados Preventivos e Proativos para Problemas de Saúde" e "Nutrição, Dieta e Peso"
2. Avalie diferentes formas de melhorar o ambiente, mencionando os benefícios para a condição do pet
3. Utilize somente o nome do pet no texto e não repita os demais dados do <cadastro>
4. Se o pet for geriátrico, utilize os termos "mais idoso" ou "idoso avançado"
5. A recomendação deve formatada exatamente em 2 tópicos, sem textos antes ou depois:    
    - "Para fazer em casa:", citando ações práticas para o tutor realizar em sua moradia
    - "Com o veterinário:", citando ações clínicas ou profissionais. 
    - Termine com: "Ficou na dúvida? Pergunte pra IAPetSenior!"
    - O texto deve conter aproximadamente 1000 caracteres, sem ultrapassar este limite
"""

message_health = f"""
<dado>{random.choice(["problemas de saúde", "remédios", "peso", "idade", "porte", "raça"])}</dado>

Com base no <cadastro> do pet, elabore uma recomendação personalizada sobre "Cuidados Preventivos e Proativos para Problemas de Saúde", adaptada à fase da vida e às possíveis limitações, relacionada com a informação de <dado>
1. Não inclua recomendações sobre "Enriquecimento Ambiental" e "Nutrição, Dieta e Peso"
2. Avalie a utilidade dos remédios, mencionando funções e efeitos colaterais comuns, sem citar nomes de medicamentos ou suplementos.
3. Utilize somente o nome do pet no texto e não repita os demais dados do <cadastro>
4. Se o pet for geriátrico, utilize os termos "mais idoso" ou "idoso avançado"
5. A recomendação deve formatada exatamente em 2 tópicos, sem textos antes ou depois:    
    - "Para fazer em casa:", citando ações práticas para o tutor realizar em sua moradia
    - "Com o veterinário:", citando ações clínicas ou profissionais. 
    - O texto deve conter aproximadamente 1000 caracteres, sem ultrapassar este limite
"""


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
                    data[r.type] = {"data": r.content, "id": r.id}

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
            cached_health_recommendation = update_or_create_recommendation_service(
                create_recommendation(
                    "health", health_result, pet["data"]))
            cached_nutrition_recommendation = update_or_create_recommendation_service(
                create_recommendation(
                    "nutrition", nutrition_result, pet["data"]))
            cached_activity_recommendation = update_or_create_recommendation_service(
                create_recommendation(
                    "activity", activity_result, pet["data"])
            )

            return Response({"data": {"health": {"data": cached_health_recommendation.content, "id": cached_health_recommendation.id}, "nutrition": {"data": cached_nutrition_recommendation.content, "id": cached_nutrition_recommendation.id}, "activity": {"data": cached_activity_recommendation.content, "id": cached_activity_recommendation.id}}})

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
