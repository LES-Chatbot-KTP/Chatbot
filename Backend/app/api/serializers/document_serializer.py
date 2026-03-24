from rest_framework import serializers

TIPOS_PERMITIDOS = ["portaria", "resolucao", "rod"]


class DocumentCreateSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=255)
    tipo = serializers.ChoiceField(choices=TIPOS_PERMITIDOS)
    caminho_arquivo = serializers.CharField(max_length=500)


class DocumentUpdateSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=255, required=False)
    tipo = serializers.ChoiceField(choices=TIPOS_PERMITIDOS, required=False)
    caminho_arquivo = serializers.CharField(max_length=500, required=False)

    def validate(self, data):
        if not data:
            raise serializers.ValidationError(
                "Envie ao menos um campo para atualizar: nome, tipo ou caminho_arquivo."
            )
        return data