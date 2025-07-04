import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from Portfolio.models import Certificate
from PIL import Image as PILImage
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Add certificates from the Certificates directory to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing certificates before adding new ones',
        )
        parser.add_argument(
            '--certificates-dir',
            type=str,
            default='Certificates',
            help='Path to certificates directory (default: Certificates)',
        )

    def handle(self, *args, **options):
        certificates_dir = options['certificates_dir']
        clear_existing = options['clear_existing']
        
        if clear_existing:
            self.stdout.write("Clearing existing certificates...")
            Certificate.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Existing certificates cleared."))
        
        # Statistics
        total_processed = 0
        created_count = 0
        skipped_count = 0
        error_count = 0
        
        # Process each subdirectory
        certificates_path = Path(certificates_dir)
        
        if not certificates_path.exists():
            self.stdout.write(
                self.style.ERROR(f"Certificates directory not found: {certificates_path}")
            )
            return
        
        # Category mapping based on directory names
        category_mapping = {
            'courses': 'courses',
            'contests': 'contests', 
            'benchmarks': 'benchmarks',
            'participation': 'participation',
            'scholarships': 'scholarships'
        }
        
        for category_dir in certificates_path.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith('.'):
                continue
                
            category = category_mapping.get(category_dir.name.lower())
            if not category:
                self.stdout.write(
                    self.style.WARNING(f"Unknown category directory: {category_dir.name}")
                )
                continue
            
            self.stdout.write(f"\nProcessing {category} certificates...")
            
            for file_path in category_dir.iterdir():
                if file_path.is_file() and not file_path.name.startswith('.'):
                    total_processed += 1
                    
                    # Check if it's an image file
                    if not self.is_image_file(file_path):
                        self.stdout.write(
                            self.style.WARNING(f"Skipping non-image file: {file_path.name}")
                        )
                        skipped_count += 1
                        continue
                    
                    try:
                        # Check if certificate already exists
                        title = self.extract_title_from_filename(file_path.name)
                        if Certificate.objects.filter(title=title, category=category).exists():
                            self.stdout.write(
                                self.style.WARNING(f"Certificate already exists: {title}")
                            )
                            skipped_count += 1
                            continue
                        
                        # Create certificate record
                        certificate = self.create_certificate(file_path, category, title)
                        if certificate:
                            created_count += 1
                            self.stdout.write(
                                self.style.SUCCESS(f"✓ Added: {certificate.title}")
                            )
                        else:
                            error_count += 1
                            
                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(f"Error processing {file_path.name}: {str(e)}")
                        )
        
        # Summary
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS("CERTIFICATE IMPORT SUMMARY"))
        self.stdout.write("="*60)
        self.stdout.write(f"Total files processed: {total_processed}")
        self.stdout.write(f"Certificates created: {created_count}")
        self.stdout.write(f"Files skipped: {skipped_count}")
        self.stdout.write(f"Errors: {error_count}")
        self.stdout.write("="*60)
    
    def is_image_file(self, file_path):
        """Check if file is an image"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp'}
        return file_path.suffix.lower() in image_extensions
    
    def extract_title_from_filename(self, filename):
        """Extract a clean title from filename"""
        # Remove file extension
        title = Path(filename).stem
        
        # Clean up common patterns
        title = title.replace('_', ' ')
        title = title.replace('-', ' ')
        
        # Handle specific patterns
        title_mappings = {
            'free-iqtest.net_cert_print.asp_cid=2237EF1E-59EF-4ED9-B6CB-7342CF3AA9A0&cert=1': 'IQ Test Certificate',
            'ratatype': 'Ratatype Typing Certificate',
            'EF SET Certificate': 'EF SET English Certificate',
            'Typing Certificate (Ratatype)': 'Ratatype Typing Certificate',
            'certificate': 'General Certificate',
            'Course_Certificate_En': 'Course Completion Certificate',
            'Certificate _ NVIDIA': 'NVIDIA Certificate',
            'c2fa08e0-c9c5-4c4b-aa5a-0b4a418bc08c': 'Event Participation Certificate',
            '3 members_page-0050': 'Team Certificate',
            'AWS Edcuate Participation Cert(530)': 'AWS Educate Participation Certificate',
            'خالد محمد ابراهيم': 'Khaled Muhammad Ibrahim Contest Certificate',
        }
        
        # Check for exact matches first
        clean_filename = Path(filename).stem
        if clean_filename in title_mappings:
            return title_mappings[clean_filename]
        
        # Handle Coursera certificates with IDs
        if title.startswith('Coursera ') and len(title.split()) == 2:
            return f'Coursera Certificate {title.split()[1]}'
        
        # Handle name-specific patterns
        if 'Khaled Muhammad' in title or 'Khaled_Muhammad' in title:
            # Extract the main subject
            if 'ChatGPT' in title:
                return 'ChatGPT Certificate'
            elif 'C#' in title or 'C Sharp' in title:
                return 'C# Programming Certificate'
            elif 'Ethical Hacking' in title:
                return 'Ethical Hacking Certificate'
            elif 'html5-css3-js' in title:
                return 'HTML5 CSS3 JavaScript Certificate'
            elif 'abacus' in title:
                return 'Abacus Certificate'
        
        # Handle platform-specific patterns
        if 'from Sololearn' in title:
            language = title.split(' from Sololearn')[0]
            return f'{language} Certificate - Sololearn'
        
        if 'Udacity' in title:
            return 'Udacity Tech Skills Certificate'
        
        # Handle contest/event names
        if 'ICPC' in title:
            return 'ICPC Programming Contest Certificate'
        
        if 'NASA Space Apps' in title:
            return 'NASA Space Apps Challenge Certificate'
        
        if 'Flutter Puzzle Hack' in title:
            return 'Flutter Puzzle Hack Certificate'
        
        if 'DECI' in title:
            if 'Level 2' in title:
                return 'DECI Level 2 Scholarship'
            elif 'Level 3' in title:
                return 'DECI Level 3 Scholarship'
            elif 'GEEKS' in title:
                return 'DECI GEEKS Participation Certificate'
            elif 'Innovation Day' in title:
                return 'DECI Innovation Day Certificate'
        
        if 'Ebhar Misr' in title:
            return 'Ebhar Misr 2024 Scholarship'
        
        # Default: capitalize and clean
        return ' '.join(word.capitalize() for word in title.split())
    
    def extract_issuer_from_title(self, title, filename):
        """Extract issuer from title or filename"""
        issuers = {
            'coursera': 'Coursera',
            'sololearn': 'Sololearn', 
            'udacity': 'Udacity',
            'nvidia': 'NVIDIA',
            'nasa': 'NASA',
            'aws': 'AWS',
            'icpc': 'ICPC',
            'deci': 'DECI',
            'ef set': 'EF Education First',
            'ratatype': 'Ratatype',
            'flutter': 'Google',
            'chatgpt': 'OpenAI',
        }
        
        title_lower = title.lower()
        filename_lower = filename.lower()
        
        for key, issuer in issuers.items():
            if key in title_lower or key in filename_lower:
                return issuer
        
        return None
    
    def create_certificate(self, file_path, category, title):
        """Create a certificate record in the database"""
        try:
            # Calculate aspect ratio
            with PILImage.open(file_path) as img:
                width, height = img.size
                aspect_ratio = round(width / height, 3) if height > 0 else None
            
            # Create certificate instance
            certificate = Certificate()
            certificate.title = title
            certificate.category = category
            certificate.aspect_ratio = aspect_ratio
            certificate.issuer = self.extract_issuer_from_title(title, file_path.name)
            
            # Create description based on category and title
            certificate.description = self.generate_description(title, category)
            
            # Copy file to media directory and assign to image field
            with open(file_path, 'rb') as f:
                django_file = File(f)
                certificate.image.save(
                    file_path.name,
                    django_file,
                    save=False
                )
            
            # Save the certificate (this will trigger the save method and recalculate aspect ratio)
            certificate.save()
            
            return certificate
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error creating certificate from {file_path}: {str(e)}")
            )
            return None
    
    def generate_description(self, title, category):
        """Generate a description based on title and category"""
        descriptions = {
            'courses': f'Certificate of completion for {title}',
            'contests': f'Achievement certificate from {title}',
            'benchmarks': f'Performance benchmark certificate - {title}',
            'participation': f'Participation certificate for {title}',
            'scholarships': f'Scholarship award - {title}',
        }
        
        return descriptions.get(category, f'Certificate - {title}') 