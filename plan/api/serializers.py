from rest_framework import serializers
from plan.models import Plan, PlanItem

class PlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItem
        fields = ( 'name', 'description')
        read_only_fields = ("id",)

class PlanSerializer(serializers.ModelSerializer):
    features = PlanItemSerializer(many=True, required = False, allow_null=True)

    class Meta:
        model = Plan
        fields = ('id', 'name', 'description', 'price', 'features')
        read_only_fields = ('id',)

    def create(self, validated_data):
        # Create a new Plan instance
        features_data = validated_data.pop('features', [])
        plan = Plan.objects.create(**validated_data)
        if features_data is not None:
            # Create new PlanItem instances and add them to the new Plan instance
            for feature in features_data:
                plan_item = PlanItem.objects.create(plan=plan, **feature)
                plan.features.add(plan_item)
        
        return plan

    def update(self, instance, validated_data):
        # Update the fields of the Plan instance
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        
        # Update the PlanItem instances related to this Plan
        feature_data = validated_data.pop('features', None)
        if feature_data is not None:
            instance.features.clear()
            for feature in feature_data:
                if feature.get('id'):
                    item = PlanItem.objects.get(pk=feature['id'])
                    item.name = feature.get('name', item.name)
                    item.description = feature.get('description', item.description)
                    item.save()
                    instance.features.add(item)
                else:
                    item = PlanItem.objects.create(**feature)
                    instance.features.add(item)
        instance.save()
        return instance