from django.core.management.base import BaseCommand
from apps.portfolio.models import Badge


class Command(BaseCommand):
    help = 'Create the initial 10 badges for the Academy'

    def handle(self, *args, **kwargs):
        badges_data = [
            {
                'name': 'First Steps',
                'description': 'Complétez votre premier exercice',
                'icon': '🎓',
                'condition_type': 'exercises_completed',
                'condition_value': 1,
                'color': 'green',
                'order': 1
            },
            {
                'name': 'Fire Starter',
                'description': 'Maintenez un streak de 3 jours consécutifs',
                'icon': '🔥',
                'condition_type': 'streak',
                'condition_value': 3,
                'color': 'red',
                'order': 2
            },
            {
                'name': 'Perfect Score',
                'description': 'Réussissez 5 exercices du premier coup',
                'icon': '🎯',
                'condition_type': 'first_try_success',
                'condition_value': 5,
                'color': 'blue',
                'order': 3
            },
            {
                'name': 'Bookworm',
                'description': 'Regardez 10 vidéos',
                'icon': '📚',
                'condition_type': 'videos_completed',
                'condition_value': 10,
                'color': 'purple',
                'order': 4
            },
            {
                'name': 'Python Pro',
                'description': 'Complétez 10 exercices Python',
                'icon': '🐍',
                'condition_type': 'exercises_completed',
                'condition_value': 10,
                'color': 'yellow',
                'order': 5
            },
            {
                'name': 'Speed Runner',
                'description': 'Complétez un exercice en moins de 5 minutes',
                'icon': '🚀',
                'condition_type': 'time_based',
                'condition_value': 5,
                'color': 'cyan',
                'order': 6
            },
            {
                'name': 'Early Bird',
                'description': 'Activité avant 8h du matin',
                'icon': '🌟',
                'condition_type': 'time_based',
                'condition_value': 8,
                'color': 'orange',
                'order': 7
            },
            {
                'name': 'Night Owl',
                'description': 'Activité après 22h',
                'icon': '🦉',
                'condition_type': 'time_based',
                'condition_value': 22,
                'color': 'indigo',
                'order': 8
            },
            {
                'name': 'Level Up',
                'description': 'Atteignez le niveau 5',
                'icon': '📈',
                'condition_type': 'level_reached',
                'condition_value': 5,
                'color': 'pink',
                'order': 9
            },
            {
                'name': 'Centurion',
                'description': 'Accumulez 100 XP',
                'icon': '🏆',
                'condition_type': 'xp_total',
                'condition_value': 100,
                'color': 'gold',
                'order': 10
            },
        ]

        created_count = 0
        for badge_data in badges_data:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created badge: {badge.icon} {badge.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Badge already exists: {badge.icon} {badge.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Done! {created_count} new badges created.')
        )


