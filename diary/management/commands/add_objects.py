from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Add test books to the database'

    def handle(self, *args, **options):
        categorys = [
            {
                'name': 'Молочка',
                'description': 'Молочные продукты'
            },
            {
                'name': 'Выпечка',
                'description': 'Хлобобулочные'
            }
        ]
        A = Category.objects.get(name='Молочка')
        B = Category.objects.get(name='Выпечка')
        products = [
            {
                'name': 'Молоко',
                'description': 'Молоко',
                'category': A,
                'price': '100',
                'created_at': '2025-06-21',
                'updated_at': '2025-06-21'
            },
            {
                'name': 'Хлеб',
                'description': 'Хлеб',
                'category': B,
                'price': '50',
                'created_at': '2025-06-21',
                'updated_at': '2025-06-21'
            }
        ]

        for category_data in categorys:
            category, created = Category.objects.get_or_create(**category_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added category: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category.name}'))
        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))


[{"model": "catalog.category", "pk": 6, "fields": {"name": "Молочка", "description": "Молочные продукты"}},
 {"model": "catalog.category", "pk": 7, "fields": {"name": "Выпечка", "description": "Хлобобулочные"}}]
