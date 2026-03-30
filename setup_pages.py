import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'viktorijacoaching.settings.production')
django.setup()

from wagtail.models import Page, Site
from home.models import HomePage
from pages.models import AboutPage

root = Page.objects.get(depth=1)

if not HomePage.objects.exists():
    welcome = Page.objects.filter(depth=2).first()
    if welcome:
        welcome.delete()
        root = Page.objects.get(depth=1)
    hp = HomePage(
        title='Home', slug='home',
        hero_title='Transform Your Life with Purpose & Clarity',
        hero_subtitle='Empowering ambitious women to unlock their full potential through personalized coaching, mindset mastery, and strategic action.',
        hero_cta_text='Work With Me',
        about_heading='Meet Viktorija',
        about_text='<p>I am a certified life coach passionate about helping women step into their power, find clarity in their vision, and build lives that truly light them up. With a background in psychology and years of coaching experience, I bring a unique blend of warmth, insight, and practical strategy to every session.</p>',
        services_heading='How I Can Help',
        services_subheading='Whether you are navigating a career transition, seeking deeper self-awareness, or ready to level up in every area of life, I have a path designed for you.',
        testimonials_heading='What Clients Say',
        newsletter_heading='Join My Community',
        newsletter_text='Get weekly insights on personal growth, mindset shifts, and practical tools delivered straight to your inbox.',
        cta_heading='Ready to Begin Your Transformation?',
        cta_text='Every journey starts with a single step. Book a free discovery call and let us explore how coaching can help you create the life you have been dreaming of.',
        cta_button_text="Let's Connect",
    )
    root.add_child(instance=hp)
    hp.save_revision().publish()
    print("Created HomePage")
else:
    hp = HomePage.objects.first()
    print("HomePage exists")

site = Site.objects.first()
if site:
    site.root_page = hp
    site.site_name = 'Viktorija Coaching'
    site.save()
else:
    Site.objects.create(hostname='localhost', root_page=hp, is_default_site=True, site_name='Viktorija Coaching')

if not AboutPage.objects.exists():
    about = AboutPage(
        title='About', slug='about', show_in_menus=True,
        hero_heading="Hi, I'm Viktorija",
        hero_subheading='Life coach, mindset mentor, and your biggest cheerleader on the path to becoming who you were always meant to be.',
        credentials_heading='Credentials & Training',
        philosophy_heading='My Approach',
        philosophy_text='<p>I believe that every woman has the power within her to create extraordinary change. My coaching approach blends evidence-based psychology with intuitive guidance, creating a safe space for deep transformation.</p>',
        personal_heading='Beyond the Bio',
        cta_heading='Ready to Start Your Journey?',
        cta_text='I would love to hear your story and explore how we can work together.',
        cta_button_text="Let's Connect",
    )
    hp.add_child(instance=about)
    about.save_revision().publish()
    print("Created AboutPage")
else:
    print("AboutPage exists")

for p in Page.objects.all():
    print(f"  {p.depth} | {p.title} | {type(p.specific).__name__}")
