from django.urls import path
from diary.apps import DiaryConfig


app_name = DiaryConfig.name


urlpatterns = [
    # path('home/', home, name='home'),
    # path('contacts/', contacts, name='contacts'),
    # path('catalog/', ProductListView.as_view(), name='product_list'),
    # path('catalog/<int:pk>/', ProductDetailListView.as_view(), name='product_detail'),
    # path('catalog/new', ProductCreateView.as_view(), name='product_create'),
    # path('catalog/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    # path('catalog/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
    #
    # path('catalog/category/', CategoryListView.as_view(), name='category_list'),
    # path('catalog/category/<int:pk>/', CategoryDetailListView.as_view(), name='category_detail'),
    # path('catalog/category/new', CategoryCreateView.as_view(), name='category_create'),
    # path('catalog/category/<int:pk>/update', CategoryUpdateView.as_view(), name='category_update'),
    # path('catalog/category/list/<int:category_id>/', ProductByCategoryListView.as_view(), name='category_products'),
]