from django.db import models
from PIL import Image as PILImage
import os
from multiselectfield import MultiSelectField

# Create your models here.

PLATFORM_CHOICES = [
    ("GitHub", "GitHub"),
    ("GitLab", "GitLab"),
    ("Bitbucket", "Bitbucket"),
    ("LinkedIn", "LinkedIn"),
    ("Twitter", "Twitter"),
    ("X", "X (Twitter)"),
    ("Facebook", "Facebook"),
    ("Instagram", "Instagram"),
    ("YouTube", "YouTube"),
    ("Twitch", "Twitch"),
    ("Reddit", "Reddit"),
    ("StackOverflow", "Stack Overflow"),
    ("Hashnode", "Hashnode"),
    ("DevTo", "Dev.to"),
    ("Medium", "Medium"),
    ("Dribbble", "Dribbble"),
    ("Behance", "Behance"),
    ("CodePen", "CodePen"),
    ("LeetCode", "LeetCode"),
    ("HackerRank", "HackerRank"),
    ("Codeforces", "Codeforces"),
    ("Codewars", "Codewars"),
    ("Kaggle", "Kaggle"),
    ("Replit", "Replit"),
    ("Discord", "Discord"),
    ("Telegram", "Telegram"),
    ("Figma", "Figma"),
    ("ProductHunt", "Product Hunt"),
    ("Substack", "Substack"),
    ("Notion", "Notion"),
    ("Other", "Other"),
]

PROJECT_PLATFORM_CHOICES = [
    ("web", "Web"),
    ("mobile", "Mobile"),
    ("scripts", "Scripts"),
    ("cli", "CLI"),
    ("software_gui", "Software/GUI"),
]

def uploadSkillIcon(instance, filename):
    return "skillsIcon/admin/%s@%s" % (instance.title, filename)


def uploadWorkImage(instance, filename):
    return "WorksImage/admin/%s@%s" % (instance.name, filename)


def uploadCertificateImage(instance, filename):
    return "Certificate/admin/%s" % (filename)


kinds = (
    ("skill", "skill"),
    ("tool", "tool"),
)

sections = (
    ("Programming Language", "Programming Language"),
    ("Framework", "Framework"),
    ("Database", "Database"),
    ("DevOp", "DevOp"),
    ("Library", "Library"),
)


class Use(models.Model):
    uses = models.CharField(max_length=300)

    def __str__(self):
        return self.uses


class Skill(models.Model):
    title = models.CharField(max_length=100)
    about = models.TextField(max_length=10000, blank=True, null=True)
    summary = models.TextField(max_length=10000, blank=True, null=True)
    icon = models.ImageField(upload_to=uploadSkillIcon, blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)
    uses = models.TextField(max_length=10000, blank=True, null=True)
    abilites = models.TextField(max_length=10000, blank=True, null=True)
    kind = models.CharField(max_length=80, choices=kinds)
    section = models.CharField(
        max_length=100, choices=sections, blank=True, null=True)
    yearsOfExprience = models.IntegerField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class CMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(max_length=1500)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    platforms = MultiSelectField(choices=PROJECT_PLATFORM_CHOICES)
    url = models.URLField(null=True, blank=True)
    description = models.TextField(max_length=1500, blank=True, null=True)
    image = models.ImageField(upload_to=uploadWorkImage)
    stack = models.ManyToManyField(Skill)
    status = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Info(models.Model):
    title = models.CharField(max_length=60, unique=True)
    info = models.TextField(max_length=500)

    def __str__(self):
        return self.title


CERTIFICATE_CATEGORIES = [
    ('courses', 'Courses'),
    ('contests', 'Contests'),
    ('benchmarks', 'Benchmarks'),
    ('participation', 'Participation'),
    ('scholarships', 'Scholarships'),
]


class Certificate(models.Model):
    image = models.ImageField(upload_to=uploadCertificateImage)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CERTIFICATE_CATEGORIES, null=True, blank=True)
    aspect_ratio = models.FloatField(null=True, blank=True, help_text="Width/Height ratio")
    date_issued = models.DateField(null=True, blank=True)
    issuer = models.CharField(max_length=255, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Calculate aspect ratio automatically when saving
        if self.image and hasattr(self.image, 'path'):
            try:
                with PILImage.open(self.image.path) as img:
                    width, height = img.size
                    self.aspect_ratio = round(width / height, 3) if height > 0 else None
            except Exception:
                self.aspect_ratio = None
        super().save(*args, **kwargs)
    
    def calculate_aspect_ratio(self):
        """Calculate aspect ratio from image file"""
        if self.image and hasattr(self.image, 'path') and os.path.exists(self.image.path):
            try:
                with PILImage.open(self.image.path) as img:
                    width, height = img.size
                    return round(width / height, 3) if height > 0 else None
            except Exception:
                return None
        return None
    
    def get_image_dimensions(self):
        """Get image width and height"""
        if self.image and hasattr(self.image, 'path') and os.path.exists(self.image.path):
            try:
                with PILImage.open(self.image.path) as img:
                    return img.size
            except Exception:
                return None, None
        return None, None
    
    def __str__(self):
        return self.title or f"Certificate {self.id}"


class SocialMedia(models.Model):
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES)
    url = models.CharField(max_length=500)
    username = models.CharField(max_length=150)

    def __str__(self):
        return self.platform