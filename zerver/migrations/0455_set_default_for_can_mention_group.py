# Generated by Django 4.2.1 on 2023-06-12 10:47

from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps


def set_default_value_for_can_mention_group(
    apps: StateApps, schema_editor: BaseDatabaseSchemaEditor
) -> None:
    Realm = apps.get_model("zerver", "Realm")
    UserGroup = apps.get_model("zerver", "UserGroup")

    groups_to_update = []
    for realm in Realm.objects.all():
        # The default value of `can_mention_group` is everyone group for
        # all groups except role-based system groups. For role-based system
        # groups, we set the value of `can_mention_group` to nobody group.
        nobody_group = UserGroup.objects.get(name="@role:nobody", realm=realm, is_system_group=True)
        everyone_group = UserGroup.objects.get(
            name="@role:everyone", realm=realm, is_system_group=True
        )
        for group in UserGroup.objects.filter(realm=realm):
            if group.is_system_group:
                group.can_mention_group = nobody_group
            else:
                group.can_mention_group = everyone_group
            groups_to_update.append(group)

    UserGroup.objects.bulk_update(groups_to_update, ["can_mention_group"])


class Migration(migrations.Migration):
    dependencies = [
        ("zerver", "0454_usergroup_can_mention_group"),
    ]

    operations = [
        migrations.RunPython(
            set_default_value_for_can_mention_group,
            elidable=True,
            reverse_code=migrations.RunPython.noop,
        )
    ]