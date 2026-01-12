from rest_framework import serializers
from .models import SlackUser, SlackUserEmail, SlackUserPhoneNumber, SlackUserAddress, SlackUserGroup, SlackUserPhoto, SlackUserRole
import uuid
from datetime import datetime

class SlackUserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlackUserEmail
        fields = ['value', 'type', 'primary']

class SlackUserPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlackUserPhoneNumber
        fields = ['value', 'type', 'primary']

class SlackUserAddressSerializer(serializers.ModelSerializer):
    streetAddress = serializers.CharField(source='street_address')
    postalCode = serializers.CharField(source='postal_code')
    
    class Meta:
        model = SlackUserAddress
        fields = ['formatted', 'streetAddress', 'locality', 'region', 'postalCode', 'country', 'type', 'primary']

class SlackUserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlackUserGroup
        fields = ['value', 'display', 'type']

class SlackUserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlackUserPhoto
        fields = ['value', 'type']

class SlackUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlackUserRole
        fields = ['value', 'primary']

class SlackUserSerializer(serializers.ModelSerializer):
    emails = SlackUserEmailSerializer(many=True, required=False)
    phoneNumbers = SlackUserPhoneNumberSerializer(many=True, required=False, source='phone_numbers')
    addresses = SlackUserAddressSerializer(many=True, required=False)
    groups = SlackUserGroupSerializer(many=True, required=False)
    photos = SlackUserPhotoSerializer(many=True, required=False)
    roles = SlackUserRoleSerializer(many=True, required=False)
    
    # SCIM required fields
    schemas = serializers.SerializerMethodField()
    id = serializers.CharField(source='scim_id', read_only=True)
    externalId = serializers.CharField(source='external_id', required=False, allow_blank=True)
    userName = serializers.CharField(source='user_name', required=False)
    nickName = serializers.CharField(source='nick_name', required=False, allow_blank=True)
    displayName = serializers.CharField(source='display_name', required=False, allow_blank=True)
    profileUrl = serializers.URLField(source='profile_url', required=False, allow_blank=True)
    userType = serializers.CharField(source='user_type', required=False, allow_blank=True)
    preferredLanguage = serializers.CharField(source='preferred_language', required=False, allow_blank=True)
    
    # Direct field mappings for name components (write-only)
    given_name = serializers.CharField(required=False, allow_blank=True, write_only=True)
    family_name = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    # SCIM name object
    name = serializers.SerializerMethodField()
    
    # SCIM meta object
    meta = serializers.SerializerMethodField()
    
    # Enterprise extension
    enterprise_extension = serializers.SerializerMethodField(source='get_enterprise_extension')
    
    # Slack extension
    slack_extension = serializers.SerializerMethodField(source='get_slack_extension')
    
    class Meta:
        model = SlackUser
        fields = [
            'schemas', 'id', 'externalId', 'userName', 'nickName', 'name', 'displayName',
            'profileUrl', 'title', 'userType', 'preferredLanguage', 'locale', 'timezone',
            'active', 'password', 'emails', 'phoneNumbers', 'addresses', 'photos', 'roles',
            'groups', 'meta', 'enterprise_extension', 'slack_extension', 'given_name', 'family_name'
        ]
        read_only_fields = ['id']
    
    def get_schemas(self, obj):
        return [
            "urn:ietf:params:scim:schemas:core:2.0:User",
            "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User",
            "urn:ietf:params:scim:schemas:extension:slack:profile:2.0:User"
        ]
    
    def get_name(self, obj):
        return {
            'formatted': obj.formatted_name,
            'familyName': obj.family_name,
            'givenName': obj.given_name,
            'middleName': obj.middle_name,
            'honorificPrefix': obj.honorific_prefix,
            'honorificSuffix': obj.honorific_suffix
        }
    
    def get_meta(self, obj):
        return {
            'created': obj.created.isoformat() if obj.created else None,
            'location': f"https://api.slack.com/scim/v2/Users/{obj.scim_id}" if obj.scim_id else None
        }
    
    def get_enterprise_extension(self, obj):
        extension = {
            'employeeNumber': obj.employee_number,
            'costCenter': obj.cost_center,
            'organization': obj.organization,
            'division': obj.division,
            'department': obj.department
        }
        if obj.manager_id:
            extension['manager'] = {'managerId': obj.manager_id}
        return extension
    
    def get_slack_extension(self, obj):
        return {
            'startDate': obj.start_date.isoformat() if obj.start_date else None
        }
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add enterprise extension with proper key
        data['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User'] = data.pop('enterprise_extension')
        data['urn:ietf:params:scim:schemas:extension:slack:profile:2.0:User'] = data.pop('slack_extension')
        return data
    
    def create(self, validated_data):
        emails_data = validated_data.pop('emails', [])
        phone_numbers_data = validated_data.pop('phone_numbers', [])
        addresses_data = validated_data.pop('addresses', [])
        groups_data = validated_data.pop('groups', [])
        photos_data = validated_data.pop('photos', [])
        roles_data = validated_data.pop('roles', [])
        
        # Handle enterprise extension
        enterprise_data = self.initial_data.get('urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', {})
        validated_data.update({
            'employee_number': enterprise_data.get('employeeNumber', ''),
            'cost_center': enterprise_data.get('costCenter', ''),
            'organization': enterprise_data.get('organization', ''),
            'division': enterprise_data.get('division', ''),
            'department': enterprise_data.get('department', ''),
            'manager_id': enterprise_data.get('manager', {}).get('managerId', '')
        })
        
        # Handle slack extension
        slack_data = self.initial_data.get('urn:ietf:params:scim:schemas:extension:slack:profile:2.0:User', {})
        if slack_data.get('startDate'):
            validated_data['start_date'] = datetime.fromisoformat(slack_data['startDate'].replace('Z', '+00:00'))
        
        # Handle name object from input
        name_data = self.initial_data.get('name', {})
        validated_data.update({
            'formatted_name': name_data.get('formatted', ''),
            'family_name': name_data.get('familyName', validated_data.get('family_name', '')),
            'given_name': name_data.get('givenName', validated_data.get('given_name', '')),
            'middle_name': name_data.get('middleName', ''),
            'honorific_prefix': name_data.get('honorificPrefix', ''),
            'honorific_suffix': name_data.get('honorificSuffix', '')
        })
        
        validated_data['scim_id'] = str(uuid.uuid4())
        
        # Generate unique username if empty or not provided
        if not validated_data.get('user_name'):
            # Use email as username if available
            if emails_data:
                validated_data['user_name'] = emails_data[0]['value']
            else:
                validated_data['user_name'] = f"user_{validated_data['scim_id'][:8]}"
        
        # Set slack_user_id to None if not provided to avoid unique constraint issues
        if not validated_data.get('slack_user_id'):
            validated_data['slack_user_id'] = None
            
        user = SlackUser.objects.create(**validated_data)
        
        # Create related objects
        for email_data in emails_data:
            SlackUserEmail.objects.create(user=user, **email_data)
        
        for phone_data in phone_numbers_data:
            SlackUserPhoneNumber.objects.create(user=user, **phone_data)
        
        for address_data in addresses_data:
            SlackUserAddress.objects.create(user=user, **address_data)
        
        for group_data in groups_data:
            SlackUserGroup.objects.create(user=user, **group_data)
        
        for photo_data in photos_data:
            SlackUserPhoto.objects.create(user=user, **photo_data)
        
        for role_data in roles_data:
            SlackUserRole.objects.create(user=user, **role_data)
        
        return user
        
    def update(self, instance, validated_data):
        emails_data = validated_data.pop('emails', [])
        phone_numbers_data = validated_data.pop('phone_numbers', [])
        addresses_data = validated_data.pop('addresses', [])
        groups_data = validated_data.pop('groups', [])
        photos_data = validated_data.pop('photos', [])
        roles_data = validated_data.pop('roles', [])
        
        # Handle enterprise extension
        enterprise_data = self.initial_data.get('urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', {})
        if enterprise_data:
            validated_data.update({
                'employee_number': enterprise_data.get('employeeNumber', instance.employee_number),
                'cost_center': enterprise_data.get('costCenter', instance.cost_center),
                'organization': enterprise_data.get('organization', instance.organization),
                'division': enterprise_data.get('division', instance.division),
                'department': enterprise_data.get('department', instance.department),
                'manager_id': enterprise_data.get('manager', {}).get('managerId', instance.manager_id)
            })
        
        # Handle slack extension
        slack_data = self.initial_data.get('urn:ietf:params:scim:schemas:extension:slack:profile:2.0:User', {})
        if slack_data and slack_data.get('startDate'):
            validated_data['start_date'] = datetime.fromisoformat(slack_data['startDate'].replace('Z', '+00:00'))
        
        # Handle name object from input
        name_data = self.initial_data.get('name', {})
        if name_data:
            validated_data.update({
                'formatted_name': name_data.get('formatted', instance.formatted_name),
                'family_name': name_data.get('familyName', validated_data.get('family_name', instance.family_name)),
                'given_name': name_data.get('givenName', validated_data.get('given_name', instance.given_name)),
                'middle_name': name_data.get('middleName', instance.middle_name),
                'honorific_prefix': name_data.get('honorificPrefix', instance.honorific_prefix),
                'honorific_suffix': name_data.get('honorificSuffix', instance.honorific_suffix)
            })
        
        # Update instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        # Update related objects if provided
        if emails_data:
            instance.emails.all().delete()
            for email_data in emails_data:
                SlackUserEmail.objects.create(user=instance, **email_data)
        
        if phone_numbers_data:
            instance.phone_numbers.all().delete()
            for phone_data in phone_numbers_data:
                SlackUserPhoneNumber.objects.create(user=instance, **phone_data)
        
        return instance