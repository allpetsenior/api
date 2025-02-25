import traceback
from concurrent.futures import ThreadPoolExecutor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from v0.errors.app_error import App_Error
from ai.chatbot_provider import Chatbot
from pets.services.get_pet_service import get_pet_service
from pets.serializers.pet_serializer import PetSerializer

chatbot = Chatbot()

message_nutrition = "Analise os dados de cadastro fornecidos sobre o pet (espécie, gênero, raça, idade, peso, problemas de saúde e medicações diárias), e crie uma recomendação em até mil caracteres relacionada à nutrição, dieta e peso visando promover a saúde preventiva e proativa do animal para um envelhecimento saudável. A recomendação deve ser detalhada e prática, que aborde aspectos específicos da alimentação e cuidados nutricionais com base nas características do pet. Use uma sugestão de ação que o tutor possa fazer em casa, e outra no veterinário. A recomendação deve respeitar o contexto cadastral fornecido, mantendo um tom empático e educativo. Não generalize; personalize as orientações com base nos dados disponíveis."

message_activity = "Enriquecimento ambiental e gerenciamento de estresse (socialização com outros pets e familiares, exercícios físicos e cognitivos, passeio). Analise os dados de cadastro fornecidos sobre o pet (espécie, gênero, raça, idade, peso, problemas de saúde e medicações diárias), e crie uma recomendação personalizada em até mil caracteres relacionada a enriquecimento ambiental e gerenciamento de estresse. As orientações devem considerar socialização, exercícios físicos e cognitivos, e passeios, visando o envelhecimento saudável do pet. A recomendação deve ser detalhada e prática que aborde aspectos específicos da alimentação e cuidados nutricionais com base nas características do pet. Use uma sugestão de ação que o tutor possa fazer em casa, e outra no veterinário. Condições: personalize as sugestões com base nas informações fornecidas, evitando generalizações; as orientações devem ser realistas e alinhadas às condições de saúde e limitações do pet; adote um tom empático, educativo e motivador para engajar o tutor."

message_health = "Analise os dados de cadastro fornecidos sobre o pet (espécie, gênero, raça, idade, peso, problemas de saúde e medicações diárias), e crie uma recomendação personalizada em até mil caracteres relacionada aos cuidados da saúde preventivos e proativos voltados ao envelhecimento saudável. Considere as predisposições da raça, idade, e doenças secundárias. Para esta recomendação, não use exemplos de dieta e nutrição. Não use exemplos de enriquecimento ambiental e adaptações em casa. Use uma recomendação de ação que o tutor possa fazer em casa, e outra no veterinário. A recomendação deve ser detalhada e prática que aborde aspectos específicos da alimentação e cuidados nutricionais com base nas características do pet. Use uma sugestão de ação que o tutor possa fazer em casa, e outra no veterinário. Condições: use as informações fornecidas para criar recomendações específicas, evitando generalizações; as sugestões devem priorizar o envelhecimento saudável e as necessidades individuais do pet; mantenha o tom empático e educativo, reforçando o cuidado preventivo."


def format_prompt(message, pet):
    serialized = PetSerializer(pet)

    return str(serialized.data) + message


class PromptPetRecommendations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            pet_id = request.query_params["pet_id"]
            pet = get_pet_service({"id": pet_id})

            if pet["data"] is None:
                raise App_Error("Pet not founded", 404)

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

            return Response({"data": {"health": futures["health"].result(), "nutrition": futures["nutrition"].result(), "activity": futures["activity"].result()}})

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
