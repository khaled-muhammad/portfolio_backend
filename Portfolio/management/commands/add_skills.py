from django.core.management.base import BaseCommand
from Portfolio.models import Skill


class Command(BaseCommand):
    help = 'Add predefined skills to the database'

    def handle(self, *args, **options):
        skills_list = [
            "Html 5",
            "CSS 3",
            "JS",
            "Python",
            "Django",
            "DRF",
            "React",
            "React Router",
            "AXIOS",
            "Apache",
            "NGINX",
            "Bash",
            "Bootstrap",
            "Dart",
            "Flutter",
            "FileZilla",
            "GIT",
            "Github",
            "Illustrator",
            "JQuery",
            "JSON",
            "Jupyter",
            "Linux",
            "MD",
            "Matplotlib",
            "MySQL",
            "NumPy",
            "opencv",
            "Pandas",
            "Postman",
            "Realm",
            "SQLITE",
            "Supabase",
            "Tailwind",
            "TS",
            "VS Code",
            "ViteJS"
        ]

        # Mapping skills to appropriate sections
        skill_sections = {
            "Html 5": "Programming Language",
            "CSS 3": "Programming Language",
            "JS": "Programming Language",
            "TS": "Programming Language",
            "Python": "Programming Language",
            "Dart": "Programming Language",
            "Django": "Framework",
            "DRF": "Framework",
            "React": "Framework",
            "React Router": "Library",
            "Bootstrap": "Framework",
            "Tailwind": "Framework",
            "Flutter": "Framework",
            "AXIOS": "Library",
            "JQuery": "Library",
            "NumPy": "Library",
            "opencv": "Library",
            "Pandas": "Library",
            "Matplotlib": "Library",
            "MySQL": "Database",
            "SQLITE": "Database",
            "Supabase": "Database",
            "Realm": "Database",
            "Apache": "DevOp",
            "NGINX": "DevOp",
            "GIT": "DevOp",
            "Github": "DevOp",
            "FileZilla": "DevOp",
            "Postman": "DevOp",
            "VS Code": "DevOp",
            "ViteJS": "DevOp",
            "Bash": "DevOp",
            "Linux": "DevOp",
            "Jupyter": "DevOp",
            "Illustrator": "DevOp",
            "JSON": "DevOp",
            "MD": "DevOp"
        }

        created_count = 0
        updated_count = 0

        for skill_name in skills_list:
            skill, created = Skill.objects.get_or_create(
                title=skill_name,
                defaults={
                    'kind': 'skill',
                    'section': skill_sections.get(skill_name, None),
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created skill: {skill_name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Skill already exists: {skill_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: {created_count} skills created, {updated_count} skills already existed'
            )
        ) 