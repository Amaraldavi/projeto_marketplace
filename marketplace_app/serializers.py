from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers
from .models import User, Category, Listing, ListingImage, StoreProfile, CommonProfile

# --- Tradutores de Anúncios (Para a Vitrine do React) ---

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image']

class ListingSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    seller_name = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Listing
        fields = [
            'id', 'seller', 'seller_name', 'category', 'title', 
            'description', 'price', 'listing_type', 'condition', 
            'status', 'is_featured', 'is_store_featured', 
            'created_at', 'images'
        ]

# --- Tradutor de Registro (Para o seu Front de Cadastro) ---

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_store = serializers.BooleanField(default=False)
    cpf = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    cep = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    cnpj = serializers.CharField(required=False, allow_blank=True)
    razao_social = serializers.CharField(required=False, allow_blank=True)
    fantasy_name = serializers.CharField(required=False, allow_blank=True)
    state_registration = serializers.CharField(required=False, allow_blank=True)
    responsible_name = serializers.CharField(required=False, allow_blank=True)
    responsible_cpf = serializers.CharField(required=False, allow_blank=True)
    commercial_cep = serializers.CharField(required=False, allow_blank=True)
    commercial_address = serializers.CharField(required=False, allow_blank=True)
    store_phone = serializers.CharField(required=False, allow_blank=True)
    store_email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'is_store',
            'cpf', 'birth_date', 'phone', 'cep', 'address',
            'cnpj', 'razao_social', 'fantasy_name', 'state_registration',
            'responsible_name', 'responsible_cpf', 'commercial_cep',
            'commercial_address', 'store_phone', 'store_email',
        ]

    def create(self, validated_data):
        cpf = validated_data.pop('cpf', None)
        birth_date = validated_data.pop('birth_date', None)
        phone = validated_data.pop('phone', '')
        cep = validated_data.pop('cep', '')
        address = validated_data.pop('address', '')
        cnpj = validated_data.pop('cnpj', None)
        razao_social = validated_data.pop('razao_social', None)
        fantasy_name = validated_data.pop('fantasy_name', '')
        state_registration = validated_data.pop('state_registration', '')
        responsible_name = validated_data.pop('responsible_name', '')
        responsible_cpf = validated_data.pop('responsible_cpf', '')
        commercial_cep = validated_data.pop('commercial_cep', '')
        commercial_address = validated_data.pop('commercial_address', '')
        store_phone = validated_data.pop('store_phone', '')
        store_email = validated_data.pop('store_email', '')
        is_store = validated_data.get('is_store', False)

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)

            try:
                if is_store:
                    profile = StoreProfile(
                        user=user,
                        cnpj=cnpj,
                        razao_social=razao_social,
                        fantasy_name=fantasy_name,
                        state_registration=state_registration,
                        responsible_name=responsible_name,
                        responsible_cpf=responsible_cpf,
                        phone=store_phone,
                        email=store_email,
                        commercial_cep=commercial_cep,
                        commercial_address=commercial_address,
                    )
                    profile.full_clean()
                    profile.save()
                else:
                    profile = CommonProfile(
                        user=user,
                        cpf=cpf,
                        birth_date=birth_date,
                        phone=phone,
                        cep=cep,
                        address=address,
                    )
                    profile.full_clean()
                    profile.save()
            except DjangoValidationError as error:
                raise serializers.ValidationError(error.message_dict if hasattr(error, 'message_dict') else error.messages)

        return user