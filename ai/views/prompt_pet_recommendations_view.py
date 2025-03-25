import traceback
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
from pets.serializers.pet_serializer import PetSerializer
from ai.services.update_or_create_recommendation import update_or_create_recommendation_service
from ai.services.get_many_recommendations import get_many_recommendations_service
from datetime import datetime, timedelta


def create_recommendation(type, content, pet):
    return {"content": content["data"], "pet": pet, "type": type, "update_in": datetime.now() + timedelta(days=1)}


chatbot = Chatbot()

message_nutrition = """Com base nos dados anteriores do pet, crie uma recomendação personalizada (máx. 1000 caracteres) sobre nutrição, dieta e peso, visando promover um envelhecimento saudável. A recomendação deve ser detalhada, prática e específica, abordando aspectos nutricionais relevantes para o pet.
1. Utilize somente o nome do pet, sem citar outras informações cadastrais.
2. Inclua uma ação que o tutor possa realizar em casa para melhorar a alimentação ou controle de peso.
3. Inclua uma ação que o veterinário deve realizar, como exames ou ajustes dietéticos.
4. Não mencione nomes comerciais de medicamentos ou suplementos, substituindo-os por descrições funcionais.
"""

message_activity = """Com base nos dados anteriores do pet, crie uma recomendação personalizada (máx. 1000 caracteres) sobre enriquecimento ambiental e gerenciamento de estresse, considerando socialização, exercícios físicos e cognitivos, e passeios para um envelhecimento saudável e longevidade ativa. Considere predisposições da raça, idade e possíveis doenças secundárias.
1. Não inclua recomendações sobre dieta/nutrição.
2. Utilize o nome do pet, sem mencionar outras informações cadastrais.
3. Inclua uma ação para o tutor realizar em casa, como brinquedos interativos, passeios ou técnicas de socialização, uso de tapetes antiderrapantes, rampas, camas suspensas e acolchoadas etc.
4. Inclua uma ação para o veterinário, como terapias comportamentais ou atividades supervisionadas, apenas se houver necessidade.
5. Não mencione nomes comerciais de medicamentos ou suplementos, substituindo-os por descrições funcionais.
"""

message_health = """Com base nos dados anteriores do pet, crie uma recomendação personalizada (máx. 1000 caracteres) sobre cuidados preventivos e proativos voltados para um envelhecimento saudável. Considere predisposições da raça, idade e doenças secundárias.
1. Não inclua recomendações sobre dieta/nutrição, enriquecimento ambiental ou adaptações em casa.
2. Utilize somente o nome do pet, sem citar outras informações cadastrais.
3. A recomendação deve ser detalhada, prática e específica, abordando aspectos de saúde preventiva e monitoramento de doenças comuns em pets idosos.
4. Inclua uma ação para o tutor aplicar em casa para uma melhor qualidade de vida e saúde do pet.
5. Inclua uma ação para o veterinário, como exames regulares ou tratamentos preventivos, apenas se houver a necessidade.
6. Não mencione nomes comerciais de medicamentos ou suplementos, substituindo-os por descrições funcionais.
"""


def format_prompt(message, pet):
    serialized = PetSerializer(pet)

    return str(serialized.data) + message


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
                    chatbot.send_message, messages=[
                        {"content": "Olá, como posso ajudar?", "role": "assistant"},
                        {"content": prompt_nutrition, "role": "user"}
                    ]

                )
                futures["activity"] = executor.submit(
                    chatbot.send_message, messages=[
                        {"content": "Olá, como posso ajudar?", "role": "assistant"},
                        {"content": prompt_activity, "role": "user"}
                    ]

                )
                futures["health"] = (executor.submit(
                    chatbot.send_message, messages=[
                        {"content": "Olá, como posso ajudar?", "role": "assistant"},
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
