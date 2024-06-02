from django.contrib import admin
from django.contrib.auth.models import User, Group

class CustomAdminSite(admin.AdminSite):
    site_header = "DexGO 管理后台"
    site_title = "DexGO 管理"
    index_title = "欢迎使用 DexGO 管理后台"

    def each_context(self, request):
        context = super().each_context(request)
        user_groups = request.user.groups.values_list('name', flat=True)
        context['user_groups'] = user_groups
        return context


custom_admin_site = CustomAdminSite(name='custom_admin')


class CustomModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # 根据用户组过滤数据
        if request.user.groups.filter(name='manager').exists():
            return qs.filter(manager=request.user)
        if request.user.groups.filter(name='merchant').exists():
            return qs.filter(merchant=request.user)
        return qs

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='manager').exists() and obj and obj.manager == request.user:
            return True
        if request.user.groups.filter(name='merchant').exists() and obj and obj.merchant == request.user:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='manager').exists() and obj and obj.manager == request.user:
            return True
        if request.user.groups.filter(name='merchant').exists() and obj and obj.merchant == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='manager').exists() and obj and obj.manager == request.user:
            return True
        if request.user.groups.filter(name='merchant').exists() and obj and obj.merchant == request.user:
            return True
        return False


custom_admin_site.register(User)
custom_admin_site.register(Group)
